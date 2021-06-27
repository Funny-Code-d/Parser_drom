import sql_class
from time import sleep
import datetime
import pandas as pd

sql = sql_class.SQL_request('drom', 'parser_drom', 'parser_drom', '192.168.0.200')
table_model = sql.select_model()
now = datetime.datetime.now()
rating = {}
for item in table_model:
	model = item[0]
	number_pub = item[1]

	average_view = 0

	table_for_analysis = sql.select_for_analysis(model)
	number_pub_model = len(table_for_analysis)
	for publication in table_for_analysis:
		# Вычисление количества дней с даты публикации
		day = publication[0].day
		month = publication[0].month
		year = publication[0].year
		date_pub = datetime.datetime(year, month, day)
		per_day = (now - date_pub).days
		#----------------------------------------------
		try:
			view = publication[1][1] / per_day
		except ZeroDivisionError:
			view = publication[1][1]
		average_view += view
	average_view /= number_pub_model
	rating[model] = average_view
df = pd.DataFrame(rating.values(), index = rating.keys(), columns=['Average view'])
rating = df.sort_values(['Average view'], ascending=[False])
for car in rating:
	print(car)