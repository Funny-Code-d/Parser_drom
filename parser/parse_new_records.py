from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from time import sleep


from function_for_parse import *
#-----------------------------------------------------------------------------------------------------------------
conn = psycopg2.connect(dbname='drom', user='parser_drom', 
                        password='parser_drom', host='localhost')


#-----------------------------------------------------------------------------------------------------------------
# Функция для извлечения информации с карточки машины
def get_info_from_field(field, city):
	name = field.find("span", {"data-ftid":"bull_title"}).get_text(strip=True)
	list_name = name.split(',')
	name = list_name[0]
	href = field.get("href")
	price = field.find("span", {"data-ftid":"bull_price"}).get_text(strip=True)
	list_price = price.split(' ')
	price = ''
	for i in list_price:
		price += i
	if 0 < int(price) <= 100000:
		average_price = '0-100'
	elif 100000 < int(price) <= 200000:
		average_price = '100-200'
	elif 200000 < int(price) <= 500000:
		average_price = '200-500'
	elif 500000 < int(price) <= 900000:
		average_price = '500-900'
	elif 900000 < int(price) <= 1500000:
		average_price = '900-1500'
	elif 1500000 < int(price) <= 2000000:
		average_price = '1500-2000'


	dict_info = {
	"name_car" : name,
	"href" : href,
	"price" : price,
	"average_price" : average_price,
	"city" : city
	}

	return dict_info


#-----------------------------------------------------------------------------------------------------------------
# Фкнция для получения информации со страницы (с каждой карточки информация проверяется отдельно)
def get_field_pages(html, city):
	soup = BeautifulSoup(html, "html.parser")

	items = soup.find_all('a', class_='ewrty960')
	with conn.cursor() as cursor:
		conn.autocommit = True

		for item in items:
			
			# Вызов функции для получения информации из таблички (Одной)
			dict_info = get_info_from_field(item, city)

			select = sql.SQL("SELECT url, model FROM advertisement WHERE url = %s AND model = %s")
			cursor.execute(select, (dict_info['href'], dict_info['name_car']))
			# Запись полученной таблицы в переменную
			list_from_select = cursor.fetchall()
			print(list_from_select)

			# Если такой записи нет в базе
			if  len(list_from_select) == 0:
				print("New record is write")
				insert = sql.SQL("INSERT INTO advertisement (city, price_range, price, url, model) VALUES (%s, %s, %s, %s, %s)")
				cursor.execute(insert, (dict_info['city'], dict_info['average_price'], dict_info['price'], dict_info['href'], dict_info['name_car']))
			# Иначе если есть
			else:
				print("Запись есть")
			# #insert = sql.SQL("INSERT INTO advertisement (city, price_range, price, url, model) VALUES (%s, %s, %s, %s, %s)")
			#cursor.execute(insert, (city, average_price, price, href, name,))


#-----------------------------------------------------------------------------------------------------------------
# Функция для парса по городу и ценовому диапазону
def parse(number_page, city, categories):
	for  page in range(1, number_page + 1):
		html = get_html()
		if html.status_code == 200:
			get_field_pages(html.text, city)

#-----------------------------------------------------------------------------------------------------------------
# функция для общего парса
def main(city_n):
	for city in city_n:
		categories = [ [0, 100000], [100000, 200000], [200000, 500000], [500000, 900000], [900000, 1500000], [1500000, 2000000] ]

		for categ in categories:
			parse(10, city, categ)



#--------------------------------------------MAIN-----------------------------------------------------------------
if __name__ == "__main__":
	ciry_name = ['novosibirsk', 'irkutsk', 'moscow', 'spb']
	main(ciry_name)
	conn.close()
