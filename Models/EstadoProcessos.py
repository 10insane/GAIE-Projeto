from Models.bd_connection import *
import mysql.connector


def criarEstado(idEstado, estado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO EstadosProcesso (idEstado, Estado)
            VALUES (%s, %s)
            """,
            (idEstado, estado)
        )
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao inserir o estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def listarEstados():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM EstadosProcesso")
        estados = cursor.fetchall()
        return estados
    except mysql.connector.Error as erro:
        print("Erro ao listar os estados:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarEstado(idEstado, novoEstado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE EstadosProcesso
            SET Estado = %s
            WHERE idEstado = %s
            """,
            (novoEstado, idEstado)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar o estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarEstado(idEstado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM EstadosProcesso WHERE idEstado = %s",
            (idEstado,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar o estado:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
