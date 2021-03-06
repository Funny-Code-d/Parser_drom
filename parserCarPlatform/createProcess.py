from database.sqlParserClass import ParserSqlInterface
# import ..env.envParser as envImports
from env.envParser import objectPlatform, databaseSettings
import os
import loguru



class Creator:

    def __init__(self, step):
        self.listPlatrform = objectPlatform.keys()

        self.sqlClient = ParserSqlInterface(
            databaseSettings['database'],
            databaseSettings['user'],
            databaseSettings['password'],
            databaseSettings['host']
        )
        self.cityNames = self.sqlClient.getCity()
        loguru.logger.add("logs/Report.log", format='{time} | {level} | {message}', level="DEBUG", rotation="2 MB", compression='zip')

        self.typeStep = step
        self.error = False
        if step not in ('first', 'second'):
            self.error = True





    def run(self):
        if self.error:
            loguru.logger.error("Программа завершена с ошибкой, неверные параметры запуска. Допустимые значения: first, second")
            exit()
        for platform in self.listPlatrform:
            for city in self.cityNames:
                if self.typeStep == 'first':
                    os.system(f"python3 firstStepParser.py {platform} {city} &")
                else:
                    os.system(f"python3 secondStepParser.py {platform} {city} &")
        
        if self.typeStep == 'first':
            loguru.logger.info(f"Запущен первый этап сбора информации")
        else:
            loguru.logger.info(f"Запущен второй этап сбора информации")