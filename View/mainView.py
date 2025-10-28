import flet as ft
import flet_lottie as fl

UTILIZADOR_CORRETO = "admin"
PALAVRA_PASSE_CORRETA = "admin123"


def main(page: ft.Page):
    page.title = "GAIE - Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = False

    # ==========================
    # CAMPOS LOGIN
    # ==========================
    animacao_lottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
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

    # ==========================
    # PÁGINA PRINCIPAL
    # ==========================
    def carregar_tela_principal():
        page.clean()
        page.title = "GAIE - Área Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = True
        page.bgcolor = ft.Colors.WHITE
        page.gradient = None

        # ----- DRAWER (menu lateral direito) -----
        def handle_dismissal(e):
            print("Drawer fechado!")

        def handle_change(e):
            print(f"Selecionado: {e.control.selected_index}")
            page.close(drawer)

        drawer = ft.NavigationDrawer(
            on_dismiss=handle_dismissal,
            on_change=handle_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Inserir Aluno",
                    icon=ft.Icons.PERSON_ADD_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.PERSON_ADD),
                ),
                ft.NavigationDrawerDestination(
                    label="Inserir Escolas",
                    icon=ft.Icons.SCHOOL_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.SCHOOL),
                ),
                ft.NavigationDrawerDestination(
                    label="Inserir Técnico",
                    icon=ft.Icons.ENGINEERING_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.ENGINEERING),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Estado do Processo",
                    icon=ft.Icons.ASSIGNMENT_TURNED_IN_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.ASSIGNMENT_TURNED_IN),
                ),
                ft.NavigationDrawerDestination(
                    label="Problemática SPO",
                    icon=ft.Icons.REPORT_PROBLEM_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.REPORT_PROBLEM),
                ),
            ],
            position=ft.NavigationDrawerPosition.END,  # <-- faz abrir do lado direito
        )

        # ----- Cabeçalho -----
        cabecalho = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "GAIE",
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    margin=ft.margin.only(left=10),
                ),
                ft.Container(expand=True),
                # Ícone de menu hamburguer maior
                ft.IconButton(
                    icon=ft.Icons.MENU,           # ← 3 barras
                    icon_color=ft.Colors.BLACK,
                    icon_size=35,                 # ← tamanho aumentado
                    tooltip="Abrir menu",
                    on_click=lambda e: page.open(drawer),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # ----- Conteúdo da página -----
        conteudo = ft.Column(
            [
                ft.Text(
                    "Bem-vindo à área principal do GAIE!",
                    style=ft.TextThemeStyle.HEADLINE_SMALL,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                ft.Text(
                    "Aqui poderás gerir alunos, escolas, técnicos e processos.",
                    color=ft.Colors.BLACK,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        page.add(
            ft.Column(
                [
                    cabecalho,
                    ft.Divider(),
                    conteudo,
                ],
                expand=True,
                spacing=10,
            )
        )

    # ==========================
    # LOGIN
    # ==========================
    def autenticar(e):
        if campo_utilizador.value == UTILIZADOR_CORRETO and campo_palavra_passe.value == PALAVRA_PASSE_CORRETA:
            carregar_tela_principal()
        else:
            mensagem_erro.value = "Utilizador ou palavra-passe incorretos!"
            page.update()

    botao_entrar = ft.ElevatedButton("Entrar", icon=ft.Icons.LOGIN, on_click=autenticar)

    def carregar_login():
        page.clean()
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = None

        fundo_com_gradiente = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#FF8C00", "#FF69B4"],
            ),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            animacao_lottie,
                                            ft.Text(
                                                "Login",
                                                style=ft.TextThemeStyle.HEADLINE_SMALL,
                                                weight=ft.FontWeight.BOLD,
                                            ),
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
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )

        page.add(fundo_com_gradiente)

    carregar_login()


ft.app(target=main, view=ft.WEB_BROWSER)
