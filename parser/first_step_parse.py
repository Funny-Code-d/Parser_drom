import parser_class
import sql_class
parser = parser_class.Parser()
sql = sql_class.SQL_request("drom", "parser_drom", "parser_drom", "localhost")
city = ['novosibirsk', 'irkutsk', 'moscow', 'spb']
categories = [[0, 100000], [100000, 200000], [200000, 500000], [500000, 900000], [900000, 1500000], [1500000, 2000000]]

for c in city:
	for categ in categories:
		print("Город: {}\tКатегория {}-{}".format(c, categ[0], categ[1]))
		for page in range(1, 50):
			url = "https://" + c + ".drom.ru/auto/all/page" + str(page) + "/?minprice=" + str(categ[0]) + "&maxprice=" + str(categ[1])
			dict_car = parser.get_info_fields(url, c)
			for car in dict_car.keys():
				ones_ob = dict_car[car]
				check_record = sql.check_record_in_db('advertisement', ones_ob['url'], ones_ob['model_car'])
				if check_record:
					#Запись есть
					print("Запись существует")
				else:
					# Новая запись
					sql.insert_primary_info(ones_ob['city'], ones_ob['average_price'], ones_ob['price'], ones_ob['url'], ones_ob['model_car'])

