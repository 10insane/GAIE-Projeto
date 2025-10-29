from Models.ProblematicaSPO import *

def Criar(idProblematica, tipoProblematica):
    return criarProblematica(idProblematica, tipoProblematica)

def Listar():
    return listarProblematicas()

def atualizar(idProblematica, novoTipo):
    return atualizarProblematica(idProblematica, novoTipo)

def deletar(idProblematica):
    return eliminarProblematica(idProblematica)