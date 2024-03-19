import mysql.connector as msql
from mysql.connector import Error
from key import password_sql #dit is een klasse die ik heb gemaakt en mijn password in zit als een variable

def getData(db, table):
    try:
        conn = msql.connect(host='localhost', user='root', password=password_sql, database= db)
        sql = f'''SELECT * FROM {table}'''
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    except Error as e:
        print("Error while connecting to MySQL", e)

getData("tennisdb","spelers")
