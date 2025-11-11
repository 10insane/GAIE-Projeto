from Models.AlunosModel import *

def Criar(nProcessoAluno, nomeAluno, IdEscola, ano, turma):
    return criarAluno(nProcessoAluno, nomeAluno, IdEscola, ano, turma)

def Listar():
    return listarAlunos()

def atualizar(nProcessoAluno, novoNome, novoAno, novaTurma, novoIdEscola):
    return atualizarAluno(nProcessoAluno, novoNome, novoAno, novaTurma, novoIdEscola)

def deletar(nProcessoAluno):
    return eliminarAluno(nProcessoAluno)