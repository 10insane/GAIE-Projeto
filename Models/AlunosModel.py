from Models.bd_connection import *
import mysql.connector

def criarAluno(nProcesso, nomeAluno):
    conn = bd_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tecnicos (nProcesso, NomeAluno) VALUES (%s, %s)",
            (nProcesso, nomeAluno)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir aluno:", error)
        return False
    finally:
        cursor.close()
        conn.close()
        
def listarAluno():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)  
    try:
        cursor.execute("SELECT * FROM alunos")
        tecnicos = cursor.fetchall()
        return tecnicos
    except mysql.connector.Error as error:
        print("Erro ao buscar aluno:", error)
        return []
    finally:
        cursor.close()
        conn.close()
        
def atualizarAluno(nProcesso, novoAluno):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE alunos SET NomeAluno = %s WHERE nProcesso = %s",
            (novoAluno, nProcesso)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar aluno:", error)
        return False
    finally:
        cursor.close()
        conn.close()

def deletarAluno(nProcesso):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM alunos WHERE nProcesso = %s",
            (nProcesso,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar aluno:", error)
        return False
    finally:
        cursor.close()
        conn.close()

        