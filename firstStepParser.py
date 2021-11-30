"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys
from env import envParser
from env.error import ErrorsCodes
from loguru import logger
from database.sqlParserClass import ParserSqlInterface
#from telegram.webhooks import filtersNewRecords
import datetime
from time import sleep

class FirstStep:


    def __init__(self, platform, city):
        self.objectPlatform = envParser.objectPlatform[platform]
        self.namePlatform = platform
        self.city = city
        self.header = envParser.headerUserAgent
        self.proxies = envParser.proxies
        self.firstTable = 'notice_of_publication'
        self.secondTable = 'ads'
        #self.webhook = filtersNewRecords()
        self.sqlClient = ParserSqlInterface(
            envParser.databaseSettings['database'], 
            envParser.databaseSettings['user'], 
            envParser.databaseSettings['password'], 
            envParser.databaseSettings['host'])
        
        self.numberPages = 30

        logger.add("logs/Create_process.log", format='{time} | {level} | {message}', level="DEBUG", rotation="10 MB", compression='zip')



    # Функция проверки объявлений для рассылки и перемещение в главную таблицу
    def webhookFilterAndMoveToAds(self):
        
        newRecord = self.sqlClient.getNewRecord(self.city, self.namePlatform, self.firstTable)
        # filtersUsers = self.sqlClient.getFiltersUsers()
        for record in newRecord:
            getData = self.objectPlatform.getInfoPageCar(record['url'])
            getData['url'] = record['url']
            if getData['errors'] == ErrorsCodes.requestError:
                    continue
            if getData['errors'] == ErrorsCodes.deleteAction:
                self.sqlClient.deleteRecord(self.firstTable, getData)
                continue

            getData['update_status'] = True
            self.sqlClient.updateRecord(getData, self.firstTable)
            # self.webhook.filter(record, filtersUsers)
            self.sqlClient.moveToAds(record, self.firstTable, self.secondTable)
        
        countOst = self.sqlClient.getCountAdsForOffset(self.city, self.namePlatform, self.firstTable)
        
        if countOst > 0:
            return self.webhookFilterAndMoveToAds()


    # Функция сбора информации с сайта  
    def collectData(self):
        tablePriceRange = self.sqlClient.getPriceRange()
        for priceRangeIndex in range(len(tablePriceRange)):
            
            minPrice = tablePriceRange[priceRangeIndex][0]
            maxPrice = tablePriceRange[priceRangeIndex][1]
            for page in range(self.numberPages):

                link = self.objectPlatform.createUrl(page, minPrice, maxPrice, self.city)
                getData = self.objectPlatform.getInfoListCar(link)
                

                if not isinstance(getData, list):
                    logger.error("Error first step, getData not is list")
                    continue
                
                for indexRecord in range(len(getData)):
                    getData[indexRecord]['city'] = self.city
                    getData[indexRecord]['platform'] = self.namePlatform
                    getData[indexRecord]['price_range'] = str(int(minPrice/1000)) + '-' + str(int(maxPrice/1000))
                    getData[indexRecord]['date_getting'] = self.sqlClient.getNowDateSqlFormat()
                    getData[indexRecord]['update_status'] = False
                    
                self.sqlClient.insertRecordSkipConflict(getData, self.firstTable)




    @logger.catch
    def run(self):

        # Сбор информации с сайта
        self.collectData()
        # Количество собранных новых объявлений
        countNewAds = self.sqlClient.getCountNewAds(self.namePlatform, self.city)
        # Фильтр webhooks и перемещение в таблицу ads
        self.webhookFilterAndMoveToAds()
        # запись в лог файл
        logger.info(f"Первый этап завершён: | {self.city} | {self.namePlatform} | {countNewAds} новых объявлений")
        



if __name__ == '__main__':
    namePlatform = sys.argv[1]
    nameCity = sys.argv[2]
    

    ObjectProgram = FirstStep(namePlatform, nameCity)
    
    ObjectProgram.run()