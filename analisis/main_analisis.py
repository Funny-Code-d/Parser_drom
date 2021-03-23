import car_class
import os
import shelve
from time import sleep

# функция для вычисления среднего количкства просмотров
def analisis_file(path_to_dir, name_file):
    # print('new file')
    list_object_from_file = []
    with shelve.open(path_to_dir + name_file) as file:
        for key in file.keys():
            object = file[key]
            list_object_from_file.append(object)
    name_car = name_file.replace('.db', '')
    analisis_object = car_class.Car(number_view=0,
                                    price=0,
                                    name_car=name_car)
    for object_from_list in list_object_from_file:
        try:
            # object_from_list.analisis(analisis_object)
            analisis_object.analisis(object_from_list)
        except AttributeError:
            continue
    analisis_object.average_number_view_one_week()
    analisis_object.average_number_view_two_week()
    analisis_object.average_number_view_month()
    # print('next object', end='\n\n')
    return analisis_object    


# --------------------------------------------------------------
# Функции для сортировки в зависимости от отрезка времени
def sort_list_car_one_week(list_car):
    sort_list = []
    length = len(list_car)

    for iteration_sort in range(length):
        object_of_list_car = list_car[0]
        max_view = list_car[0].one_week_pub
        index_for_delete_object_from_list = 0

        for car in range(len(list_car)):
            if list_car[car].one_week_pub > max_view:
                max_view = list_car[car].one_week_pub
                object_of_list_car = list_car[car]
                index_for_delete_object_from_list = car

        sort_list.append(object_of_list_car)
        del list_car[index_for_delete_object_from_list]

    return sort_list


def sort_list_car_two_week(list_car):
    sort_list = []
    length = len(list_car)
    for iteration_sort in range(length):
        object_of_list_car = list_car[0]
        max_view = list_car[0].two_week_pub
        index_for_delete_object_from_list = 0

        for car in range(len(list_car)):
            
            if list_car[car].two_week_pub > max_view:
                max_view = list_car[car].two_week_pub
                object_of_list_car = list_car[car]
                index_for_delete_object_from_list = car
                
        sort_list.append(object_of_list_car)
        del list_car[index_for_delete_object_from_list]
        
    return sort_list


def sort_list_car_month(list_car):
    sort_list = []
    length = len(list_car)

    for iteration_sort in range(length):
        object_of_list_car = list_car[0]
        max_view = list_car[0].month_pub
        index_for_delete_object_from_list = 0

        for car in range(len(list_car)):

            if list_car[car].month_pub > max_view:
                max_view = list_car[car].month_pub
                object_of_list_car = list_car[car]
                index_for_delete_object_from_list = car

        sort_list.append(object_of_list_car)
        del list_car[index_for_delete_object_from_list]

    return sort_list
# -----------------------------------------------------------------------------------------------------------

def main():
    # переменные с городами
    _city = ('novosibirsk', 'irkutsk', 'moscow', 'spb')
    
    _directory = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
    _save_analisis = _directory.copy()
    
    directory = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
    save_analisis = _directory.copy()
    # заходим в директорию города
    
    for city in _city:
        # составление относительного пути
        for iter in range(len(_directory)):
            directory[iter] = f'../data_base/{city}/{_directory[iter]}/'
            save_analisis[iter] = f'../telegram/analisis/{city}/{_save_analisis[iter]}/'
        
        # заходим в директорию ценового диапазона
        index_save_path = 0
        for direct in directory:
            # получаем список файлов в каталоге
            # ------------------------------------------
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
            # ------------------------------------------
            print(f"Анализируется {direct}")
            # получаем список с объектами клааса которые имеют среднее количество промотров
            name_car_for_analisis = []      
            for car_file in ls:
                car = analisis_file(direct, car_file)
                name_car_for_analisis.append(car)
            analisis_one_week = name_car_for_analisis.copy()
            analisis_two_week = name_car_for_analisis.copy()
            analisis_month = name_car_for_analisis.copy()
            
            # освобождаем память
            del name_car_for_analisis
            
            # Сортировка списка объектов
            sort_car_one_week = sort_list_car_one_week(analisis_one_week)
            sort_car_two_week = sort_list_car_two_week(analisis_two_week)
            sort_car_month = sort_list_car_month(analisis_month)
            
            # освобождение памяти
            del analisis_one_week
            del analisis_two_week
            del analisis_month

            # словари для хранения объектов
            sort_dict_one_week = {}
            sort_dict_two_week = {}
            sort_dict_month = {}
            # Запись списков в слоарь для хранения и блее простого и надёжного извлечения
            # запись: место в рейтинге => объект
            for iteration in range(len(sort_car_one_week)):
                sort_dict_one_week[iteration] = sort_car_one_week[iteration]
            
            for iteration in range(len(sort_car_two_week)):
                sort_dict_two_week[iteration] = sort_car_two_week[iteration]
                
            for iteration in range(len(sort_car_month)):
                sort_dict_month[iteration] = sort_car_month[iteration]
            
            # Освобождение памяти
            del sort_car_one_week
            del sort_car_two_week
            del sort_car_month
            
            with shelve.open(save_analisis[index_save_path] + 'analisis.db') as file:
                file['one_week'] = sort_dict_one_week
                file['two_week'] = sort_dict_two_week
                file['month'] = sort_dict_month
                print("was write!!!")
            del sort_dict_one_week
            del sort_dict_two_week
            del sort_dict_month
            index_save_path += 1
            
            
                

main()
