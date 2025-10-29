from Models.AlunosALModel import *

def Criar( nProcessoAluno, anoLetivo):
    return criarAlunoAL(nProcessoAluno, anoLetivo)

def Listar():
    return listarAlunosAL()

def atualizar(idAlunoAL, novoAnoLetivo):
    return atualizarAlunoAL(idAlunoAL, novoAnoLetivo)

def deletar(idAlunoAL):
    return eliminarAlunoAL(idAlunoAL)