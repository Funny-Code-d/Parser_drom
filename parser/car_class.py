import datetime


class Car:
    def __init__(self, name_car=None, years=None, number_view=None, date_public=None, url=None, photo=None, price=None, publication=0):
        self.name_car = name_car
        self.number_view = number_view
        self.date_public = date_public
        self.url = url
        self.photo = photo
        self.years = years
        self.price = price
        self.publication = publication

    # методы для получения значений из класса
    def return_url(self):
        return self.url

    def return_name_car(self):
        return self.name_car
    
    def return_years(self):
        return self.years
    
    def return_price(self):
        return self.price
    def return_photo(self):
        return self.photo

    # метод для вывода объекта на экран
    def output(self):
        print('Name car: ' + self.name_car)
        print("Years: " + str(self.years))
        print("Price: " + str(self.price))
        print("Url: " + str(self.url))
        print("Number view: " + str(self.number_view))
        print("Date: " + str(self.date_public))
        print('Url-photo: ' +str(self.photo))
        print('\n')

    
    def analisis(self, other_object):
        date_now = datetime.datetime.now()
        difference_date = (date_now - self.date_public).days
        views_per_day = self.number_view / difference_date
        other_object.number_view += views_per_day
        other_object.publication += 1
        
        

