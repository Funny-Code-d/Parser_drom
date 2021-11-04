"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys
import env.envParser as envImports
from loguru import logger
from database.sqlParserClass import ParserSqlInterface



class Program:


    def __init__(self, platform, city):
        self.objectPlatform = envImports.objectPlatform[platform]
        self.namePlatform = platform
        self.city = city
        self.header = envImports.headerUserAgent
        self.proxies = envImports.proxies
        
        self.sqlClient = ParserSqlInterface(
            envImports.databaseSettings['database'], 
            envImports.databaseSettings['user'], 
            envImports.databaseSettings['password'], 
            envImports.databaseSettings['host'])
        
        self.numberPages = 90

        logger.add("logs/" + platform + "_" +  city + '.log', format='{time} | {level} | {message}', level="DEBUG", rotation="10 MB", compression='zip')


    
    def createUrl(self, page, minPrice, maxPrice):
        link = f"https://{self.city}.{self.namePlatform}.ru/auto/all/page{page}/?minprice={minPrice}&maxprice={maxPrice}"
        return link


    def run(self):
        tablePriceRange = self.sqlClient.getPriceRange()
        for priceRangeIndex in range(len(tablePriceRange)):
            
            minPrice = tablePriceRange[priceRangeIndex][0]
            maxPrice = tablePriceRange[priceRangeIndex][1]
            for page in range(self.numberPages):

                link = self.createUrl(page, minPrice, maxPrice)
                getData = self.objectPlatform.getInfoFields(link)
                for indexRecord in range(len(getData)):
                    getData[indexRecord]['city'] = self.city
                    getData[indexRecord]['platform'] = self.namePlatform
                    getData[indexRecord]['price_range'] = str(int(minPrice/1000)) + '-' + str(int(maxPrice/1000))
                self.sqlClient.upSertFirstStep(getData)










if __name__ == '__main__':
    #namePlatform = sys.argv[0]
    #nameCity = sys.argv[1]
    namePlatform = 'drom'
    nameCity = 'novosibirsk'

    ObjectProgram = Program(namePlatform, nameCity)
    ObjectProgram.run()