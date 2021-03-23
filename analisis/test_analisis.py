import car_class
import shelve

db = {}

_directory = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
_save_analisis = _directory.copy()

_city = ('novosibirsk', 'irkutsk', 'moscow', 'spb')
directory = ['0-100', '100-200', '200-500', '500-900', '900-1500', '1500-2000']
save_analisis = directory.copy()

for city in _city:
    for iter in range(len(_directory)):
        directory[iter] = f'../data_base/{city}/{_directory[iter]}/'
        save_analisis[iter] = f'../telegram/analisis/{city}/{_save_analisis[iter]}/'

    for path in save_analisis:
        with shelve.open(path + 'analisis.db') as file:
            db = file['month']
        print(path)
        for key in range(5):
            try:
                print(f'{key + 1} место:')
                print(db[key].name_car)
                print(db[key].one_week_pub)
                print('\n')
            except KeyError:
                break
