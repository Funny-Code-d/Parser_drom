from abstractClass import AbstractParser


class dromClass(AbstractParser):

    def getInfoFields(self, url, city):

        htmlText = self.getHtml(url, header={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0', 'accept' : '*/*'})
        
        if htmlText is None:
            return None
        
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
                "city" : city
            })
        return returnsList
        

    def getInfoPageField(self, url):
        htmlText = self.getHtml(url)

        if htmlText is None:
            return None

        try:
            check_delete_page = htmlText.find("h1", class_="e18vbajn0").get_text(strip=True)
            
            if check_delete_page in ['Объявление удалено!', 'Объявление не опубликовано.']:
                return "Delete ads"

            number_view = int(htmlText.find("div", class_="css-14wh0pm e1lm3vns0").get_text(strip=True))
            print(number_view)
            date_text = htmlText.find("div", class_="css-pxeubi evnwjo70").get_text(strip=True)
        
        except AttributeError:
            return "Attribute error"


        # Извлечение даты из декста
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


obj = dromClass()
print(obj.getInfoPageField('https://angarsk.drom.ru/toyota/celica/44530474.html'))
