import parser_class
import sql_class
from time import sleep
import datetime
# Создание объектов
parser = parser_class.Parser()
sql = sql_class.SQL_request("drom", "parser_drom", "parser_drom", "localhost")
#sql.before_update()
# Запрос на получение всех url адресов из таблицы
table = sql.select_url()
# Отображения процесса
all_ = len(table)
ones_persent = all_ / 100
process = 0
process_index = 0
process_index_print = 0
# Парс каждого объявления по отдельноси
for item in table:
	#print(item[0])
	dict_info = parser.get_info_page_field(item[0])

	# Если страница не существует (Ошибка 404)
	if dict_info == "delete":
		sql.delete_url(item[0])
	else:

		sql.update_info(dict_info['number_view'], dict_info['date_publication'], dict_info['url'])

	#print("Осталось {} объявлений".format(process))
	process_index += 1
	process_index_print += 1
	if process_index >= ones_persent:
		process += 1
		process_index = 0

	if process_index_print % 2 == 0:
		print("{} % --- ({} in {})".format(process, process_index_print, all_), end='\r')
	elif process_index_print % 2 == 1:
		print("{} % ||| ({} in {})".format(process, process_index_print, all_), end='\r')

