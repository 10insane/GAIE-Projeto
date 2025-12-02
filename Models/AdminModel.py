from Models.bd_connection import *
import mysql.connector

def criarAdmin(nProcAdmin, NomeAdmin, password):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Admin (nProcAdmin, NomeAdmin, password) VALUES (%s, %s, %s)",
            (nProcAdmin, NomeAdmin, password)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir admin:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def listarAdmin():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)  
    try:
        cursor.execute("SELECT * FROM Admin")
        admins = cursor.fetchall()
        return admins
    except mysql.connector.Error as error:
        print("Erro ao buscar admins:", error)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarAdmin(nProcAdmin, novoNome, novaPassword):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Admin SET NomeAdmin = %s, password = %s WHERE nProcAdmin = %s",
            (novoNome, novaPassword, nProcAdmin)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar admin:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarAdmin(nProcAdmin):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Admin WHERE nProcAdmin = %s",
            (nProcAdmin,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar admin:", error)
        return False
    finally:
        cursor.close()
        conn.close()
