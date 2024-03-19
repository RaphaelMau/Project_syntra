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

def store_user(username, password):
    salt=os.urandom(32)
    hashed_password = create_hash(password,salt)

    conn = create_connection()
    if conn.is_connected():
        cursor = conn.cursor()
        query = f'''call insert_user( %s, %s, %s);'''
        val = (username, hashed_password, salt.decode('latin1'))
        cursor.execute(query,val)
        conn.commit()
        conn.close()
store_user("test","TEST")

def check_password(iduser, userPassword):
    conn = create_connection()
    sql = f'''call get_user({iduser})'''
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0]

    hash_password_InDB = result[2]
    salt = result[3].encode('latin1')

    hex_hash = create_hash(userPassword,salt)
    return hex_hash == hash_password_InDB

print(check_password(2, "TEST"))