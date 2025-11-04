from Models.TecnicoModel import *

def Criar( nProcTecnico, nomeTecnico):
    return criarTecnico(nProcTecnico, nomeTecnico)

def Listar():
    return listarTecnico()

def atualizar(nProcTecnico, novoNome):
    return atualizarTecnico(nProcTecnico, novoNome)

def deletar(nProcTecnico):
    return deletarTecnico(nProcTecnico)