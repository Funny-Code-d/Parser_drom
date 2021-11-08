print('test1')
from database.sqlParserClass import ParserSqlInterface
# import ..env.envParser as envImports
from env.envParser import objectPlatform
import os
import loguru

class Creator:

    def __init__(self):
        self.listPlatrform = objectPlatform.keys()
        #print(self.listPlatrform)
        self.sqlClient = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
        self.cityNames = self.sqlClient.getCity()
        loguru.logger.add("logs/Create_process.log", format='{time} | {level} | {message}')




    def run(self):
        for platform in self.listPlatrform:
            for city in self.cityNames:
                print(os.system("pwd"))
                os.system(f"python3 firstStepParser.py {platform} {city} &")
                loguru.logger.warning(f"Запущен процесс парсинга платформы {platform}, города {city}")


