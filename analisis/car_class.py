import datetime
from time import sleep

class Car:
    def __init__(self, name_car=None, years=None, number_view=None, date_public=None, url=None, photo=None, price=None):
        self.name_car = name_car
        self.number_view = number_view
        self.date_public = date_public
        self.url = url
        self.photo = photo
        self.years = years
        self.price = price
        self.publication = 0
        self.average_view = 0
        
        self.one_week_pub = 0
        self.one_week_pub_counter = 0
        
        self.two_week_pub = 0
        self.two_week_pub_counter = 0
        
        self.month_pub = 0
        self.month_pub_counter = 0


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
        try:
            difference_date = (date_now - other_object.date_public).days
            try:
                views_per_day = int(other_object.number_view) / difference_date
            except ZeroDivisionError:
                views_per_day = int(other_object.number_view)
            # print(f"Name car: {self.name_car}\nDay: {difference_date}\nNumber_view: {other_object.number_view}\nViews per day: {views_per_day}")

            # если дата публикации не более недели
            if 0 <= difference_date <= 7:
                self.one_week_pub += views_per_day
                self.one_week_pub_counter += 1
                # print("Попало в статичтику первой недели")
            # если дата публикации не более 2 недель
            if 0 < difference_date <= 14:
                self.two_week_pub += views_per_day
                self.two_week_pub_counter += 1
                # print("Попало в статистику первый двух недель")
            # Если дата публикации не более месяца
            if 0 < difference_date <= 30:
                # print("Попало в статистку за месяц")
                self.month_pub += views_per_day
                self.month_pub_counter += 1
                
        except TypeError:
            pass
        
    def average_number_view_one_week(self):
        if self.one_week_pub_counter > 0:
            self.one_week_pub = self.one_week_pub / self.one_week_pub_counter
        else:
            pass
            # print('ERROR1')
            # print(f"Name car: {self.name_car}\nOne week pub: {self.one_week_pub}\nOne week pub counter: {self.one_week_pub_counter}")
            # sleep(2)
    
    def average_number_view_two_week(self):
        if self.two_week_pub_counter > 0:
            self.two_week_pub = self.two_week_pub / self.two_week_pub_counter
        else:
            pass
            #print("ERROR2")
            #print(f"Name car: {self.name_car}\nOne week pub: {self.two_week_pub}\nOne week pub counter: {self.two_week_pub_counter}")
            #sleep(2)
            
    def average_number_view_month(self):
        if self.month_pub_counter > 0:
            self.month_pub = self.month_pub / self.month_pub_counter
        else:
            pass
            #print("ERROR3")
            #print(f"Name car: {self.name_car}\nOne week pub: {self.month_pub}\nOne week pub counter: {self.month_pub_counter}")
            #sleep(2)
