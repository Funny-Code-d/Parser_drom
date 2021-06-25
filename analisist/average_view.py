import sql_class

sql = sql_class.SQL_request('drom', 'parser_drom', 'parser_drom', 'localhost')

print(sql.select_model())