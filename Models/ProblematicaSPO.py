from Models.bd_connection import *
import mysql.connector


from Models.bd_connection import *
import mysql.connector

def criarProblematica(tipoProblematica):
    """
    Cria uma nova problemática e retorna o ID gerado.
    """
    conn = bd_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO problematicaspo (TipoProblematica) VALUES (%s)",
            (tipoProblematica,)
        )
        conn.commit()
        # Pegar o ID auto increment
        return cursor.lastrowid
    except mysql.connector.Error as erro:
        print("Erro ao inserir problemática:", erro)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()




def listarProblematicas():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM problematicaspo")
        problematicas = cursor.fetchall()
        return problematicas
    except mysql.connector.Error as erro:
        print("Erro ao listar as problemáticas:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarProblematica(idProblematica, novoTipoProblematica):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE problematicaspo
            SET TipoProblematica = %s
            WHERE idProblematica = %s
            """,
            (novoTipoProblematica, idProblematica)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar a problemática:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarProblematica(idProblematica):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM problematicaspo WHERE idProblematica = %s",
            (idProblematica,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar a problemática:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
