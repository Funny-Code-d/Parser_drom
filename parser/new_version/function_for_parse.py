import requests

HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
           'accept' : '*/*'}

#-----------------------------------------------------------------------------------------------------------------
# Функция отправки запроса и получения страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r