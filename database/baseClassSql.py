import psycopg2
from abc import ABCMeta


class BaseSql(metaclass=ABCMeta):

    def __init__(self, datebase_name, user_name, password_db, host_address):
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

    def __del__(self):

        """Деструктор, при удалении экземпляра, проиходит отключение от базы"""
		
        self.conn.close()
        print("Close connect to db  ")


    def _get_table_from_db(self, req):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(req, ())
            return_obj = self.cursor.fetchall()
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return return_obj

    def _insert_to_db(self, req):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(req, ())
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)