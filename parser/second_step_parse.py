import parser_class
import sql_class
from time import sleep
import datetime
# Создание объектов
parser = parser_class.Parser()
sql = sql_class.SQL_request("drom", "parser_drom", "parser_drom", "localhost")
# Запрос на получение всех url адресов из таблицы
table = sql.select_url()
# Парс каждого объявления по отдельноси
for item in table:
	print(item[0])
	dict_info = parser.get_info_page_field(item[0])
	
	# Если страница не существует (Ошибка 404)
	if dict_info == "delete":
		sql.delete_url(item[0])
	else:
		start = datetime.datetime.now()
		sql.update_info(dict_info['number_view'], dict_info['date_publication'], dict_info['url'])
		end = datetime.datetime.now()
		diff = end - start
		print("Время запроса: {}.{}с".format(diff.seconds, diff.microseconds))
