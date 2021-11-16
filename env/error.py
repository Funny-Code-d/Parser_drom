from enum import Enum

class ErrorsCodes(Enum):
    
    requestOk = 200
    notFound = 404
    deleteAction = 'delete'
    listCheckDeleteAds = ('Объявление удалено!', 'Объявление не опубликовано.')
    requestError = 'rechek'
    soldThisCar = 'sold'