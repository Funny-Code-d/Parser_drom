# from bs4.element import AttributeValueWithCharsetSubstitution
# import requests
# from bs4 import BeautifulSoup
# import psycopg2
# from psycopg2 import sql
from time import sleep


# connect = psycopg2.connect(dbname ='drom', user='parser_drom',
# 								password = 'parser_drom', host = 'localhost')	
# connect.autocommit = True
# with connect.cursor() as cursor1:
# 	update = """UPDATE advertisement SET date_publication = %s, number_view = %s WHERE url = %s"""
# 	# update = sql.SQL("UPDATE advertisement SET number_view = %s WHERE url = %s")
# 	cursor1.execute(update, ('2021-06-12', 100, 'https://novosibirsk.drom.ru/toyota/tercel/39441271.html'))

import sql_class

SQL_client = sql_class.SQL_request('drom', 'parser_drom', 'parser_drom', 'localhost')

print(help(sql_class))

#sleep(100)


#SQL_client.insert_primary_info('novosibirsk', '0-100', 999999, 'https://', 'TEST_CAR')

#SQL_client.update_info(999999, '2030-03-30', 'https://')

#SQL_client.close_db()