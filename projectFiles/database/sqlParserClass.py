from .baseClassSql import BaseSql


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
                INSERT INTO ads (model, url, price, city, platform, price_range) VALUES 
                    ($${record['model_car']}$$, '{record['url']}', {record['price']}, '{record['city']}', '{record['platform']}', '{record['price_range']}')
                    ON CONFLICT (url) 
                        DO UPDATE SET
                            model = $${record['model_car']}$$,
                            price = {record['price']},
                            city = '{record['city']}',
                            platform = '{record['platform']}',
                            price_range = '{record['price_range']}'
            """
            self._insert_to_db(query)




if __name__ == '__main__':
    obj = ParserSqlInterface('carbuy_db', 'carbuy', 'carbuy', 'localhost')
    print(obj.getPriceRange())