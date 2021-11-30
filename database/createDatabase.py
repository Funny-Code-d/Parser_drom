from baseClassSql import BaseSql

class CreateTablesClass(BaseSql):

    def __init__(self, datebase_name, user_name, password_db, host_address):
        super().__init__(datebase_name, user_name, password_db, host_address)


    def createCatalogs(self):

        catalogCity = """
            CREATE TABLE IF NOT EXISTS list_city (
                id serial PRIMARY KEY,
                name_city varchar(30) UNIQUE
            )
        """

        catalogPlatform = """
            CREATE TABLE IF NOT EXISTS list_platform (
                id serial PRIMARY KEY,
                name_platform varchar(30) UNIQUE
            )
        """

        catalogPriceRange = """
            CREATE TABLE IF NOT EXISTS list_price_range (
                id serial PRIMARY KEY,
                range varchar(30) UNIQUE,
                min_price_range integer,
                max_price_range integer
            )
        """

        catalogTypeAgregation = """
            CREATE TABLE IF NOT EXISTS list_type_agregation (
                id serial PRIMARY KEY,
                number_days integer UNIQUE
            )
        """

        return (catalogCity, catalogPlatform, catalogPriceRange, catalogTypeAgregation)
    


    def createTables(self):

        tableAds = """
            CREATE TABLE IF NOT EXISTS ads (
                id serial,
                url text PRIMARY KEY,
                model varchar(50),
                city varchar(30),
                platform varchar(30),
                price float,
                number_view integer,
                price_range varchar(30),
                date_publication date,
                date_of_getting date,
                update_status bool,
                years varchar(30),
                color varchar(30),
                motor varchar(30),
                motorPower varchar(30),
                transmission varchar(30),
                drive varchar(30),
                mileage varchar(30),
                wheel varchar(30),
                bodyType varchar(30),
                generation varchar(30),
                
                FOREIGN KEY (city)
                    REFERENCES list_city(name_city)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                
                FOREIGN KEY (platform)
                    REFERENCES list_platform(name_platform)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,

                FOREIGN KEY (price_range)
                    REFERENCES list_price_range(range)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """

        tableAnalysis = """
            CREATE TABLE IF NOT EXISTS analysis (
                average_view float,
                model varchar(50) NOT NULL,
                city varchar(30),
                platform varchar(30),
                average_price float,
                price_range varchar(30) NOT NULL,
                type_agregation integer,
                date_rating date NOT NULL,
                PRIMARY KEY (model, platform, date_rating, price_range),
                FOREIGN KEY (type_agregation)
                    REFERENCES list_type_agregation(number_days)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """

        tableNumberModel = """
            CREATE TABLE IF NOT EXISTS number_of_model_declarations (
                model varchar(50),
                number_declaration integer,
                type_agregation integer,
                city varchar(30),
                platform varchar(30),
                calculate_date date,
                
                PRIMARY KEY (model, platform, calculate_date),
                
                FOREIGN KEY (type_agregation)
                    REFERENCES list_type_agregation(number_days)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                
                FOREIGN KEY (city)
                    REFERENCES list_city(name_city)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,

                FOREIGN KEY (platform)
                    REFERENCES list_platform(name_platform)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """

        tableOldAds = """
            CREATE TABLE IF NOT EXISTS save_old_ads (
                id serial PRIMARY KEY,
                model varchar(50),
                city varchar(30),
                platform varchar(30),
                price float,
                number_view integer,
                price_range varchar(30),
                date_start_publication date,
                date_end_publication date,
                years varchar(30),
                color varchar(30),
                motor varchar(30),
                motorPower varchar(30),
                transmission varchar(30),
                drive varchar(30),
                mileage varchar(30),
                wheel varchar(30),
                bodyType varchar(30),
                generation varchar(30)
            )
        """

        noticeOfPublication = """
            CREATE TABLE IF NOT EXISTS notice_of_publication (
                id serial,
                url text PRIMARY KEY,
                model varchar(50),
                city varchar(30),
                platform varchar(30),
                price float,
                number_view integer,
                price_range varchar(30),
                date_publication date,
                date_of_getting date,
                update_status bool,
                years varchar(30),
                color varchar(30),
                motor varchar(30),
                motorPower varchar(30),
                transmission varchar(30),
                drive varchar(30),
                mileage varchar(30),
                wheel varchar(30),
                bodyType varchar(30),
                generation varchar(30)
            )
        """
        

        return (tableAds, tableAnalysis, tableNumberModel, tableOldAds, noticeOfPublication)
    
    def dropTables(self):
        dropList = [
            "DROP TABLE ads",
            "DROP TABLE analysis",
            "DROP TABLE number_of_model_declarations",
            "DROP TABLE save_old_ads",
            "DROP TABLE list_type_agregation",
            "DROP TABLE list_price_range",
            "DROP TABLE list_platform",
            "DROP TABLE list_city"
        ]

        for item in dropList:
            self._insert_to_db(item)
        else:
            print("База удалена")
        

    def run(self):
        
        catalogs = self.createCatalogs()
        tables = self.createTables()

        for item in catalogs:
            self._insert_to_db(item)
        
        for item in tables:
            self._insert_to_db(item)


if __name__ == "__main__":
    obj = CreateTablesClass("carbuy_db", 'carbuy', 'carbuy', 'localhost')
    obj.run()