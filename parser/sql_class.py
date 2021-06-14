import psycopg2
from psycopg2 import sql


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
		print("Connect to db")
# --------------------------------------------------------------------------------------------------------------
	def __del__(self):

		"""Деструктор, при удалении экземпляра, проиходит отключение от базы"""
		
		self.conn.close()
		print("Close connect to db")
# --------------------------------------------------------------------------------------------------------------
	def select_url(self, table_name):

		"""Метод для получения таблицы URL адресов

		Параметры: table_name - Имя таблицы

		Возвращает таблицу"""

		self.cursor = self.conn.cursor()
		select = """SELECT url FROM %s"""
		self.cursor.execute(select, (table_name, ))
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
		select = """SELECT url, model FROM %s WHERE url = %s AND model = %s"""
		self.cursor.execute(select, (table_name, check_url, check_model))

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
		
		insert = """INSERT INTO advertisement (city, price_range, price, url, model) VALUES (%s, %s, %s, %s, %s)"""
		self.cursor.execute(insert, (city, average_price, price, url, model))
		print("Запись добавлена")
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

			update = """UPDATE advertisement SET date_publication = %s, number_view = %s WHERE url = %s"""
			self.cursor.execute(update, (date_publication, number_view, url))
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error dataBase")
		else:
			print("Запись обновлена")