import flet as ft
from Models.TecnicoModel import criarTecnico

def CreateTecnico(page: ft.Page):
    # === CORES (Mesmas da tela principal) ===
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
    cor_texto_medio = "#334155"
    cor_texto_claro = "#64748B"
    cor_borda = "#E2E8F0"

    # === FUNÇÃO DE VALIDAÇÃO ===
    def LimitarNumero(e):
        valor = ''.join(filter(str.isdigit, e.control.value))
        if len(valor) > 10:
            valor = valor[:10]
        e.control.value = valor
        page.update()

    # === CAMPOS DO FORMULÁRIO ===
    campoNovoNumero = ft.TextField(
        label="Nº Processo Técnico",
        hint_text="Ex: 1234567890",
        prefix_icon=ft.Icons.BADGE_ROUNDED,
        width=500,
        autofocus=True,
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        text_size=15,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
        on_change=LimitarNumero,
    )

    campoNovoNome = ft.TextField(
        label="Nome Completo do Técnico",
        hint_text="Ex: João Silva Costa",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        width=500,
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        text_size=15,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
    )

    campoNovaSenha = ft.TextField(
        label="Password",
        hint_text="Digite uma password segura",
        prefix_icon=ft.Icons.LOCK_ROUNDED,
        width=500,
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        text_size=15,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
        password=True,  # oculta os caracteres
        can_reveal_password=True,  # permite mostrar/esconder senha
    )

    # === FUNÇÃO SALVAR TÉCNICO ===
    def salvarTecnico(e):
        nProc = campoNovoNumero.value.strip()
        nome = campoNovoNome.value.strip()
        senha = campoNovaSenha.value.strip()

        if not nProc or not nome or not senha:
            page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.WHITE),
                        ft.Text("Preencha todos os campos!", color=ft.Colors.WHITE, size=14),
                    ],
                    spacing=10,
                ),
                bgcolor="#F59E0B",
            )
            page.snack_bar.open = True
            page.update()
            return

        if criarTecnico(nProc, nome, senha):
            page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.WHITE),
                        ft.Text("Técnico criado com sucesso!", color=ft.Colors.WHITE, size=14),
                    ],
                    spacing=10,
                ),
                bgcolor="#10B981",
            )
            page.snack_bar.open = True
            page.update()
            page.go("/Config")
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ERROR_ROUNDED, color=ft.Colors.WHITE),
                        ft.Text("Erro ao criar técnico!", color=ft.Colors.WHITE, size=14),
                    ],
                    spacing=10,
                ),
                bgcolor="#DC2626",
            )
            page.snack_bar.open = True
            page.update()

    # === BOTÕES DE AÇÃO ===
    botaoSalvar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Criar Técnico", size=15, weight=ft.FontWeight.W_600),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=salvarTecnico,
        bgcolor=cor_primaria,
        color=ft.Colors.WHITE,
        width=240,
        height=52,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=3,
        ),
    )

    botaoCancelar = ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=20, color=cor_texto_medio),
                ft.Text("Voltar a Configurações", size=15, weight=ft.FontWeight.W_600, color=cor_texto_medio),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=lambda e: page.go("/Config"),
        width=240,
        height=52,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            side=ft.BorderSide(2, cor_borda),
        ),
    )

    # === LINHA DE BOTÕES ===
    botoesAcao = ft.Row(
        [botaoSalvar, botaoCancelar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )

    # === CARD PRINCIPAL ===
    cardPrincipal = ft.Container(
        content=ft.Column(
            [
                # Cabeçalho com ícone
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, color=cor_primaria, size=40),
                                bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                                padding=18,
                                border_radius=16,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(bottom=10),
                ),

                # Título
                ft.Text(
                    "Criar Novo Técnico",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_escuro,
                    text_align=ft.TextAlign.CENTER,
                ),

                # Subtítulo
                ft.Text(
                    "Preencha os dados abaixo para registar um novo técnico no sistema",
                    size=14,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Container(height=20),

                # Campos do formulário
                campoNovoNumero,
                campoNovoNome,
                campoNovaSenha,

                ft.Container(height=10),

                # Botões
                botoesAcao,

                # Informação adicional
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.INFO_ROUNDED, size=16, color=cor_texto_claro),
                            ft.Text(
                                "O número do processo deve ter até 10 dígitos",
                                size=12,
                                color=cor_texto_claro,
                                italic=True,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(top=16),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        ),
        bgcolor=cor_card,
        padding=50,
        border_radius=20,
        width=600,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=30,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        border=ft.border.all(1, cor_borda),
    )

    # === LOGO/MARCA NO TOPO ===
    logoTopo = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.WHITE, size=32),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    padding=12,
                    border_radius=12,
                ),
                ft.Column(
                    [
                        ft.Text("GAIE", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Gestão Integrada de Alunos e Educação", size=13, color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE)),
                    ],
                    spacing=0,
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(bottom=40),
    )

    # === LAYOUT COMPLETO ===
    layoutCompleto = ft.Container(
        content=ft.Column(
            [
                logoTopo,
                cardPrincipal,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[cor_primaria, "#3B82F6", "#60A5FA"],
        ),
        expand=True,
        padding=40,
    )

    return ft.View(
        route="/criar-tecnico",
        controls=[layoutCompleto],
        bgcolor=cor_primaria,
    )
