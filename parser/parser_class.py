import requests
class Parser:
	"""
	Класс для сбора информации с сайта Drom.ru
	Сбор информации происходит по городам и ценовым диапазонам
	Количество ценовых диапазонов = 6
	-------------------------------------------------
	Пример:
		Количество городов = 3
		Количество страниц для каждой категории = 10
		Количество объявлений на странице = 20

		Парсер выдаст 3600 объявлений
	--------------------------------------------------


	Парамеры при создании экземпляра:
	city - город(а) для сбора информации (можно передать как строку, так и список)
	number_pages - количество страниц сбора информации в каждой категории
	"""
	def __init__(self, city, number_pages):
		self.HEADER = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0', 'accept' : '*/*'}
		self.categories = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
		self.city = city
		self.number_pages = number_pages
		self.url = 'https://auto.drom.ru/all/'

	def get_url(self, page, min_price, max_price):
		"""Метод для формирования правильного URL (с учётом номера страницы и ценового диапазона)

		Параметры:
		page - Номер страницы
		min_price - Минимальная цена
		max_price - Максимальная цена

		Возвращает URL ссылку
		"""
		final_url = self.url + 'page' + page + '/?minprice=' + min_price + '&maxprice=' + max_price
		return final_url

	def get_html(self, page, min_price, max_price, params=None):
		"""
		Метод для отправки запроса на получение страницы
		Возвращает html страницу
		"""
		r = requests.get(get_url(page, min_price, max_price), headers=HEADERS, param=params)
		return r
        