import requests

HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
           'accept' : '*/*'}

#-----------------------------------------------------------------------------------------------------------------
# Функция отправки запроса и получения страницы
def get_html(url, params=None):
    proxies = {
    # "https" : "91.227.45.220:8080",
    # "http" : '46.42.16.245:31565',
    "socks4" : "188.235.34.146:1080"
    }
    r = requests.get(url, headers=HEADERS, params=params, proxies=proxies)
    return r