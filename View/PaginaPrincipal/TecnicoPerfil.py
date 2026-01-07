import flet as ft
from .estilos import *
from Models.TecnicoModel import atualizarTecnico


def PerfilTecnico(tecnico, page):
    """
    View completa do perfil do técnico com design moderno
    """

    # =========================
    # CARD PERFIL PRINCIPAL
    # =========================
    def build_card():
        nome = tecnico.get("NomeTecnico", "Sem Nome")
        nproc = tecnico.get("nProcTecnico", "N/A")

        return ft.Container(
            content=ft.Column(
                [
                    # Avatar com efeito glassmorphism
                    ft.Container(
                        content=ft.Stack(
                            [
                                # Círculo de fundo com blur
                                ft.Container(
                                    width=160,
                                    height=160,
                                    border_radius=80,
                                    bgcolor=ft.Colors.with_opacity(0.15, cor_primaria),
                                    blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
                                ),
                                # Avatar principal
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.PERSON_ROUNDED,
                                        size=90,
                                        color=ft.Colors.WHITE,
                                    ),
                                    width=150,
                                    height=150,
                                    alignment=ft.alignment.center,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=[
                                            cor_primaria,
                                            ft.Colors.with_opacity(0.6, cor_primaria),
                                        ],
                                    ),
                                    border_radius=75,
                                    border=ft.border.all(5, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                    shadow=ft.BoxShadow(
                                        blur_radius=30,
                                        spread_radius=5,
                                        color=ft.Colors.with_opacity(0.3, cor_primaria),
                                        offset=ft.Offset(0, 8),
                                    ),
                                ),
                            ],
                            width=160,
                            height=160,
                        ),
                    ),
                    
                    ft.Container(height=24),
                    
                    # Nome do técnico com destaque
                    ft.Container(
                        content=ft.Text(
                            nome,
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    
                    ft.Container(height=12),

                    # Badge profissional do nº de processo
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Número de Processo",
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                    color=ft.Colors.with_opacity(0.7, cor_texto_claro),
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Container(height=4),
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.FINGERPRINT,
                                            size=22,
                                            color=cor_primaria,
                                        ),
                                        ft.Text(
                                            nproc,
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=cor_primaria,
                                        ),
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                        ),
                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                        border_radius=16,
                        bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                        border=ft.border.all(
                            2, ft.Colors.with_opacity(0.2, cor_primaria)
                        ),
                    ),

                    ft.Container(height=20),

                    # Linha decorativa animada
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    width=30,
                                    height=3,
                                    bgcolor=ft.Colors.with_opacity(0.3, cor_primaria),
                                    border_radius=2,
                                ),
                                ft.Container(
                                    width=60,
                                    height=3,
                                    bgcolor=cor_primaria,
                                    border_radius=2,
                                ),
                                ft.Container(
                                    width=30,
                                    height=3,
                                    bgcolor=ft.Colors.with_opacity(0.3, cor_primaria),
                                    border_radius=2,
                                ),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=50,
            border_radius=28,
            bgcolor=cor_card,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_borda)),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 15),
            ),
            width=500,
            animate=300,
        )

    card = build_card()

    # =========================
    # CAMPO DE EDIÇÃO
    # =========================
    nome_input = ft.TextField(
        label="Nome do Técnico",
        value=tecnico.get("nomeTecnico", ""),
        disabled=True,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        text_size=16,
        height=65,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=12,
    )

    # Container para os botões
    botoes_container = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.EDIT_OUTLINED, size=20),
                            ft.Text("Editar Perfil", size=15, weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    on_click=lambda e: ativar_edicao(e),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=cor_primaria,
                        padding=ft.padding.symmetric(horizontal=28, vertical=18),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=4,
                    ),
                    height=55,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(top=16),
    )

    def ativar_edicao(e):
        """Ativa o modo de edição"""
        nome_input.disabled = False
        nome_input.focus()
        
        botoes_container.content = ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=20),
                            ft.Text("Salvar", size=15, weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    on_click=salvar,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREEN_600,
                        padding=ft.padding.symmetric(horizontal=28, vertical=18),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=4,
                    ),
                    height=55,
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CLOSE_ROUNDED, size=20),
                            ft.Text("Cancelar", size=15, weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    on_click=cancelar_edicao,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_600,
                        padding=ft.padding.symmetric(horizontal=28, vertical=18),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=4,
                    ),
                    height=55,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
        )
        botoes_container.update()
        nome_input.update()

    def cancelar_edicao(e):
        """Cancela a edição"""
        nome_input.value = tecnico.get("nomeTecnico", "")
        nome_input.disabled = True
        
        botoes_container.content = ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.EDIT_OUTLINED, size=20),
                            ft.Text("Editar Perfil", size=15, weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    on_click=lambda e: ativar_edicao(e),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=cor_primaria,
                        padding=ft.padding.symmetric(horizontal=28, vertical=18),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=4,
                    ),
                    height=55,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        botoes_container.update()
        nome_input.update()

    def salvar(e):
        """Salva as alterações"""
        if not nome_input.value or not nome_input.value.strip():
            return
            
        sucesso = atualizarTecnico(
            tecnico["nProcTecnico"],
            nome_input.value.strip()
        )

        if sucesso:
            novo_nome = nome_input.value.strip()
            tecnico["nomeTecnico"] = novo_nome
            
            # ATUALIZA A SESSÃO para refletir no header
            if page:
                page.session.set("tecnico_nome", novo_nome)
                page.session.set("tecnico", tecnico)
            
            nome_input.disabled = True
            
            # Atualiza o card
            card.content = build_card().content
            card.update()
            
            # Volta ao botão de editar
            botoes_container.content = ft.Row(
                [
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.EDIT_OUTLINED, size=20),
                                ft.Text("Editar Perfil", size=15, weight=ft.FontWeight.W_500),
                            ],
                            spacing=8,
                        ),
                        on_click=lambda e: ativar_edicao(e),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=cor_primaria,
                            padding=ft.padding.symmetric(horizontal=28, vertical=18),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=4,
                        ),
                        height=55,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            botoes_container.update()
            nome_input.update()
            
            if page:
                page.go("/pagina-principal")

    # =========================
    # SEÇÃO DE EDIÇÃO
    # =========================
    secao_edicao = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SETTINGS_OUTLINED,
                            size=24,
                            color=cor_primaria,
                        ),
                        ft.Text(
                            "Configurações do Perfil",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(height=20),
                nome_input,
                botoes_container,
            ],
            spacing=0,
        ),
        padding=36,
        border_radius=24,
        bgcolor=cor_card,
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_borda)),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        ),
        width=500,
    )

    # =========================
    # BOTÃO VOLTAR
    # =========================
    def voltar(e):
        if page:
            page.go("/pagina-principal")

    botao_voltar = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    icon_size=24,
                    on_click=voltar,
                    style=ft.ButtonStyle(
                        color=cor_primaria,
                        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=12,
                    ),
                    tooltip="Voltar",
                ),
                ft.Text(
                    "Voltar",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=cor_primaria,
                ),
            ],
            spacing=8,
        ),
        on_click=voltar,
        ink=True,
        visible=page is not None,  # Só mostra se page foi passado
    )

    # =========================
    # LAYOUT FINAL
    # =========================
    return ft.Container(
        content=ft.Column(
            [
                # Botão voltar no topo à esquerda
                ft.Container(
                    content=botao_voltar,
                    alignment=ft.alignment.top_left,
                    width=500,
                ),
                ft.Container(height=20),
                card,
                ft.Container(height=40),
                secao_edicao,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=40,
        expand=True,
    )