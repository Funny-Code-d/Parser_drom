from .abstractClassPlatform import AbstractParser
from env.error import ErrorsCodes
from env.tagsParser import tagsForParse
from time import sleep


class dromClass(AbstractParser):

    def __init__(self, proxies, header):
        super().__init__(proxies, header)
        self.namePlatform = "drom"
        self.tagsClass = tagsForParse.tags.value[self.namePlatform]

    def getInfoFromHtml(self, textForExtract, tag, classTag):
        try:
            if isinstance(classTag, dict):
                data = textForExtract.find(tag, classTag).get_text(strip=True)
            elif isinstance(classTag, str):
                data = textForExtract.find(tag, class_=classTag).get_text(strip=True)
        except AttributeError:
            return None
        else:
            return data 
    
    def getInfoTable(self, line):
        try:
            key = line.find(self.tagsClass['keyTable']['tag']).get_text(strip=True)
            value = line.find(self.tagsClass['valueTable']['tag']).get_text(strip=True)
        except AttributeError:
            return None, None

        if key == 'Двигатель':
            return 'motor', value
        elif key == 'Мощность':
            return 'motorPower', value
        elif key == 'Трансмиссия':
            return 'transmission', value
        elif key == 'Привод':
            return 'drive', value
        elif key == 'Цвет':
            return 'color', value
        elif key == 'Пробег':
            return 'mileage', value
        elif key == 'Руль':
            return 'wheel', value
        elif key == 'Тип кузова':
            return 'bodyType', value
        elif key == 'Поколение':
            return 'generation', value
        else:
            return None, value

    def getInfoListCar(self, url):

        htmlText = self.getHtml(url)

        if htmlText == ErrorsCodes.requestError:
            return ErrorsCodes.requestError

        elif htmlText == ErrorsCodes.deleteAction:
            return ErrorsCodes.deleteAction
        
        fields = htmlText.find_all(self.tagsClass['fields']['tag'], class_=self.tagsClass['fields']['class'])
        
        returnsList = []

        for item in fields:
            # model_car = self.getInfoFromHtml(item, "span", self.tagsClass['modelCar'])
            model_car = self.getInfoFromHtml(item, self.tagsClass['modelCar']['tag'], self.tagsClass['modelCar']['class'])
            list_name = model_car.split(',')
            model_car = list_name[0]
            yearsCar = list_name[1]
            href = item.get("href")
            price = self.getInfoFromHtml(item, self.tagsClass['price']['tag'], self.tagsClass['price']['class'])
            list_price = price.split(' ')
            price = ''
            
            for i in list_price:
                price += i
            price = price.replace(u'\xa0', '')

            returnsList.append({
                "model_car" : model_car,
                "url" : href,
                "price" : price,
                'years_car' : yearsCar
            })
        return returnsList
        

    def getInfoPageCar(self, url):
        dict_info = dict()
        dict_info['errors'] = None
        htmlText = self.getHtml(url)


        if htmlText == ErrorsCodes.requestError:
            dict_info['errors'] = ErrorsCodes.requestError
            return dict_info

        elif htmlText == ErrorsCodes.deleteAction:
            dict_info['errors'] = ErrorsCodes.deleteAction
            return dict_info


        # Проверка существования страницы
        if self.getInfoFromHtml(htmlText, self.tagsClass['404']['tag'], self.tagsClass['404']['class']) is not None:
            dict_info['errors'] = ErrorsCodes.deleteAction
            return dict_info

        # Проверка что объявление не снято с публикации
        if self.getInfoFromHtml(htmlText, self.tagsClass['checkDeletePage']['tag'], self.tagsClass['checkDeletePage']['class']) in ErrorsCodes.listCheckDeleteAds.value:
            dict_info['errors'] = ErrorsCodes.deleteAction
            return dict_info

        if self.getInfoFromHtml(htmlText, self.tagsClass['checkSoldCar']['tag'], self.tagsClass['checkSoldCar']['class']) is not None:
            dict_info['errors'] = ErrorsCodes.soldThisCar

        # Получение даты публикации
        date_text = self.getInfoFromHtml(htmlText, self.tagsClass['datePublication']['tag'], self.tagsClass['datePublication']['class'])
        try:
            list_date = date_text.split(' ')
            date_pub = list_date[-1].split('.')
            date_publication = date_pub[2] + '-' + date_pub[1] + '-' + date_pub[0]
            dict_info['date_publication'] = date_publication
        except AttributeError:
            dict_info['errors'] = ErrorsCodes.requestError
            return dict_info
        

        dict_info['number_view'] = int( self.getInfoFromHtml(htmlText, self.tagsClass['numberView']['tag'], self.tagsClass['numberView']['class']) )
        
        
        dict_info['url'] = url

        # Извлечение характеристик из таблицы
        tableCharacteristics = htmlText.find_all(self.tagsClass['tableCharacteristics']['tag'], self.tagsClass['tableCharacteristics']['class'])
        for lines in tableCharacteristics:
            key, value = self.getInfoTable(lines)
            dict_info[key] = value


        if dict_info['number_view'] is None and dict_info['date_publication'] is None:
            dict_info['errors'].ErrorsCodes.requestError
        else:
            return dict_info

    def createUrl(self, page, minPrice, maxPrice, city):
        link = f"https://{city}.{self.namePlatform}.ru/auto/all/page{page}/?minprice={minPrice}&maxprice={maxPrice}"
        return link

    def __call__(self):
        return 'Объект класса dromClass'
