from Models.bd_connection import *
import mysql.connector

def listarEstados():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT idEstado, Estado FROM estadosprocesso")
        return cursor.fetchall()
    except mysql.connector.Error as erro:
        print("Erro ao listar estados:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def criarEstado(idEstado, Estado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO estadosprocesso (idEstado, Estado) VALUES (%s, %s)", (idEstado, Estado))
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao criar estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def atualizarEstado(idEstado, novoEstado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE estadosprocesso SET Estado = %s WHERE idEstado = %s", (novoEstado, idEstado))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarEstado(idEstado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM estadosprocesso WHERE idEstado = %s", (idEstado,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
