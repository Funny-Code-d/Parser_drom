import parser_class
import sql_class
import os
from requests.packages import urllib3
import requests
import sys
"""
Программа для сбора данных с сайта drom.ru и записи в базу
Автор: Соснин Д.
Email: sosnin_dienis@mail.ru
GitHub: Funny-Code-d
"""

class Program:
	"""
	Класс работы парсера

	Для запуска необходимо создать экземпляр класса
	и вызвать метод run()
	Параметров для создания экземпляра не требуется
	"""
	def __init__(self):
		self.sql = sql_class.SQL_request("carbuy_db", "carbuy", "carbuy", "localhost")
		self.parser = parser_class.Parser()
		self.city = ['novosibirsk', 'irkutsk']

		self.categories = [[0, 100000], [100000, 200000], [200000, 500000], [500000, 900000], [900000, 1500000], [1500000, 2000000]]

		self.number_pages = 5



	def process_monitoring(self, index, len_index):
		try:
			x = int(index / len_index * 100)
		except ZeroDivisionError:
			x = 0

		if index % 2 == 0:
			print(f"{x}% --- ({index} in {len_index})", end='\r')
		else:
			print(f"{x}% ||| ({index} in {len_index})", end='\r')


	def insert_filed_to_base(self, dict_info_car):
		"""
		Метод для работы со словарём карточек объявлений и записи в базу

		Параметры:
		dict_info_car - словарь с данными
		"""
		# Цикл по карточкам объявлений

		for car in dict_info_car.keys():
			# Извлечение информации о карточке
			ones_field_car = dict_info_car[car]
			# Проверка есть ли такая запись в базе
			check_record = self.sql.check_record_in_db('advertisement', ones_field_car['url'], ones_field_car['model_car'])
			if check_record:
				#Запись есть
				pass
			else:
				# Новая запись
				self.sql.insert_primary_info(ones_field_car['city'], ones_field_car['average_price'], ones_field_car['price'], ones_field_car['url'], ones_field_car['model_car'])
			


	def first_step_parse(self):
		"""
		Метод первичного сбора
		
		Собирает информацию с карточек объявлений и записывает в базу
		(не собирает дату публикации и количество просмотров, это во втором шаге)

		Вызывается без параматеров, работает с переменными класса
		"""
		# Цикл по городам
		index = 0
		len_index = len(self.city) * len(self.categories) * self.number_pages
		for name_city in self.city:
			# Цикл по категориям
			for categor in self.categories:
				# Цикл по страницам
				for page in range(1, self.number_pages + 1):
					# Построение url
					url = "https://" + name_city + ".drom.ru/auto/all/page" + str(page) + "/?minprice=" + str(categor[0]) + "&maxprice=" + str(categor[1])
					# Получение карточек объявлений со станицы
					dict_field_car = self.parser.get_info_fields(url, name_city)

					# Разбор словаря с данными и запись в базу
					self.insert_filed_to_base(dict_field_car)
					#print(dict_field_car)
					# Отображение хода выполенния
					self.process_monitoring(index, len_index)
					index += 1

	def second_step_parse(self):
		"""
		Метод второго шага сбора информации
		Заправшивает страницу каждого объявления из базы и обновляет информаци
		Собирает со страницы дату публикации и количество просмотров

		"""
		# Запрос всех объявлений
		table_all_records = self.sql.select_url(self.city[0])
		index = 0
		len_index = len(table_all_records)
		# Цикл по полученой таблице из запроса
		for ones_publication in table_all_records:
			# Url ссылка на объявление
			url_publication = ones_publication[0]
			print(url_publication)
			# Запрос и сбор информации со страницы
			dict_info_form_page_car = self.parser.get_info_page_field(url_publication)
			
			#print(dict_info_form_page_car)
			# Если объявление удалили
			if dict_info_form_page_car == 'delete':
				self.sql.delete_url(url_publication)
			else:
				self.sql.update_info(dict_info_form_page_car['number_view'], dict_info_form_page_car['date_publication'], dict_info_form_page_car['url'])
			# Отображение хода выполения
			self.process_monitoring(index, len_index)
			index += 1


	def try_second_step_parse(self):
		flag = True
		while flag:
			flag = False
			try:
				self.second_step_parse()
			except (BaseError) as error_atr:
				flag = True
				print(error_atr)
				continue

	def swap(self):
		self.sql.before_update()

	def run(self):
		#self.first_step_parse()
		#self.swap()
		self.second_step_parse()


if __name__ == "__main__":
	p = Program()
	p.run()
	# p = Program(int(sys.argv[1]))
	# if sys.argv[2] == 'first_step':
	# 	p.first_step_parse()
	# elif sys.argv[2] == 'swap':
	# 	p.swap()
	# elif sys.argv[2] == 'second_step':
	# 	p.try_second_step_parse()
	# else:
	# 	print("Undefined problem")
