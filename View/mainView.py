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
    # PÁGINA PRINCIPAL (melhorada)
    # ==========================
    def carregar_tela_principal():
        page.clean()
        page.title = "GAIE - Área Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = "#F5F6FA"
        page.scroll = True

        # ----- Drawer -----
        drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Inserir Aluno",
                    icon=ft.Icons.PERSON_ADD_OUTLINED,
                ),
                ft.NavigationDrawerDestination(
                    label="Inserir Escolas",
                    icon=ft.Icons.SCHOOL_OUTLINED,
                ),
                ft.NavigationDrawerDestination(
                    label="Inserir Técnico",
                    icon=ft.Icons.ENGINEERING_OUTLINED,
                ),
                ft.Divider(thickness=1),
                ft.NavigationDrawerDestination(
                    label="Estado do Processo",
                    icon=ft.Icons.ASSIGNMENT_TURNED_IN_OUTLINED,
                ),
                ft.NavigationDrawerDestination(
                    label="Problemática SPO",
                    icon=ft.Icons.REPORT_PROBLEM_OUTLINED,
                ),
            ],
            position=ft.NavigationDrawerPosition.END,
        )

        # ----- Cabeçalho -----
        cabecalho = ft.Container(
            bgcolor="#8A2BE2",
            padding=15,
            content=ft.Row(
                [
                    ft.Text(
                        "GAIE",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        icon_color=ft.Colors.WHITE,
                        icon_size=30,
                        tooltip="Abrir menu",
                        on_click=lambda e: page.open(drawer),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        # ----- Cartões principais -----
        def criar_card(titulo, descricao, icone, cor):
            return ft.Container(
                bgcolor=cor,
                width=250,
                height=160,
                border_radius=15,
                padding=20,
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.2)"),
                content=ft.Column(
                    [
                        ft.Icon(icone, size=50, color="white"),
                        ft.Text(
                            titulo,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            descricao,
                            size=13,
                            color="white",
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            )

        cards = ft.Row(
            [
                criar_card("Inserir Aluno", "Adicionar novos alunos ao sistema", ft.Icons.PERSON_ADD, "#6C63FF"),
                criar_card("Inserir Escolas", "Gerir lista de escolas", ft.Icons.SCHOOL, "#FF6584"),
                criar_card("Inserir Técnico", "Cadastrar técnicos", ft.Icons.ENGINEERING, "#00C49A"),
            ],
            wrap=True,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        cards2 = ft.Row(
            [
                criar_card("Estado do Processo", "Acompanhar o progresso", ft.Icons.ASSIGNMENT_TURNED_IN, "#0088FE"),
                criar_card("Problemática SPO", "Ver relatórios e alertas", ft.Icons.REPORT_PROBLEM, "#FFBB28"),
            ],
            wrap=True,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        conteudo = ft.Column(
            [
                ft.Container(height=20),
                ft.Text(
                    "Bem-vindo à Área Principal do GAIE!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#2F2F2F",
                ),
                ft.Text(
                    "Selecione uma das opções abaixo para começar:",
                    size=16,
                    color="#4F4F4F",
                ),
                ft.Container(height=30),
                cards,
                ft.Container(height=20),
                cards2,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        page.add(
            ft.Column(
                [
                    cabecalho,
                    ft.Container(padding=30, content=conteudo),
                ],
                expand=True,
            )
        )

    # ==========================
    # LOGIN
    # ==========================
    def autenticar(e):
        if (
            campo_utilizador.value == UTILIZADOR_CORRETO
            and campo_palavra_passe.value == PALAVRA_PASSE_CORRETA
        ):
            carregar_tela_principal()
        else:
            mensagem_erro.value = "Utilizador ou palavra-passe incorretos!"
            page.update()

    botao_entrar = ft.ElevatedButton(
        "Entrar",
        icon=ft.Icons.LOGIN,
        on_click=autenticar,
        bgcolor="#8A2BE2",
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    # ==========================
    # LOGIN SCREEN
    # ==========================
    def carregar_login():
        page.clean()
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = None

        fundo_com_gradiente = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#E90000", "#FAA6FF"],
            ),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        animacao_lottie,
                                        ft.Text(
                                            "Login",
                                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
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
                                padding=40,
                                width=400,
                                border_radius=20,
                                bgcolor="rgba(0, 0, 0, 0.4)",
                                border=ft.border.all(2, ft.Colors.WHITE70),
                                shadow=ft.BoxShadow(
                                    spread_radius=2,
                                    blur_radius=8,
                                    color="rgba(0,0,0,0.5)",
                                    offset=ft.Offset(2, 2),
                                ),
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
