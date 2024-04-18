from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Function to insert data into MySQL database
def insert_into( table, data):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rafi2004.',
            database='project_db'
        )
        cursor = conn.cursor()
        sql = f"INSERT INTO {table} (iduser, name, first_name, phone_number, email, password, salt, admin) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
        conn.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as e:
        print("Error while inserting data into MySQL:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")