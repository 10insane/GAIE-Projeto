from Models.EstadoProcessos import *

def Criar(IdEstadoProcesso, Estado):
    return criarEstadoProcesso(IdEstadoProcesso, Estado)

def Listar():
    return listarEstadoProcesso()

def atualizar(IdEstadoProcesso, novoEstadoProcesso):
    return atualizarEstadoProcesso(IdEstadoProcesso, novoEstadoProcesso)

def deletar(IdEstadoProcesso):
    return deletarEstadoProcesso(IdEstadoProcesso)