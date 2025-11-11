from Models.EscolasModel import *

def Criar(IdEscola, nomeEscola):
    return criarEscola(IdEscola, nomeEscola)

def Listar():
    return listarEscolas()

def atualizar(IdEscola, novoNome):
    return atualizarEscola(IdEscola, novoNome)

def deletar(IdEscola):
    return deletarEscola(IdEscola)