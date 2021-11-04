from database.sqlParserClass import ParserSqlInterface
import env.envParser as envImports
import os
import loguru

class Creator:

    def __init__(self):
        self.listPlatrform = envImports.objectPlatform.keys()
        #print(self.listPlatrform)
        self.sqlClient = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
        self.cityNames = self.sqlClient.getCity()
        loguru.logger.add("logs/Create_process.log", format='{time} | {level} | {message}')




    def run(self):
        for platform in self.listPlatrform:
            for city in self.cityNames:
                # os.system(f"python3 startParserPlatform.py {platform} {city}")
                loguru.logger.error(f"Запущен процесс парсинга платформы {platform}, города {city}")


