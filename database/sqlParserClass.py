from .baseClassSql import BaseSql
import datetime
from time import sleep
class ParserSqlInterface(BaseSql):

    def __init__(self, datebase_name, user_name, password_db, host_address):
        super().__init__(datebase_name, user_name, password_db, host_address)

    
    def getCity(self):
        query = "SELECT name_city FROM list_city"

        resultTable = self._get_table_from_db(query)

        result = []

        for city in resultTable:
            result.append(city[0])
        return result
    

    def getPriceRange(self):

        query = "SELECT min_price_range, max_price_range FROM list_price_range"

        return self._get_table_from_db(query)


    # Добавление новых объявлений во временную таблицу
    def insertRecordSkipConflict(self, getData, nameTable):

        for record in getData:

            query = f"SELECT * FROM ads WHERE url = '{record['url']}'"

            result = self._get_table_from_db(query)

            if len(result) == 0:

                query = f"""
                    INSERT INTO {nameTable} (model, url, price, city, platform, date_of_getting, years, update_status) VALUES
                        ($${record['model_car']}$$, $${record['url']}$$, {record['price']}, $${record['city']}$$,
                        $${record['platform']}$$, $${record['date_getting']}$$, $${record['years_car']}$$, $${record['update_status']}$$)
                            ON CONFLICT (url) DO NOTHING
                """
                self._insert_to_db(query)
            else:
                continue

    

    def UpdateSecondStep(self, getData):

        query = f"UPDATE ads SET  number_view = {getData['number_view']}"
        for attribute in getData.keys():
            if attribute is not None and attribute != 'number_view' and attribute != 'errors':
                query += f", {attribute} = $${getData[attribute]}$$"
        query += f", update_status = true WHERE url = '{getData['url']}'"

        self._insert_to_db(query)

    def getNowDateSqlFormat(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}"
        

    def getAdsForSecondStep(self, city, platform, limit):
        query = f"""
            SELECT url FROM ads
                WHERE city = '{city}' AND platform = '{platform}' AND update_status = false
                LIMIT {limit}
        """
        return self._get_table_from_db(query)


    def getCountAdsForOffset(self, city, platform, nameTable):
        query = f"""
            SELECT COUNT(*) FROM {nameTable}
                WHERE city = '{city}' AND platform = '{platform}'  AND update_status = false
        """
        return self._get_table_from_db(query)[0][0]

    

    def updateStatusToFalse(self, platform, city):

        query = f"""
            UPDATE ads SET update_status = false
                WHERE platform = '{platform}' AND city = '{city}'
        """

        self._insert_to_db(query)

    def moveToOldAds(self, url):
    
        query = f"""
            SELECT model, platform, city, price_range, price, date_publication, number_view
                FROM ads WHERE url = '{url}'
        """
        getOldAds = self._get_table_from_db(query)[0]

        # если не было получено даты публикаци, а объявление уже удалили => просто удалить, без переноса
        datePublication = getOldAds[5]
        if datePublication is None:
            query = f"""
                DELETE FROM ads WHERE url = '{url}'
            """
            self._insert_to_db(query)
            return None


        numberView = getOldAds[6]

        if numberView is None:
            numberView = 0        

        todayDate = self.getNowDateSqlFormat()

        query = f"""
            INSERT INTO save_old_ads (model, platform, city, price_range, price, date_start_publication, date_end_publication, number_view)
                VALUES ($${getOldAds[0]}$$, '{getOldAds[1]}', '{getOldAds[2]}', '{getOldAds[3]}', '{getOldAds[4]}', '{getOldAds[5]}', '{todayDate}', {numberView})
        """

        self._insert_to_db(query)

        query = f"""
            DELETE FROM ads WHERE url = '{url}'
        """
        self._insert_to_db(query)
    

    def getNewRecord(self, city, platform, nameTable):

        query = f"SELECT url FROM {nameTable} WHERE city = '{city}' AND platform = '{platform}' AND update_status = 'f' LIMIT 100"

        table = self._getRecordsDict(query)
        return table 
    
    def _createInsertQuery(self, nameTable, getDict):
        query = f'INSERT INTO {nameTable} '

        keyList = '('
        valueList = '('

        for attribute in getDict.keys():
            if getDict[attribute] is not None and attribute != 'id':
                keyList += f"{attribute},"

                if isinstance(getDict[attribute], int) or isinstance(getDict[attribute], bool):
                    valueList += f'{getDict[attribute]},'
                else:
                    valueList += f'$${getDict[attribute]}$$,'
            else:
                continue
        
        keyList = keyList[:-1]
        valueList = valueList[:-1]

        query += keyList

        query += ") VALUES "

        query += valueList

        query += ") ON CONFLICT (url) DO NOTHING "

        return query
    
    def _createUpdateQuery(self, nameTable, getDict):

        query = f"UPDATE {nameTable} SET date_publication = $${getDict['date_publication']}$$ "

        for record in getDict.keys():
            
            if record == 'errors' or record == 'url' or record is None or record == 'date_publication':
                continue
            
            if isinstance(getDict[record], str):
                query += f", {record} = $${getDict[record]}$$ "
            elif isinstance(getDict[record], int) or isinstance(getDict[record], bool):
                query += f", {record} = {getDict[record]} "
        query += f" WHERE url = $${getDict['url']}$$"
        return query

    def updateRecord(self, getData, nameTable):

        query = self._createUpdateQuery(nameTable, getData)

        self._insert_to_db(query)



    def moveToAds(self, record, nameTableFrom, nameTableTo):

        query = f"SELECT * FROM {nameTableFrom} WHERE url = $${record['url']}$$"

        getData = self._getOneRecordDict(query)

        query = self._createInsertQuery(nameTableTo, getData)

        self._insert_to_db(query)

        query = f"DELETE FROM {nameTableFrom} WHERE url = $${record['url']}$$"

        self._insert_to_db(query)
    


    def getCountNewAds(self, platform, city):
        
        query = f"SELECT COUNT(*) FROM notice_of_publication WHERE city = '{city}' AND platform = '{platform}'"

        count = self._getOneRecordDict(query)

        return count['count']
    
    def deleteRecord(self, nameTable, record):
        query = f"DELETE FROM {nameTable} WHERE url = $${record['url']}$$"
        self._insert_to_db(query)


if __name__ == '__main__':
    obj = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
    print(obj.getPriceRange())