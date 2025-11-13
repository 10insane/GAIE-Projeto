from Models.bd_connection import *
from Models.ProblematicaSPO import criarProblematica
from datetime import date
import mysql.connector

from Models.bd_connection import *
from Models.ProblematicaSPO import criarProblematica
from datetime import date
import mysql.connector

def criarRegisto(nProcessoAluno, idEstado, DataArquivo, Observacoes, tipoProblematica, nProcTecnico=None):
    """
    Cria um registo no Registos e uma problemática nova se fornecida.
    """
    # 1️⃣ Criar problemática e pegar o ID
    idProblematica = criarProblematica(tipoProblematica)
    if not idProblematica:
        print("Erro ao criar problemática.")
        return False

    # 2️⃣ Preparar datas
    dataEntradaSPO = date.today()
    dataInicio = None

    # 3️⃣ Inserir registo
    conn = bd_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Registos 
            (nPIA, nProcessoAluno, nProcTecnico, idEstado, idProblematica, DataEntradaSPO, DataInicio, DataArquivo, Observacoes)
            VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nProcessoAluno, nProcTecnico, idEstado, idProblematica, dataEntradaSPO, dataInicio, DataArquivo, Observacoes)
        )
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao criar registo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()



def listarRegistos():
    conn = bd_connection()
    if not conn:
        return []

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


def atualizarRegisto(idRegisto, novoIdEstado, novaData, novaObservacoes, novoNProcTecnico=None):
    conn = bd_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE registos SET idEstado=%s, DataArquivo=%s, Observacoes=%s, nProcTecnico=%s WHERE nPIA=%s",
            (novoIdEstado, novaData, novaObservacoes, novoNProcTecnico, idRegisto)
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
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM registos WHERE nPIA = %s", (idRegisto,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print("Erro ao eliminar o registo:", erro)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
