from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from time import sleep


connect = psycopg2.connect(dbname ='drom', user='parser_drom',
								password = 'parser_drom', host = 'localhost')	
connect.autocommit = True
with connect.cursor() as cursor1:
	update = """UPDATE advertisement SET date_publication = %s, number_view = %s WHERE url = %s"""
	# update = sql.SQL("UPDATE advertisement SET number_view = %s WHERE url = %s")
	cursor1.execute(update, ('2021-06-12', 100, 'https://novosibirsk.drom.ru/toyota/tercel/39441271.html'))