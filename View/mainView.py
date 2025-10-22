import flet as ft
from Models.TecnicoModel import *

USUARIO_CORRETO = "admin"
SENHA_CORRETA = "admin123"

def main(page: ft.Page):
    page.title = "GAIE Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Campos e mensagem de login
    username_field = ft.TextField(label="Usuário", prefix_icon=ft.Icons.PERSON)
    password_field = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    login_msg = ft.Text(color=ft.Colors.RED)

    def abrir_modal(e):
        nProcesso_field = ft.TextField(label="Número de Processo")
        nomeTecnico_field = ft.TextField(label="Nome do Técnico")
        mensagem = ft.Text()

        def salvar_tecnico(ev):
            if criarUser(nProcesso_field.value, nomeTecnico_field.value):
                mensagem.value = "Técnico criado com sucesso!"
            else:
                mensagem.value = "Erro ao criar o Técnico"
            modal.content.controls[-1] = mensagem
            page.update()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Novo Técnico", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    nProcesso_field,
                    nomeTecnico_field,
                    ft.ElevatedButton("salvar", on_click=salvar_tecnico),
                    mensagem
                ],
                tight=True
            ),
            on_dismiss=lambda e: None
        )

        page.dialog = modal
        modal.open = True
        page.update()

    def carregar_tela_principal():
        page.clean()
        page.title = "GAIE"
        page.horizontal_alignment = None
        page.vertical_alignment = None

        header = ft.Row(
            controls=[
                ft.Text("GAIE", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Container(expand=True),
                ft.ElevatedButton("Inserir Aluno", icon=ft.Icons.PERSON_ADD, on_click=abrir_modal),
                ft.ElevatedButton("Inserir Escolas", icon=ft.Icons.PERSON_ADD, on_click=abrir_modal),
                ft.ElevatedButton("Inserir Técnico", icon=ft.Icons.PERSON_ADD, on_click=abrir_modal),
                ft.ElevatedButton("Inserir estado processo", icon=ft.Icons.PERSON_ADD, on_click=abrir_modal),
                ft.ElevatedButton("Inserir problemáticaSPO", icon=ft.Icons.PERSON_ADD, on_click=abrir_modal),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        page.add(header)

    def login(e):
        if username_field.value == USUARIO_CORRETO and password_field.value == SENHA_CORRETA:
            carregar_tela_principal()
        else:
            login_msg.value = "Utilizador ou senha incorretos"
            page.update()

    login_button = ft.ElevatedButton("Entrar", on_click=login)

    def carregar_login():
        page.clean()
        page.title = "GAIE Login"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.add(username_field, password_field, login_button, login_msg)

    carregar_login()

ft.app(target=main, view=ft.WEB_BROWSER)
