import sql_class
import datetime
import pandas
from time import sleep
class Analysis:

	def __init__(self):
		self.sql = sql_class.SQL_request("drom", "parser_drom", "parser_drom", "192.168.0.200")


	def run_analysis(self, table, name_table_for_insert):
		cars = {}
		number_pub_car = {}
		# Цикл по таблице из базы
		for item in table:
			# Если марка уже есть в словаре
			if item[0] in cars.keys():
				car[item[0]] += int(item[1])
				number_pub_car[item[0]] += 1
			# Если такой марки в словаре ещё нет
			else:
				cars[item[0]] = int(item[1])
				number_pub_car[item[0]] = 1
		# Вычисление среднего количества просмотров по каждой модели
		for item in cars.keys():
			cars[item] /= int(number_pub_car[item])
		# Создание DataFrame
		df = pandas.DataFrame({'Model': cars.keys(), 'Average view':cars.values()}, index = cars.keys())
		# Сортировка по поличеству просмотров на убывание
		rating = df.sort_values(['Average view'], ascending=[False])
		place = 1
		# Вставка/изменение записи в базе
		for index, number in rating.iterrows():
			self.sql.insert_after_analisis(name_table_for_insert, place, number["Model"], number["Average view"])



	def time_laps_analysis(self):
		name_table = [
			'analysis_one_week',
			'analysis_two_week',
			'analysis_one_month',
			'analysis_six_month',
			'analysis_twelve_month'
			]
		today = datetime.datetime.now()
		range_time = [
			today - datetime.timedelta(days = 7),
			today - datetime.timedelta(days = 14),
			today - datetime.timedelta(days = 30),
			today - datetime.timedelta(days = 182),
			today - datetime.timedelta(days = 365)
			]
		for item in range(len(range_time)):
			select = f"SELECT model, average_view FROM rating WHERE date_rating > '{range_time[item].year}-{range_time[item].month}-{range_time[item].day}'"
			table = self.sql.request_to_db(select)
			self.run_analysis(tablem name_table[time])

if __name__ == "__main__":
	a = Analysis()
	a.time_laps_analysis()