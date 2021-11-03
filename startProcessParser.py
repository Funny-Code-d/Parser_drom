# from database.sqlParserClass import ParserSqlInterface
# import env.envParser as envImports
# import os
# import logging

# class Creator:

#     def __init__(self):
#         self.listPlatrform = envImports.objectPlatform.keys()
#         #print(self.listPlatrform)
#         self.sqlClient = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
#         self.cityNames = self.sqlClient.getCity()
#         self.logger = logging.getLogger("testLog.log")



#     def run(self):
#         for platform in self.listPlatrform:
#             for city in self.cityNames:
#                 # os.system(f"python3 startParserPlatform.py {platform} {city}")
#                 self.logger.warning(f"Запущен процесс {platform} {city}")

import database

obj = database.sqlParserClass('carbuy_db', 'carbuy', 'carbuy', 'localhost')