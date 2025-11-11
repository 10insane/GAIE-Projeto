from Models.EstadoProcessos import listarEstados, criarEstado, atualizarEstado, eliminarEstado

def Criar(idEstado, Estado):
    return criarEstado(idEstado, Estado)

def Listar():
    return listarEstados()

def Atualizar(idEstado, novoEstadoProcesso):
    return atualizarEstado(idEstado, novoEstadoProcesso)

def Deletar(idEstado):
    return eliminarEstado(idEstado)
