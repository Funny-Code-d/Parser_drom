"""
Параметры заруска программы:
    0 - Название платформы
    1 - Название города
"""

import sys
from env import envParser
from loguru import logger
from database.sqlParserClass import ParserSqlInterface

class SecondStep:


    def __init__(self, platform, city):
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
        

        logger.add("logs/" + platform + "_" +  city + '_secondStep' + '.log', format='{time} | {level} | {message}', level="DEBUG", rotation="10 MB", compression='zip')

    @logger.catch
    def run(self):
        countAds = int(self.sqlClient.getCountAdsForOffset(self.city, self.namePlatform))

        for offset in range(0, countAds, self.limitGetRecord):
            tableWithRecords = self.sqlClient.getAdsForSecondStep(self.city, self.namePlatform, offset, self.limitGetRecord)
            for record in tableWithRecords:
                getData = self.objectPlatform.getInfoPageField(record[0])
                # logger.info(getData)
                if isinstance(getData, dict):
                    #logger.info(getData)
                    self.sqlClient.UpdateSecondStep(getData)
                elif getData == "Delete ads":
                    logger.error(f"Delete ads {record[0]}")
                elif getData == 'Attribute error':
                    logger.error(f"Attribute error: {record[0]}")
                else:
                    logger.error(f"Uncnown errors: {record[0]}")


if __name__ == '__main__':
    #nameCity = 'irkutsk'
    #namePlatform = 'drom'
    namePlatform = sys.argv[1]
    nameCity = sys.argv[2]
    obj = SecondStep(namePlatform, nameCity)
    obj.run()
