import flet as ft
from Models.TecnicoModel import criarTecnico

def CreateTecnico(page: ft.Page):
    campoNovoNumero = ft.TextField(label="Nº Processo Técnico")
    campoNovoNome = ft.TextField(label="Nome do Técnico")

    def salvarTecnico(e):
        nProc = campoNovoNumero.value.strip()
        nome = campoNovoNome.value.strip()

        if not nProc or not nome:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return

        if criarTecnico(nProc, nome):
            page.snack_bar = ft.SnackBar(ft.Text("✅ Técnico criado com sucesso!"))
            page.snack_bar.open = True
            page.go("/login")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao criar técnico!"))
            page.snack_bar.open = True
            page.update()

    conteudo = ft.Column(
        [
            ft.Text("Criar Novo Técnico", size=24, weight=ft.FontWeight.BOLD),
            campoNovoNumero,
            campoNovoNome,
            ft.Row([
                ft.ElevatedButton("Salvar", on_click=salvarTecnico),
                ft.TextButton("Cancelar", on_click=lambda e: page.go("/login")),
            ]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    return ft.View(
        route="/criar-tecnico",
        controls=[ft.Container(expand=True, content=conteudo)],
    )
