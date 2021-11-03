from baseClassSql import BaseSql


class TelegramSqlInterface(BaseSql):

    def __init__(self, datebase_name, user_name, password_db, host_address):
        super().__init__(datebase_name, user_name, password_db, host_address)