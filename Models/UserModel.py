from Models.bd_connection import *
import mysql.connector

def criarUser(nProcesso, nomeTecnicos):
    conn = bd_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tecnicos (nProcesso, nomeTecnicos) VALUES (%s, %s)",
            (nProcesso, nomeTecnicos)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir usuário:", error)
        return False
    finally:
        cursor.close()
        conn.close()

