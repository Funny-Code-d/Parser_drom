from .baseClassSql import BaseSql
import datetime

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
                INSERT INTO ads (model, url, price, city, platform, price_range, date_of_getting) VALUES 
                    ($${record['model_car']}$$, '{record['url']}', {record['price']}, '{record['city']}', '{record['platform']}', '{record['price_range']}', '{record['date_getting']}')
                    ON CONFLICT (url) 
                        DO UPDATE SET
                            model = $${record['model_car']}$$,
                            price = {record['price']},
                            city = '{record['city']}',
                            platform = '{record['platform']}',
                            price_range = '{record['price_range']}',
                            date_of_getting = '{record['date_getting']}'
            """
            self._insert_to_db(query)
    

    def UpdateSecondStep(self, getData):
        
        query = f"""
            UPDATE ads SET date_publication = '{getData['date_publication']}', number_view = {getData['number_view']}
                WHERE url = '{getData['url']}'

        """
        #print(query)
        self._insert_to_db(query)

    def getNowDateSqlFormat(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}"
        

    def getAdsForSecondStep(self, city, platform, offset, limit):
        yesterday = self.getNowDateSqlFormat()
        query = f"""
            SELECT url FROM ads
                WHERE city = '{city}' AND platform = '{platform}' AND date_of_getting = '{yesterday}' ORDER BY model
                LIMIT {limit} OFFSET {offset}
        """
        
        return self._get_table_from_db(query)


    def getCountAdsForOffset(self, city, platform):

        query = f"""
            SELECT COUNT(*) FROM ads
                WHERE city = '{city}' AND platform = '{platform}'
        """
        return self._get_table_from_db(query)[0][0]


if __name__ == '__main__':
    obj = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
    print(obj.getPriceRange())