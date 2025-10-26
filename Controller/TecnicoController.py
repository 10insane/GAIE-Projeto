from Models.TecnicoModel import *

def Criar(idTecnico, nProcTecnico, nomeTecnicos):
    return criarTecnico(idTecnico, nProcTecnico, nomeTecnicos)

def Listar():
    return listarTecnico()

def atualizar(nProcTecnico, novoNome):
    return atualizarTecnico(nProcTecnico, novoNome)

def deletar(nProcTecnico):
    return deletarTecnico(nProcTecnico)