from Models.AlunosModel import *

def Criar(nProcessoAluno, nomeAluno, idEscola, ano, turma):
    return criarAluno(nProcessoAluno, nomeAluno, idEscola, ano, turma)

def Listar():
    return listarAluno()

def atualizar(nProcessoAluno, novoNome, novoAno, novaTurma, novoIdEscola):
    return atualizarAluno(nProcessoAluno, novoNome, novoAno, novaTurma, novoIdEscola)

def deletar(nProcessoAluno):
    return deletarAluno(nProcessoAluno)