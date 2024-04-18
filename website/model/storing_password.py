import hashlib
from hashlib import pbkdf2_hmac as pbkdf2
import mysql.connector as msql
from mysql.connector import Error
import os

def create_hash(password, salt):
    plaintext = password.encode()
    digest = pbkdf2('sha256', plaintext, salt, 100000)
    hex_hash = digest.hex()
    return hex_hash

def create_connection():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': "Rafi2004.",
        'database': 'project_db'
        }
    conn = msql.connect(**config)
    conn = msql.connect(host= 'localhost',user= 'root',password= "Rafi2004.",database='project_db')
    return conn
    

def store_user(iduser,name, first_name, phone_number, email, password, salt, admin):
    salt=os.urandom(32)
    hashed_password = create_hash(password,salt)

    conn = create_connection()
    if conn.is_connected():
        cursor = conn.cursor()
        query = f'''call insert_user( %s, %s, %s, %s, %s, %s, %s, %s);'''
        val = (iduser,name, first_name, phone_number, email, password, salt.decode('latin1'), admin)
        cursor.execute(query,val)
        conn.commit()
        conn.close()

def check_password(iduser, userPassword):
    conn = create_connection()
    sql = f'''call Get_User({iduser})'''
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0]

    hash_password_InDB = result[0]
    salt = result[1].encode('latin1')

    hex_hash = create_hash(userPassword,salt)
    return hex_hash == hash_password_InDB