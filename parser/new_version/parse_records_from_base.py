from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from time import sleep

from function_for_parse import *



#------------------------------------------------------------------------------------------------
def get_missing_info(html, href):
	# Получение тегов и классов
	soup = BeautifulSoup(html.text, "html.parser")
	# парс информации
	number_view = int(soup.find("div", class_="css-se5ay5").get_text(strip=True))
	date = soup.find("div", class_="css-61s82p").get_text(strip=True)
	# Извлечение даты
	list_date = date.split(' ')
	date_pub = list_date[-1].split('.')
	date_publication = date_pub[2] + '-' + date_pub[1] + '-' + date_pub[0]
	dict_info = {
	"date_publication" : date_publication,
	"number_view" : number_view,
	"url" : href
	}
	print(dict_info)
	return dict_info
	

def update_records(dict_info):
	number_view1 = dict_info['number_view']
	url = dict_info['url']
	date_public = dict_info['date_publication']


	#with conn.cursor() as cursor_update:
	try:
		cur = conn.cursor()

		update = """UPDATE advertisement SET date_publication = %s, number_view = %s WHERE url = %s"""
		# update = sql.SQL("UPDATE advertisement SET number_view = %s WHERE url = %s")
		cur.execute(update, (date_public, number_view1, url))
		update_row = cur.rowcount
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)



conn = psycopg2.connect(dbname='drom', user='parser_drom', 
                        password='parser_drom', host='localhost')
conn.autocommit = True
with conn.cursor() as cursor:
		
	cursor.execute("SELECT url FROM advertisement")
	select = cursor.fetchall()


	for item in select:
		html = get_html(item[0])
		if html.status_code == 200:
			dict_miss = get_missing_info(html, str(item[0]))
			update_records(dict_miss)
		
			
