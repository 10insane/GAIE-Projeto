from Models.TecnicoModel import *

def Criar( nProcTecnico, nomeTecnicos):
    return criarTecnico(nProcTecnico, nomeTecnicos)

def Listar():
    return listarTecnico()

def atualizar(nProcTecnico, novoNome):
    return atualizarTecnico(nProcTecnico, novoNome)

def deletar(nProcTecnico):
    return deletarTecnico(nProcTecnico)