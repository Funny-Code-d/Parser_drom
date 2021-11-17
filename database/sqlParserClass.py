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

    def upSertFirstStep(self, getData):

        for record in getData:
            query = f"""
                INSERT INTO ads (model, url, price, city, platform, price_range, date_of_getting, update_status) VALUES 
                    ($${record['model_car']}$$, '{record['url']}', {record['price']}, '{record['city']}', '{record['platform']}', '{record['price_range']}', '{record['date_getting']}', {record['update_status']})
                    ON CONFLICT (url) 
                        DO UPDATE SET
                            model = $${record['model_car']}$$,
                            price = {record['price']},
                            city = '{record['city']}',
                            platform = '{record['platform']}',
                            price_range = '{record['price_range']}',
                            update_status = {record['update_status']}
            """
            self._insert_to_db(query)
    

    def UpdateSecondStep(self, getData):
        
        query = f"""
            UPDATE ads SET date_publication = '{getData['date_publication']}', number_view = {getData['number_view']}, update_status = true
                WHERE url = '{getData['url']}'

        """
        #print(query)
        self._insert_to_db(query)

    def getNowDateSqlFormat(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}"
        

    def getAdsForSecondStep(self, city, platform, limit):
        yesterday = self.getNowDateSqlFormat()
        query = f"""
            SELECT url FROM ads
                WHERE city = '{city}' AND platform = '{platform}' AND date_of_getting < '{yesterday}' AND update_status = false
                LIMIT {limit}
        """
        return self._get_table_from_db(query)


    def getCountAdsForOffset(self, city, platform):
        todayDate = self.getNowDateSqlFormat()
        query = f"""
            SELECT COUNT(*) FROM ads
                WHERE city = '{city}' AND platform = '{platform}' AND date_of_getting < '{todayDate}'  AND update_status = false
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



if __name__ == '__main__':
    obj = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
    print(obj.getPriceRange())