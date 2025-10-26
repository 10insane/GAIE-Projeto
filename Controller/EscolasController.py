from Models.EscolasModel import *

def Criar(IdEscola, nomeEscola):
    return criarEscola(IdEscola, nomeEscola)

def Listar():
    return listarEscolas()

def atualizar(idEscola, novoNome):
    return atualizarEscola(idEscola, novoNome)

def deletar(idEscola):
    return deletarEscola(idEscola)