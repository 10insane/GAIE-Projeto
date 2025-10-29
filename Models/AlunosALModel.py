from Models.bd_connection import *
import mysql.connector


def criarAlunoAL(nProcessoAluno, anoLetivo):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        #verificar se ja existe. O idAlunoAL nao entra no inserir porque é autoIncrement
        cursor.execute("SELECT nProcessoAluno FROM alunos WHERE nProcessoAluno = %s", (nProcessoAluno,))
        aluno = cursor.fetchone()
        if not aluno:
            print(f"Erro: O aluno com o número de processo {nProcessoAluno} não existe.")
            return False

        cursor.execute(
            """
            SELECT * FROM alunosal
            WHERE nProcessoAluno = %s AND AnoLetivo = %s
            """,
            (nProcessoAluno, anoLetivo)
        )
        existe = cursor.fetchone()
        if existe:
            print(f"O aluno {nProcessoAluno} já está associado ao ano letivo {anoLetivo}.")
            return False

        cursor.execute(
            """
            INSERT INTO alunosal (nProcessoAluno, AnoLetivo)
            VALUES (%s, %s)
            """,
            (nProcessoAluno, anoLetivo)
        )
        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao associar o aluno ao ano letivo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def listarAlunosAL():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT al.idAlunoAL, a.nProcessoAluno, a.NomeAluno, a.Ano, a.Turma,
                   e.NomeEscola, al.AnoLetivo
            FROM alunosal al
            JOIN alunos a ON al.nProcessoAluno = a.nProcessoAluno
            JOIN escolas e ON a.idEscola = e.idEscola
            ORDER BY al.AnoLetivo DESC, a.NomeAluno
        """)
        alunos_al = cursor.fetchall()
        return alunos_al
    except mysql.connector.Error as erro:
        print("Erro ao listar os alunos/anos letivos:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarAlunoAL(idAlunoAL, novoAnoLetivo):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunosal
            SET AnoLetivo = %s
            WHERE idAlunoAL = %s
            """,
            (novoAnoLetivo, idAlunoAL)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar o registo aluno/ano letivo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarAlunoAL(idAlunoAL):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM alunosal WHERE idAlunoAL = %s", (idAlunoAL,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar o registo aluno/ano letivo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
