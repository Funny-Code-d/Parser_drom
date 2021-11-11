from .abstract.abstractClass import AbstractParser


class dromClass(AbstractParser):

    def __init__(self, proxies, header):
        super().__init__(proxies, header)
        self.namePlatform = "drom"

    def getInfoFields(self, url):

        htmlText = self.getHtml(url)

        if htmlText is None:
            return None
        elif htmlText == '404':
            return 'Delete ads'
        
        fields = htmlText.find_all('a', class_='ewrty961')
        
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

        if htmlText is None:
            return None
        elif htmlText == '404':
            return 'Delete ads'

        try:
            check_delete_page = htmlText.find("h1", class_="e18vbajn0").get_text(strip=True)
            
            if check_delete_page in ('Объявление удалено!', 'Объявление не опубликовано.'):
                return "Delete ads"

            number_view = int(htmlText.find("div", class_="css-14wh0pm e1lm3vns0").get_text(strip=True))
            #print(number_view)
            date_text = htmlText.find("div", class_="css-pxeubi evnwjo70").get_text(strip=True)
        
        except AttributeError:
            return "Attribute error"


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
