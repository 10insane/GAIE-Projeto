from Models.bd_connection import *
import mysql.connector

def criarEstadoProcesso(IdEstadoProcesso, Estado):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO EstadosProcesso (IdEstadoProcesso, Estado) VALUES (%s, %s)",
            (IdEstadoProcesso, Estado)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir o Estado do Processo:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def listarEstadoProcesso():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM EstadosProcesso")
        EstadoProcesso = cursor.fetchall()
        return EstadoProcesso
    except mysql.connector.Error as error:
        print("Erro ao buscar o Estado do Processo:", error)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarEstadoProcesso(IdEstadoProcesso, novoEstadoProcesso):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE EstadosProcesso SET Estado = %s WHERE IdEstadoProcesso = %s",
            (novoEstadoProcesso, IdEstadoProcesso)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar Estado do Processo:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarEstadoProcesso(IdEstadoProcesso):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM EstadosProcesso WHERE IdEstadoProcesso = %s",
            (IdEstadoProcesso,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar Estado do Processo:", error)
        return False
    finally:
        cursor.close()
        conn.close()
