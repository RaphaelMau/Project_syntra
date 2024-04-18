import mysql.connector as msql
from mysql.connector import Error

def getData(table):
    try:
        conn = msql.connect(host='localhost', user='root', password="Rafi2004.", database= "project_db")
        sql = f'''SELECT * FROM {table}'''
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result
    except Error as e:
        print("Error while connecting to MySQL", e)