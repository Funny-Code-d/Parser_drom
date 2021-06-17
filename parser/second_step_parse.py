import parser_class
import sql_class
from time import sleep
# Создание объектов
parser = parser_class.Parser()
sql = sql_class.SQL_request("drom", "parser_drom", "parser_drom", "localhost")
# Запрос на получение всех url адресов из таблицы
table = sql.select_url()
# Парс каждого объявления по отдельноси
for item in table:
	dict_info = parser.get_info_page_field(item[0])
	print(item[0])
	sql.update_info(dict_info['number_view'], dict_info['date_publication'], dict_info['url'])
	sleep(1)
