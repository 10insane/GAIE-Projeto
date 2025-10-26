from Models.bd_connection import *
import mysql.connector

def criarEscola(IdEscola, nomeEscola):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO escolas (IdEscola, NomeEscola) VALUES (%s)",
            (IdEscola, nomeEscola)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir escola:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def listarEscolas():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM escolas")
        escolas = cursor.fetchall()
        return escolas
    except mysql.connector.Error as error:
        print("Erro ao buscar escolas:", error)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarEscola(idEscola, novoNome):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE escolas SET NomeEscola = %s WHERE idEscola = %s",
            (novoNome, idEscola)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar escola:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarEscola(idEscola):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM escolas WHERE idEscola = %s",
            (idEscola,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar escola:", error)
        return False
    finally:
        cursor.close()
        conn.close()
