from Models.bd_connection import *
import mysql.connector

def criarRegisto(nProcessoAluno, idEstado, DataArquivo, descricao, nProcTecnico=None):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nProcessoAluno FROM alunos WHERE nProcessoAluno = %s", (nProcessoAluno,))
        if not cursor.fetchone():
            print(f"Erro: O aluno com o processo {nProcessoAluno} não existe.")
            return False

        if nProcTecnico:
            cursor.execute("SELECT nProcTecnico FROM tecnicos WHERE nProcTecnico = %s", (nProcTecnico,))
            if not cursor.fetchone():
                print(f"Erro: O técnico com o processo {nProcTecnico} não existe.")
                return False

        cursor.execute("SELECT idEstado FROM estadosprocesso WHERE idEstado = %s", (idEstado,))
        if not cursor.fetchone():
            print(f"Erro: O estado com ID {idEstado} não existe.")
            return False

        cursor.execute(
            "INSERT INTO registos (nProcessoAluno, idEstado, DataArquivo, descricao, nProcTecnico) VALUES (%s, %s, %s, %s, %s)",
            (nProcessoAluno, idEstado, DataArquivo, descricao, nProcTecnico)
        )
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao inserir o registo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def listarRegistos():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.*, a.NomeAluno, t.NomeTecnico, e.Estado
            FROM registos r
            JOIN alunos a ON r.nProcessoAluno = a.nProcessoAluno
            LEFT JOIN tecnicos t ON r.nProcTecnico = t.nProcTecnico
            LEFT JOIN estadosprocesso e ON r.idEstado = e.idEstado
        """)
        return cursor.fetchall()
    except mysql.connector.Error as erro:
        print("Erro ao listar os registos:", erro)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarRegisto(idRegisto, novoIdEstado, novaData, novaDescricao, novoNProcTecnico=None):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        if novoNProcTecnico:
            cursor.execute("SELECT nProcTecnico FROM tecnicos WHERE nProcTecnico = %s", (novoNProcTecnico,))
            if not cursor.fetchone():
                print(f"Erro: O técnico com o processo {novoNProcTecnico} não existe.")
                return False

        cursor.execute(
            "UPDATE registos SET idEstado=%s, DataArquivo=%s, descricao=%s, nProcTecnico=%s WHERE idRegisto=%s",
            (novoIdEstado, novaData, novaDescricao, novoNProcTecnico, idRegisto)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao atualizar o registo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def eliminarRegisto(idRegisto):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM registos WHERE idRegisto = %s", (idRegisto,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar o registo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
