from abc import ABCMeta, abstractmethod
from requests.packages import urllib3
from requests import get as getRequests
from bs4 import BeautifulSoup
from env.error import ErrorsCodes


class AbstractParser(metaclass=ABCMeta):

    """
    Абстрактный класс для наследования и создания парсера под конкретную платформу

    Имеет следующие методы:

    * getHtml() - метод для отправки запроса и получения html-кода для извлечения информации (не нужно переопределять)
    * getInfoFields() - метод для получения информации со страницы списка объявлений (Необходимо переопределить и написать свою логику извлечения ифнормации)
    * getInfoPageField() - метод для получения информации со страницы конкретного объявления (Необходимо переопредеить)
    """
    def __init__(self, proxies, header):
        self.proxies = proxies
        self.header = header


    def getHtml(self, url):
        """
        Метод отправки GET запроса и в случае успеха (status_code: 200) возвращает html-код страницы

        Параметры:
        * url (string) - Ссылка на страницу
        * proxies (dict) - Словарь прокси серворов (не обязательно)
        * params - Прочие параметры для функции get модуля requests (не обязательно)
        * header (dict) - Словарь user-agent broweser


        returns: string/None
        """

        urllib3.disable_warnings()
        
        r = getRequests(url, headers=self.header, params=None, proxies=self.proxies, verify=False)
        if r.status_code == ErrorsCodes.requestOk.value:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup
        elif r.status_code == ErrorsCodes.notFound.value:
            return ErrorsCodes.deleteAction
        
        else:
            return ErrorsCodes.requestError
    


    @abstractmethod
    def getInfoListCar(self):
        pass


    @abstractmethod
    def getInfoPageCar(self):
        pass

    @abstractmethod
    def createUrl(self, page, minPrice, maxPrice, city):
        pass