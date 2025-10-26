from Models.bd_connection import *
import mysql.connector


def criarProblematica(IdProblematicaSPO, Tipo):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ProblematicasSPO (IdProblematicaSPO, Tipo) VALUES (%s, %s)",
            (IdProblematicaSPO, Tipo)
        )
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Erro ao inserir ProblematicasSPO:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def listarProblematicas():
    conn = bd_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ProblematicasSPO")
        problematicas = cursor.fetchall()
        return problematicas
    except mysql.connector.Error as error:
        print("Erro ao listar ProblematicasSPO:", error)
        return []
    finally:
        cursor.close()
        conn.close()


def atualizarProblematica(IdProblematicaSPO, novoTipo):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE ProblematicasSPO SET Tipo = %s WHERE IdProblematicaSPO = %s",
            (novoTipo, IdProblematicaSPO)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao atualizar ProblematicasSPO:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def deletarProblematica(IdProblematicaSPO):
    conn = bd_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM ProblematicasSPO WHERE IdProblematicaSPO = %s",
            (IdProblematicaSPO,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as error:
        print("Erro ao deletar ProblematicasSPO:", error)
        return False
    finally:
        cursor.close()
        conn.close()
