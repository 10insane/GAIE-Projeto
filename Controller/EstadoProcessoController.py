from Models.EstadoProcessos import *

def Criar(idEstado, Estado):
    return criarEstado(idEstado, Estado)

def Listar():
    return listarEstados()

def atualizar(idEstado, novoEstadoProcesso):
    return atualizarEstado(idEstado, novoEstadoProcesso)

def deletar(idEstado):
    return eliminarEstado(idEstado)