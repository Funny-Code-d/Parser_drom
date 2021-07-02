import psycopg2
from psycopg2 import sql
import datetime

class SQL_request:

	"""
	Класс для работы с базой данных
	** подключение и отключение к базе происходит автоматически
	за счёт контсруктора и деструктора
	
	Параметры при создании экземпляра:
	* database_name - имя базы данных
	* user_name - имя пользователя
	* password_db - пароль от учётной записи пользователя
	* host_address - адрес базы (localhost, IP)

	"""
	def __init__(self, datebase_name, user_name, password_db, host_address):
		
		"""Конструктор, создаётся подключение к базе"""

		self.database_name = datebase_name
		self.user_name = user_name
		self.password_db = password_db
		self.host_address = host_address
		self.conn = None
		self.cursor = None

		# Подключение к базе
		self.conn = psycopg2.connect(dbname=self.database_name, user=self.user_name, 
                        password=self.password_db, host=self.host_address)
		self.conn.autocommit = True
		print("Connect to db  ")
# --------------------------------------------------------------------------------------------------------------
	def __del__(self):

		"""Деструктор, при удалении экземпляра, проиходит отключение от базы"""
		
		self.conn.close()
		print("Close connect to db  ")
# --------------------------------------------------------------------------------------------------------------
	def request_to_db(self, req):
		try:
			self.cursor = self.conn.cursor()
			self.cursor.execute(req, ())
			return_obj = self.cursor.fetchall()
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		return return_obj
# --------------------------------------------------------------------------------------------------------------
	def select_url(self):

		"""Метод для получения таблицы URL адресов

		Параметры: table_name - Имя таблицы

		Возвращает таблицу"""

		self.cursor = self.conn.cursor()
		select = """SELECT url FROM advertisement WHERE number_view[2] = 0"""
		self.cursor.execute(select, ())
		return_list = self.cursor.fetchall()
		self.cursor.close()
		return return_list
# --------------------------------------------------------------------------------------------------------------
	def check_record_in_db(self, table_name, check_url, check_model):

		"""
		Метод для проверки записи на существование в таблице
		Параметры:
		table_name - имя таблицы
		check_url - URL адрес объявления
		check_model - модель машины из объявления

		Возвращает True - если есть, False - если нет
		"""

		self.cursor = self.conn.cursor()
		select = """SELECT url, model FROM advertisement WHERE url = %s AND model = %s"""
		self.cursor.execute(select, (check_url, check_model))

		answer = self.cursor.fetchall()
		self.cursor.close()
		if len(answer) == 0:
			return False
		else:
			return True
# --------------------------------------------------------------------------------------------------------------
	def insert_primary_info(self, city, average_price, price, url, model):

		"""
		Метод для вставки записи в таблицу
		Параметры:
		city - город
		average_price - ценовой диапазон
		price - цена
		url - URL ссылка на объявление
		model - модель машины
		"""

		self.cursor = self.conn.cursor()
		
		insert = """INSERT INTO advertisement (city, price_range, price, url, model, number_view) VALUES (%s, %s, %s, %s, %s, '{ 0, 0 }')"""
		self.cursor.execute(insert, (city, average_price, price, url, model))
		#print(url)
		#print("Запись добавлена")
		self.cursor.close()
# --------------------------------------------------------------------------------------------------------------
	def update_info(self, number_view, date_publication, url):

		"""
		Метод для дополнения информации в запись
		Параметры:
		number_view - количество просмотров объявления
		date_publication - дата публикации (yyyy-mm-dd)
		url - URL ссылка объявления
		"""

		try:
			self.cursor = self.conn.cursor()

			update = """UPDATE advertisement SET date_publication = %s, number_view[2] = %s WHERE url = %s"""
			self.cursor.execute(update, (date_publication, number_view, url))
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error dataBase")
		else:
			# print("Запись обновлена")
			pass
# --------------------------------------------------------------------------------------------------------------
	def delete_url(self, url):
		"""
		Метод для удаления записи из базы

		Параметры:
		url - URL ссылка на объявление
		"""
		try:
			self.cursor = self.conn.cursor()

			delete = """DELETE FROM advertisement WHERE url = %s"""
			self.cursor.execute(delete, (url,))
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error dataBase")
		else:
			#print("Запись удалена")
			pass
# --------------------------------------------------------------------------------------------------------------
	def before_update(self):
		"""
		Метод для обработки таблицы

		Изменяется массив number_view: на первое место ставиться старое количество просмотров,
		на второе место ставиться ноль.

		**Использую для выявления где остановилась программа в случае ошибки
		"""
		zero = """UPDATE advertisement SET number_view[1] = number_view[2], number_view[2] = 0"""
		try:
			self.cursor = self.conn.cursor()

			self.cursor.execute(zero, ())
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error db")
			print(error)
		else:
			#print("База обновлена")
			pass
# --------------------------------------------------------------------------------------------------------------
	def overflow_test(self):
		"""
		Метод для чистки базы, допускается до 300 объявлений по каждой марке
		При переполнении удаляются объявления с самой давней датой публикации
		"""
		get_table_model = """
		SELECT model, count(*) FROM advertisement
		GROUP BY model ORDER BY count DESC
		"""

		try:
			self.cursor = self.conn.cursor()

			self.cursor.execute(get_table_model, ())
			return_dict = self.cursor.fetchall()
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error")
		
		for item in return_dict:
			model = item[0]
			number_pub = item[1]

			if number_pub > 300:
				pub_requests = """SELECT url, model, date_publication FROM advertisement WHERE model = %s ORDER BY date_publication"""
				self.cursor = self.conn.cursor()
				self.cursor.execute(pub_requests, (model, ))
				table_pub = self.cursor.fetchall()
				self.cursor.close()
				range_del = len(table_pub) - 300
				for i in range(range_del):
					self.delete_url(table_pub[i][0])
# --------------------------------------------------------------------------------------------------------------

	def select_model(self):

		select = f"""SELECT model, count(*) FROM advertisement GROUP BY model ORDER BY count"""
		return self.request_to_db(select)

	def select_for_analysis(self, model):

		select = '''SELECT date_publication, number_view FROM advertisement WHERE model = %s'''
		try:
			self.cursor = self.conn.cursor()
			self.cursor.execute(select, (model, ))
			return self.cursor.fetchall()
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def insert_after_analisis(self, table, place, model, average_price):
		now = datetime.datetime.now()
		day = now.day
		month = now.month
		year = now.year
		date = f"{year}-{month}-{day}"
		
		insert = f"""INSERT INTO {table} (date_rating, place, average_view, model) VALUES ({date}, {place}, {average_price}, {model})"""
		self.request_to_db(insert)
#-----------------------------------------------------------------------------------------------------------------------
	def select_for_telegram(self, start):
		pass


