"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys
from time import sleep

from requests.api import get
from env.error import ErrorsCodes
from env import envParser, error
from loguru import logger
from database.sqlParserClass import ParserSqlInterface

class SecondStep:


    def __init__(self, platform, city):
        # атрибуты для отслеживания обновления базы
        self.countUpdateRecords = 0
        self.countDeleteRecords = 0
        self.countRecursion = 0

        # объект платформы для парсинга
        self.objectPlatform = envParser.objectPlatform[platform]
        # информция о запущенном процессе (платформа и город)
        self.namePlatform = platform
        self.city = city
        # header для метода get модуля requests
        self.header = envParser.headerUserAgent
        # прокси сервера для метода get
        self.proxies = envParser.proxies
        # количество записей к обновлению за один запрос к базе
        self.limitGetRecord = 100
        # подключение к базе
        self.sqlClient = ParserSqlInterface(
            envParser.databaseSettings['database'], 
            envParser.databaseSettings['user'], 
            envParser.databaseSettings['password'], 
            envParser.databaseSettings['host'])
        
        # настрйоки логирования
        logger.add("logs/Report.log", format='{time} | {level} | {message}', level="DEBUG", rotation="2 MB", compression='zip')

    # смена статуса сообщающего об обсновлении записи
    def switchUpdateStatusRecords(self):
        self.sqlClient.updateStatusToFalse(self.namePlatform, self.city)
    # сведения о количестве обновленных/удаленных записях
    def getCountEndProgram(self):
        return (self.countUpdateRecords, self.countDeleteRecords, self.countRecursion)

    @logger.catch
    def run(self):

        tableWithRecords = self.sqlClient.getAdsForSecondStep(self.city, self.namePlatform, self.limitGetRecord)
        for record in tableWithRecords:
            getData = self.objectPlatform.getInfoPageCar(record[0])
            

            # Объявление удалено (ошибка 404)
            if getData['errors'] == error.ErrorsCodes.deleteAction:
                self.countDeleteRecords += 1
                # logger.warning(f"Объявление удалено: {record[0]}")
                self.sqlClient.moveToOldAds(record[0])
            
            else:
                # Ошибка запроса (будет проверенно повторно)
                if getData['errors'] == error.ErrorsCodes.requestError:
                    logger.error(f"Request errror {record[0]}")
                    continue
                
                # logger.debug(f"Обновленно: {record[0]}")
                # logger.debug(getData)
                self.sqlClient.UpdateSecondStep(getData)
                self.countUpdateRecords += 1
                
                # Машина проданна
                
                if getData['errors'] == error.ErrorsCodes.soldThisCar:
                    self.countDeleteRecords += 1
                    # logger.warning(f"Машина продана: {record[0]}")
                    self.sqlClient.moveToOldAds(record[0])
                    self.countUpdateRecords -= 1
        
        ostRecords = int(self.sqlClient.getCountAdsForOffset(self.city, self.namePlatform, 'ads'))
        #logger.info(f'RUN --- {self.city} {self.namePlatform} --- Осталось записей: {ostRecords}')
        if ostRecords > 0:
            self.countRecursion += 1
            try:
                return self.run()
            except RecursionError:
                return self.run()
        else:
            # logger.success(f"END --- {self.city} {self.namePlatform} --- Обновленно: {self.countUpdateRecords}, Удалено {self.countDeleteRecords}")
            return None


if __name__ == '__main__':
    #nameCity = 'irkutsk'
    #namePlatform = 'drom'
    namePlatform = sys.argv[1]
    nameCity = sys.argv[2]
    obj = SecondStep(namePlatform, nameCity)
    try:
        obj.switchUpdateStatusRecords()
        obj.run()
    except BaseException:
        logger.add('logs/Create_process.log')
        logger.error("Программа проработала не до конца")
    else:
        logger.add('logs/Create_process.log')
        tupleCount = obj.getCountEndProgram()
        logger.success(f"Программа успешно завершилась. Обновленно: {tupleCount[0]}   Удалено: {tupleCount[1]}")
