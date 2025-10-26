from Models.ProblematicaSPO import *

def Criar(IdProblematicaSPO, Tipo):
    return criarProblematica(IdProblematicaSPO, Tipo)

def Listar():
    return listarProblematicas()

def atualizar(IdProblematicaSPO, novoTipo):
    return atualizarProblematica(IdProblematicaSPO, novoTipo)

def deletar(IdProblematicaSPO):
    return deletarProblematica(IdProblematicaSPO)