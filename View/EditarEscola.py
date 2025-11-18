import flet as ft
from Models.EscolasModel import *

def PaginaEditarEscola(page: ft.Page):
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"

    # Buscar ID que veio pela sessão
    id_escola = page.session.get("escola_editar_id")

    if not id_escola:
        return ft.Text("Erro: Nenhuma escola selecionada para edição.")

    # Buscar dados da escola
    escolas = listarEscolas()
    escola = next((e for e in escolas if e["idEscola"] == id_escola), None)

    if not escola:
        return ft.Text("Erro: Escola não encontrada.")

    nome_input = ft.TextField(
        label="Nome da Escola",
        width=300,
        value=escola["NomeEscola"]
    )

    mensagem = ft.Text("", size=14, color="#16A34A")

    def atualizar(e):
        novo_nome = nome_input.value.strip()

        if not novo_nome:
            mensagem.value = "⚠️ Preenche o Nome da escola."
            mensagem.color = "#DC2626"
            page.update()
            return

        if atualizarEscola(id_escola, novo_nome):
            mensagem.value = "✅ Escola atualizada com sucesso!"
            mensagem.color = "#16A34A"
            page.update()
            page.go("/pagina-principal")
        else:
            mensagem.value = "❌ Erro ao atualizar escola."
            mensagem.color = "#DC2626"
            page.update()

    conteudo = ft.Container(
        content=ft.Column([
            ft.Text("Editar Escola", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
            ft.Container(height=20),
            nome_input,
            ft.Container(height=10),
            mensagem,
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton("Guardar", bgcolor=cor_primaria, color="white", on_click=atualizar),
                ft.OutlinedButton("Cancelar", on_click=lambda e: page.go("/pagina-principal")),
            ], spacing=15),
        ], spacing=10),
        bgcolor=cor_card,
        padding=30,
        border_radius=16,
        expand=False,
    )

    return ft.View(
        route="/EditarEscola",
        controls=[conteudo],
        bgcolor=cor_fundo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
