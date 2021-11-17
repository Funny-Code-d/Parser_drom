"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys

from requests.api import get
from env.error import ErrorsCodes
from env import envParser, error
from loguru import logger
from database.sqlParserClass import ParserSqlInterface

class SecondStep:


    def __init__(self, platform, city):

        self.countUpdateRecords = 0
        self.countDeleteRecords = 0

        self.objectPlatform = envParser.objectPlatform[platform]
        self.namePlatform = platform
        self.city = city
        self.header = envParser.headerUserAgent
        self.proxies = envParser.proxies
        self.limitGetRecord = 100
        self.sqlClient = ParserSqlInterface(
            envParser.databaseSettings['database'], 
            envParser.databaseSettings['user'], 
            envParser.databaseSettings['password'], 
            envParser.databaseSettings['host'])
        

        logger.add("logs/" + platform + "_" +  city + '_secondStep' + '.log', format='{time} | {level} | {message}', rotation="10 MB", compression='zip', level='INFO')


    def switchUpdateStatusRecords(self):
        self.sqlClient.updateStatusToFalse(self.namePlatform, self.city)


    @logger.catch
    def run(self):

        tableWithRecords = self.sqlClient.getAdsForSecondStep(self.city, self.namePlatform, self.limitGetRecord)
        for record in tableWithRecords:
            getData = self.objectPlatform.getInfoPageField(record[0])
            

            # Объявление удалено (ошибка 404)
            if getData['errors'] == error.ErrorsCodes.deleteAction:
                self.countDeleteRecords += 1
                logger.debug(f"Объявление удалено: {record[0]}")
                self.sqlClient.moveToOldAds(record[0])
            
            else:
                # Ошибка запроса (будет проверенно повторно)
                if getData['errors'] == error.ErrorsCodes.requestError:
                    logger.error(f"Request errror {record[0]}")
                    continue
                
                logger.debug(f"Обновленно: {record[0]}")
                self.sqlClient.UpdateSecondStep(getData)
                
                # Машина проданна
                
                if getData['errors'] == error.ErrorsCodes.soldThisCar:
                    self.countDeleteRecords += 1
                    logger.debug(f"Машина продана: {record[0]}")
                    self.sqlClient.moveToOldAds(record[0])
        
        ostRecords = int(self.sqlClient.getCountAdsForOffset(self.city, self.namePlatform))
        logger.info(f'RUN --- {self.city} {self.namePlatform} --- Осталось записей: {ostRecords}')
        if ostRecords > 0:
            return self.run()
        else:
            logger.success(f"END --- {self.city} {self.namePlatform} --- Обновленно: {self.countUpdateRecords}, Удалено {self.countDeleteRecords}")
            return None


if __name__ == '__main__':
    #nameCity = 'irkutsk'
    #namePlatform = 'drom'
    namePlatform = sys.argv[1]
    nameCity = sys.argv[2]
    obj = SecondStep(namePlatform, nameCity)
    obj.switchUpdateStatusRecords()
    obj.run()
