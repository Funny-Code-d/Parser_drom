"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys
from env import envParser
from loguru import logger
from database.sqlParserClass import ParserSqlInterface
import datetime


class FirstStep:


    def __init__(self, platform, city):
        self.objectPlatform = envParser.objectPlatform[platform]
        self.namePlatform = platform
        self.city = city
        self.header = envParser.headerUserAgent
        self.proxies = envParser.proxies
        
        self.sqlClient = ParserSqlInterface(
            envParser.databaseSettings['database'], 
            envParser.databaseSettings['user'], 
            envParser.databaseSettings['password'], 
            envParser.databaseSettings['host'])
        
        self.numberPages = 90

        logger.add("logs/" + platform + "_" +  city + "_firstStep" + '.log', format='{time} | {level} | {message}', level="DEBUG", rotation="10 MB", compression='zip')

    def getNowDateSqlFormat(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}"


    def run(self):
        tablePriceRange = self.sqlClient.getPriceRange()
        for priceRangeIndex in range(len(tablePriceRange)):
            
            minPrice = tablePriceRange[priceRangeIndex][0]
            maxPrice = tablePriceRange[priceRangeIndex][1]
            for page in range(self.numberPages):

                link = self.objectPlatform.createUrl(page, minPrice, maxPrice, self.city)
                getData = self.objectPlatform.getInfoFields(link)
                for indexRecord in range(len(getData)):
                    getData[indexRecord]['city'] = self.city
                    getData[indexRecord]['platform'] = self.namePlatform
                    getData[indexRecord]['price_range'] = str(int(minPrice/1000)) + '-' + str(int(maxPrice/1000))
                    getData[indexRecord]['date_getting'] = self.getNowDateSqlFormat()
                    logger.debug(getData[indexRecord])
                self.sqlClient.upSertFirstStep(getData)




if __name__ == '__main__':
    namePlatform = sys.argv[1]
    nameCity = sys.argv[2]
    

    ObjectProgram = FirstStep(namePlatform, nameCity)
    ObjectProgram.run()