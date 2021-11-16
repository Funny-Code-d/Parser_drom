from .abstract.abstractClass import AbstractParser
from env.error import ErrorsCodes
from env.tagsParser import tagsForParse
class dromClass(AbstractParser):

    def __init__(self, proxies, header):
        super().__init__(proxies, header)
        self.namePlatform = "drom"
        self.tagsClass = tagsForParse.tags.value[self.namePlatform]


    def getInfoFields(self, url):

        htmlText = self.getHtml(url)

        if htmlText == ErrorsCodes.requestError:
            return ErrorsCodes.requestError

        elif htmlText == ErrorsCodes.deleteAction:
            return ErrorsCodes.deleteAction
        
        fields = htmlText.find_all('a', class_=self.tagsClass['fields'])
        
        returnsList = []

        for item in fields:
            model_car = item.find("span", {"data-ftid":"bull_title"}).get_text(strip=True)
            list_name = model_car.split(',')
            model_car = list_name[0]
            href = item.get("href")
            price = item.find("span", {"data-ftid":"bull_price"}).get_text(strip=True)
            list_price = price.split(' ')
            price = ''
            
            for i in list_price:
                price += i
            price = price.replace(u'\xa0', '')

            returnsList.append({
                "model_car" : model_car,
                "url" : href,
                "price" : price,
            })
        return returnsList
        

    def getInfoPageField(self, url):
        htmlText = self.getHtml(url)

        if htmlText == ErrorsCodes.requestError:
            return ErrorsCodes.requestError

        elif htmlText == ErrorsCodes.deleteAction:
            return ErrorsCodes.deleteAction

        # Проверка что машина не проданна
        try:
            if htmlText.find("span", class_=self.tagsClass['checkSoldCar']):
                return ErrorsCodes.soldThisCar
        except AttributeError:
            pass

        try:
            # Проверка что объявление ещё существует на сайте
            check_delete_page = htmlText.find("h1", class_=self.tagsClass['checkDeletePage']).get_text(strip=True)
            
            if check_delete_page in ErrorsCodes.listCheckDeleteAds.value:
                return ErrorsCodes.deleteAction

            
            number_view = int(htmlText.find("div", class_=self.tagsClass['numberView']).get_text(strip=True))
            #print(number_view)
            date_text = htmlText.find("div", class_=self.tagsClass['datePublication']).get_text(strip=True)
        
        except AttributeError:
            return ErrorsCodes.requestError


        # Извлечение даты из текста
        list_date = date_text.split(' ')
        date_pub = list_date[-1].split('.')
        date_publication = date_pub[2] + '-' + date_pub[1] + '-' + date_pub[0]
        # Словарь с извлечёнными данными
        dict_info = {
            "date_publication" : date_publication,
            "number_view" : number_view,
            "url" : url
        }
        return dict_info

    def createUrl(self, page, minPrice, maxPrice, city):
        link = f"https://{city}.{self.namePlatform}.ru/auto/all/page{page}/?minprice={minPrice}&maxprice={maxPrice}"
        return link

    def __call__(self):
        return 'Объект класса dromClass'
