import mysql.connector
from mysql.connector import Error

def bd_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="bd_gaie"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro na conexão: {e}")
        return None
