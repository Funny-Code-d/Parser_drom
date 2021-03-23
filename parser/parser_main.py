from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from bs4 import BeautifulSoup
import car_class
import shelve
import os
import datetime
from time import sleep
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
           'accept' : '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# начальный сбор информации
def get_primary_content(html, city):
    soup = BeautifulSoup(html, "html.parser")
    # поиск таблички каждой машины на странице
    items = soup.find_all("a", class_="css-1hgk7d1")
    for item in items:
        car = {}
        # поиск в табличке машины (марка машины, год, ссылка на объявление, цена)
        name = item.find('div', class_='eozdvfu0').get_text(strip=True)
        list_name = name.split(',')
        try:
            car['name_car'] = list_name[0]
            car['years'] = int(list_name[1])
            car['href'] = item.get('href')
        except ValueError:
            continue
        # поиск цены
        price = item.find('div', class_='css-1dv8s3l').get_text(strip=True)
        price = price.replace("q", "")
        try:
            price = int(price.replace(' ', ''))
        except ValueError:
            continue
        car['price'] = price
        
        # поиск фото
        try:
            photo = item.find('div', class_='css-1kfbj4a')
            photo = photo.find('img', class_='css-zvnnlg')
            photo = photo.get('data-src')
        except AttributeError:
            photo = None
        car['photo'] = photo
        # создание объекта
        car_object = car_class.Car(name_car=car['name_car'],
                                   years=car['years'],
                                   url=car['href'],
                                   price=car['price'],
                                   photo=car['photo'])
        
        # Сортировка по директориям
        if 0 < price < 100000:
            with shelve.open("../data_base/" + str(city) + '/0-100/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object
                
        elif 100000 < price < 200000:
            with shelve.open("../data_base/" + str(city) + '/100-200/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object

        elif 200000 < price < 500000:
            with shelve.open("../data_base/" + str(city) + '/200-500/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object
                
        elif 500000 < price < 900000:
            with shelve.open("../data_base/" + str(city) + '/500-900/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object
                
        elif 900000 < price < 1500000:
            with shelve.open("../data_base/" + str(city) + '/900-1500/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object
                
        elif 1500000 < price < 2000000:
            with shelve.open("../data_base/" + str(city) + '/1500-2000/' + str(car['name_car']) + '.db') as file:
                file[car['href']] = car_object

# сбор всех необходимых данных
def second_parse(html, name_car, years, price, url, photo):
    # сбор информации из html кода
    soup = BeautifulSoup(html.text, "html.parser")
    # получение количества просмотров
    view = soup.find('div', class_='css-se5ay5 e1lm3vns0')
    if view:
        view = soup.find('div', class_='css-se5ay5').get_text(strip=True)
    else:
        return
    # получение доты публикации
    data = soup.find('div', class_='css-61s82p')
    if data:
        data = soup.find('div', class_='css-61s82p evnwjo70').get_text(strip=True)
    else:
        return
    # проверка что дата считалась правильно
    try:
        day_mouth_years = data.split(' ')
        data_list = day_mouth_years[-1].split('.')
        day = int(data_list[0])
        mouth = int(data_list[1])
        years_public = int(data_list[2])
        date_public = datetime.datetime(years_public, mouth, day)
    except AttributeError:
        return
    # создание объекта с полной информацией
    car_object = car_class.Car(name_car=name_car,
                               years=years,
                               price=price,
                               url=url,
                               photo=photo,
                               date_public=date_public,
                               number_view=view)
    return car_object
    


# наполнение базы всей нужной информацией
def get_full_content(city):
    directory = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
    for iter in range(len(directory)):
        directory[iter] = f'../data_base/{city}/{directory[iter]}/'
    
    for direct in directory:
        # ---------------------------------------------------------------
        # Чтение имён файлов содержащихся в директории
        os.system(f"ls {direct} > name")
        ls = []
        with open('name', 'r') as file:
            while True:
                line = file.readline()
                line = line.replace('\n', '')
                if line == '':
                    break
                ls.append(line)
        os.system("rm name")
        # ---------------------------------------------------------------
        # Открытие базы даных и парсинг каждого объявления
        for db_car in ls:
            # открытие одной базы
            with shelve.open(direct + db_car) as file:
                # цикл по ключам
                for key in file.keys():
                    car_object = file[key]
                    # Получение ссылки на объявление
                    try:
                        url = car_object.return_url()
                    except AttributeError:
                        continue
                    # -------------------------------------------------------
                    # непосредсвенно парсинг объявления
                    html = get_html(url)
                    if html.status_code == 200:
                        name_car = car_object.return_name_car()
                        years = car_object.return_years()
                        price = car_object.return_price()
                        photo = car_object.return_photo()
                        car_object = second_parse(html, name_car, years, price, url, photo)
                        try: 
                            car_object.output()
                        except AttributeError:
                            pass
                        file[url] = car_object
                        del car_object
                    
                    
    
                

# Главная функция, от сюда начинается работа парсера
def parse(number_page, city, categories):
    for page in range(1, number_page + 1):
        html = get_html("https://" + str(city) + ".drom.ru/auto/all/page" + str(page) + '/?minprice=' + str(categories[0]) + '&maxprice=' + str(categories[1]))
        if html.status_code == 200:
            get_primary_content(html.text, city)
            print(f"СТРАНИЦА {page}")


def main(GLOBAL_CITY):
    for city in GLOBAL_CITY:
        categories = [ [0, 100000],
                      [100000, 200000],
                      [200000, 500000],
                      [500000, 900000],
                      [900000, 1500000],
                      [1500000, 2000000] ]
        for categ in categories:
            print(f'Сейчас парсится:\n Город: {city}\nЦеновой диапазон {categ[0]/1000} - {categ[1]/1000}')
            parse(100, city, categ)
        get_full_content(city)
        
test = ['novosibirsk', 'irkutsk', 'moscow', 'spb']
main(test)
# with shelve.open('../data_base/novosibirsk/0-100/Лада 2113 Самара.db') as file:
#     for key in file.keys():
#         car_object = file[key]
#         car_object.output()
        