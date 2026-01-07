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


def atualizarEscola(IdEscola, novoNome):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE escolas SET NomeEscola = %s WHERE IdEscola = %s",
            (novoNome, IdEscola)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar escola:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarEscola(IdEscola):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM escolas WHERE IdEscola = %s",
            (IdEscola,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar escola:", error)
        return False
    finally:
        cursor.close()
        conn.close()

def buscarEscolaPorId(IdEscola):
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM escolas WHERE IdEscola = %s",
            (IdEscola,)
        )
        escola = cursor.fetchone()  
        return escola  
    except mysql.connector.Error as error:
        print("Erro ao buscar escola:", error)
        return None
    finally:
        cursor.close()
        conn.close()
        
def contarAlunosPorEscola(IdEscola):
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT COUNT(*) AS total_alunos FROM alunos WHERE IdEscola = %s",
            (IdEscola,)
        )
        resultado = cursor.fetchone()
        return resultado["total_alunos"]
    except mysql.connector.Error as error:
        print("Erro ao contar alunos:", error)
        return 0
    finally:
        cursor.close()
        conn.close()
        
def listarEscolasComTotalAlunos():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.IdEscola, e.NomeEscola, COUNT(a.IdAluno) AS total_alunos
            FROM escolas e
            LEFT JOIN alunos a ON e.IdEscola = a.IdEscola
            GROUP BY e.IdEscola, e.NomeEscola
        """)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print("Erro ao listar escolas com alunos:", error)
        return []
    finally:
        cursor.close()
        conn.close()
