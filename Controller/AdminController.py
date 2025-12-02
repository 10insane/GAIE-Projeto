from Models.AdminModel import *

def Criar( nProcAdmin, nomeTecnico):
    return criarAdmin(nProcAdmin, nomeTecnico)

def Listar():
    return listarAdmin()

def atualizar(nProcAdmin, novoNome):
    return atualizarAdmin(nProcAdmin, novoNome)

def deletar(nProcAdmin):
    return deletarAdmin(nProcAdmin)