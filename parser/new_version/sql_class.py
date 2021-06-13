import psycopg2
from psycopg2 import sql


class SQL_request:

	def __init__(self):
		self.conn = None
		self.cursor = None

# --------------------------------------------------------------------------------------------------------------
	# Функция для подключения к базе
	def connect_db(self):
		self.conn = psycopg2.connect(dbname='drom', user='parser_drom', 
                        password='parser_drom', host='localhost')
		self.conn.autocommit = True
		print("Connect to db")
# --------------------------------------------------------------------------------------------------------------
	# Функция для отключения от базы
	def close_db(self):
		self.conn.close()
		print("Close connect to db")
# --------------------------------------------------------------------------------------------------------------
	# Функция для получения из базы url адресов для дополнения информацией
	def select_url(self):
		self.cursor = self.conn.cursor()
		select = """SELECT url FROM advertisement"""
		self.cursor.execute(select)
		return_list = self.cursor.fetchall()
		self.cursor.close()
		return return_list
# --------------------------------------------------------------------------------------------------------------
	# Функция для проверки записи на существование в базе
	def check_record_in_db(self, check_url, check_model):
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
	# Функция вставки первичной информации
	def insert_primary_info(self, city, average_price, price, url, model):
		self.cursor = self.conn.cursor()
		
		insert = """INSERT INTO advertisement (city, price_range, price, url, model) VALUES (%s, %s, %s, %s, %s)"""
		self.cursor.execute(insert, (city, average_price, price, url, model))
		print("Запись добавлена")
		self.cursor.close()
# --------------------------------------------------------------------------------------------------------------
	def update_info(self, number_view, date_publication, url):
		try:
			self.cursor = self.conn.cursor()

			update = """UPDATE advertisement SET date_publication = %s, number_view = %s WHERE url = %s"""
			self.cursor.execute(update, (date_publication, number_view, url))
			self.cursor.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("Error dataBase")
		else:
			print("Запись обновлена")