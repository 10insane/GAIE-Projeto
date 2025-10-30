import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import listarTecnico, criarTecnico

def main(page: ft.Page):
    page.title = "GAIE - Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = False

    # ==========================
    # CAMPOS LOGIN
    # ==========================
    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        reverse=False,
        animate=True,
        width=150,
        height=150,
    )

    campoNumeroProcesso = ft.TextField(
        label="Nº Processo Técnico",
        prefix_icon=ft.Icons.BADGE,
        autofocus=True,
        width=300,
    )

    campoNomeTecnico = ft.TextField(
        label="Nome do Técnico",
        prefix_icon=ft.Icons.PERSON,
        width=300,
    )

    mensagemErro = ft.Text(color=ft.Colors.RED)

    # ==========================
    # TELA PRINCIPAL DO SISTEMA
    # ==========================
    def carregarTelaPrincipal(tecnicoNome):
        page.clean()
        page.title = "GAIE - Área Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = "#F5F6FA"
        page.scroll = True

        # Conteúdo simplificado
        page.add(ft.Text(f"Bem-vindo {tecnicoNome} à área principal!", size=24))
        page.update()

    # ==========================
    # TELA DE CRIAÇÃO DE TÉCNICO
    # ==========================
    def carregarTelaCriarTecnico(pref_nProc="", pref_nome=""):
        page.clean()
        page.title = "GAIE - Criar Técnico"

        campoNovoNumero = ft.TextField(label="Nº Processo Técnico", value=pref_nProc)
        campoNovoNome = ft.TextField(label="Nome do Técnico", value=pref_nome)
        mensagemSnack = ft.Text(color=ft.Colors.RED)

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
                carregarLogin()  # Volta para a tela de login
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao criar técnico!"))
                page.snack_bar.open = True
                page.update()

        # Layout da tela
        page.add(
            ft.Column(
                [
                    ft.Text("Criar Novo Técnico", size=24, weight=ft.FontWeight.BOLD),
                    campoNovoNumero,
                    campoNovoNome,
                    ft.Row(
                        [
                            ft.ElevatedButton("Salvar", on_click=salvarTecnico, icon=ft.Icons.SAVE),
                            ft.TextButton("Cancelar", on_click=lambda e: carregarLogin()),
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            )
        )
        page.update()

    # ==========================
    # AUTENTICAÇÃO
    # ==========================
    def autenticar(e):
        nProc = campoNumeroProcesso.value.strip()
        nome = campoNomeTecnico.value.strip()

        if not nProc or not nome:
            mensagemErro.value = "Preencha ambos os campos!"
            page.update()
            return

        tecnicos = listarTecnico()
        tecnicoExiste = any(
            str(t["nProcTecnico"]) == nProc and t["nomeTecnicos"].lower() == nome.lower()
            for t in tecnicos
        )

        if tecnicoExiste:
            carregarTelaPrincipal(nome)
        else:
            mensagemErro.value = "Técnico não encontrado! Deseja criar um novo?"
            botaoCriar.visible = True
            page.update()

    # ==========================
    # BOTÕES
    # ==========================
    botaoEntrar = ft.ElevatedButton(
        "Entrar",
        icon=ft.Icons.LOGIN,
        on_click=autenticar,
        bgcolor="#8A2BE2",
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    botaoCriar = ft.ElevatedButton(
        "Criar Técnico",
        icon=ft.Icons.PERSON_ADD,
        bgcolor="#00C49A",
        color=ft.Colors.WHITE,
        visible=False,
        on_click=lambda e: carregarTelaCriarTecnico(
            pref_nProc=campoNumeroProcesso.value,
            pref_nome=campoNomeTecnico.value,
        ),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    botoesLogin = ft.Row(
        [botaoEntrar, botaoCriar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # ==========================
    # LOGIN SCREEN
    # ==========================
    def carregarLogin():
        page.clean()
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = None
        botaoCriar.visible = False

        fundoComGradiente = ft.Container(
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
                                        animacaoLottie,
                                        ft.Text(
                                            "Login do Técnico",
                                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
                                        ),
                                        campoNumeroProcesso,
                                        campoNomeTecnico,
                                        botoesLogin,
                                        mensagemErro,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                                padding=40,
                                width=400,
                                border_radius=20,
                                bgcolor="rgba(0, 0, 0, 0.8)",
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

        page.add(fundoComGradiente)
        page.update()

    carregarLogin()

ft.app(target=main, view=ft.WEB_BROWSER)
