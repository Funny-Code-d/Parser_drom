from baseClassSql import BaseSql


class ParserSqlInterface(BaseSql):

    def __init__(self, datebase_name, user_name, password_db, host_address):
        super().__init__(datebase_name, user_name, password_db, host_address)

    
    def getCity(self):
        query = "SELECT name_city FROM list_city"

        return self._get_table_from_db(query)

if __name__ == '__main__':
    obj = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
    print(obj.getCity())