import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='tinkerTHEbest', host='localhost')
# cursor = conn.cursor()
# code = ['190', "747", '987']
# cursor.execute("INSERT INTO aircrart VALUES ('123', 'Airbus', 7000)")
# records = cursor.fetchall()
with conn.cursor() as cursor:
    conn.autocommit = True
    insert = sql.SQL("INSERT INTO aircraft VALUES ('243', 'Boeing', 4000)")
    cursor.execute(insert) 

cursor.close()
conn.close()