from Models.TecnicoModel import *

def Criar(nProcesso, nomeTecnicos):
    return criarTecnico(nProcesso, nomeTecnicos)

def Listar(nProcesso, nomeTecnicos):
    return listarTecnico(nProcesso, nomeTecnicos)

def atualizar(nProcesso, nomeTecnicos):
    return atualizarTecnico(nProcesso, nomeTecnicos)

def deletar(nProcesso):
    return deletarTecnico(nProcesso)