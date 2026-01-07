from Models.bd_connection import *
import mysql.connector

def criarTecnico(nProcTecnico, nomeTecnico, password):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tecnicos (nProcTecnico ,nomeTecnico, password) VALUES (%s, %s, %s)",
            (nProcTecnico, nomeTecnico, password)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir tecnico:", error)
        return False
    finally:
        cursor.close()
        conn.close()

def listarTecnico():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)  
    try:
        cursor.execute("SELECT * FROM tecnicos")
        tecnicos = cursor.fetchall()
        return tecnicos
    except mysql.connector.Error as error:
        print("Erro ao buscar tecnico:", error)
        return []
    finally:
        cursor.close()
        conn.close()

def atualizarTecnico(nProcTecnico, novoNome):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE tecnicos SET nomeTecnico = %s WHERE nProcTecnico = %s",
            (novoNome, nProcTecnico)  # 2 valores para 2 %s
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar tecnico:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarTecnico(nProcTecnico):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM tecnicos WHERE nProcTecnico  = %s",
            (nProcTecnico,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar tecnico:", error)
        return False
    finally:
        cursor.close()
        conn.close()

def buscarTecnicoPorProc(nProcTecnico):
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM tecnicos WHERE nProcTecnico = %s",
            (nProcTecnico,)
        )
        return cursor.fetchone()
    except mysql.connector.Error as error:
        print("Erro ao buscar tecnico:", error)
        return None
    finally:
        cursor.close()
        conn.close()