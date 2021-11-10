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
        self.typeStep = step
        self.error = False
        if step == 'first':
            loguru.logger.add("logs/Create_process_firstStep.log", format='{time} | {level} | {message}')
        elif step == 'second':
            loguru.logger.add("logs/Create_process_firstStep.log", format='{time} | {level} | {message}')
        else:
            self.error = True





    def run(self):
        if self.error:
            loguru.logger.error("Программа завершена с ошибкой, неверные параметры запуска. Допустимые значения: first, second")
            exit()
        for platform in self.listPlatrform:
            for city in self.cityNames:
                print(os.system("pwd"))
                if self.typeStep == 'first':
                    os.system(f"python3 firstStepParser.py {platform} {city} &")
                    loguru.logger.warning(f"Запущен процесс обновления данных по объявлениям платформы {platform}, города {city}")
                else:
                    os.system(f"python3 secondStepParser.py {platform} {city} &")
                    loguru.logger.warning(f"Запущен процесс парсинга платформы {platform}, города {city}")