from Models.bd_connection import *
import mysql.connector

def criarAluno(nProcessoAluno, nomeAluno,ano, turma, idEscola):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT idEscola FROM escolas WHERE idEscola = %s", (idEscola,))
        escola = cursor.fetchone()
        if not escola:
            print(f"Erro: A escola com o ID {idEscola} não existe.")
            return False

        cursor.execute(
            """
            INSERT INTO alunos (nProcessoAluno, NomeAluno, Ano, Turma, idEscola)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nProcessoAluno, nomeAluno, ano, turma, idEscola)
        )
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao inserir o aluno:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def listarAlunos():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.*, e.NomeEscola
            FROM alunos a
            JOIN escolas e ON a.idEscola = e.idEscola
        """)
        alunos = cursor.fetchall()
        return alunos
    except mysql.connector.Error as erro:
        print("Erro ao listar os alunos:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarAluno(nProcessoAluno, novoNome, novoAno, novaTurma, novoIdEscola):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        if novoIdEscola:
            cursor.execute("SELECT idEscola FROM escolas WHERE idEscola = %s", (novoIdEscola,))
            escola = cursor.fetchone()
            if not escola:
                print(f"Erro: A escola com o ID {novoIdEscola} não existe.")
                return False

        cursor.execute(
            """
            UPDATE alunos
            SET NomeAluno = %s, Ano = %s, Turma = %s, idEscola = %s
            WHERE nProcessoAluno = %s
            """,
            (novoNome, novoAno, novaTurma, novoIdEscola, nProcessoAluno)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar o aluno:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarAluno(nProcessoAluno):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM alunos WHERE nProcessoAluno = %s", (nProcessoAluno,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar o aluno:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
