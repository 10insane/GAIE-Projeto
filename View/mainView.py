import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import *

UTILIZADOR_CORRETO = "admin"
PALAVRA_PASSE_CORRETA = "admin123"


def main(page: ft.Page):
    page.title = "GAIE - Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = False

    # Lottie animado para o login
    animacao_lottie = fl.Lottie(
        src="https://raw.githubusercontent.com/xvrh/lottie-flutter/refs/heads/master/example/assets/Logo/LogoSmall.json",
        reverse=False,
        animate=True,
        width=150,
        height=150,
    )

    campo_utilizador = ft.TextField(
        label="Utilizador",
        prefix_icon=ft.Icons.PERSON,
        autofocus=True,
        width=300,
    )
    campo_palavra_passe = ft.TextField(
        label="Palavra-passe",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        width=300,
    )
    mensagem_erro = ft.Text(color=ft.Colors.RED)

    def abrir_modal(e):
        pass

    def carregar_tela_principal():
        page.clean()
        page.title = "GAIE - Área Principal"
        page.vertical_alignment = None
        page.horizontal_alignment = None
        page.scroll = True

        cabecalho = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Gaie",
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        font_family="Roboto",
                        weight=ft.FontWeight.BOLD
                    ),
                    margin=ft.margin.only(left=10)  
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Inserir Aluno",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=abrir_modal
                ),
                ft.ElevatedButton(
                    "Inserir Escolas",
                    icon=ft.Icons.SCHOOL,
                    on_click=abrir_modal
                ),
                ft.ElevatedButton(
                    "Inserir Técnico",
                    icon=ft.Icons.ENGINEERING,
                    on_click=abrir_modal
                ),
                ft.ElevatedButton(
                    "Estado do Processo",
                    icon=ft.Icons.ASSIGNMENT_TURNED_IN,
                    on_click=abrir_modal
                ),
                ft.ElevatedButton(
                    "Problemática SPO",
                    icon=ft.Icons.REPORT_PROBLEM,
                    on_click=abrir_modal
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        page.add(cabecalho)

    def autenticar(e):
        if campo_utilizador.value == UTILIZADOR_CORRETO and campo_palavra_passe.value == PALAVRA_PASSE_CORRETA:
            carregar_tela_principal()
        else:
            mensagem_erro.value = "Utilizador ou palavra-passe incorretos!"
            page.update()

    botao_entrar = ft.ElevatedButton(
        "Entrar",
        icon=ft.Icons.LOGIN,
        on_click=autenticar
    )

    def carregar_login():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        login_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        animacao_lottie,
                        ft.Text("Login", style=ft.TextThemeStyle.HEADLINE_SMALL),
                        campo_utilizador,
                        campo_palavra_passe,
                        botao_entrar,
                        mensagem_erro,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
                width=400,
            ),
            elevation=10,
        )

        page.add(login_card)

    carregar_login()


ft.app(target=main, view=ft.WEB_BROWSER)
