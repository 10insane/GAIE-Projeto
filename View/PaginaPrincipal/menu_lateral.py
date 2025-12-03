import flet as ft
from .estilos import *


def criar_switch_tema(page, atualizar_icon_callback):

    # Estado inicial do switch
    ativo = page.theme_mode == ft.ThemeMode.LIGHT

    bola = ft.Container(
        width=22,
        height=22,
        border_radius=30,
        bgcolor="white",
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        left=26 if ativo else 2,
    )

    fundo = ft.Container(
        width=50,
        height=26,
        border_radius=30,
        bgcolor="#FFD54F" if ativo else "#5A5A5A",
        padding=2,
        content=ft.Stack([bola]),
        ink=True
    )

    label = ft.Text(
        "Modo Claro" if ativo else "Modo Escuro",
        size=13,
        color=cor_texto_claro
    )

    def alternar(e):
        nonlocal ativo
        ativo = not ativo

        # Atualizar bola deslizante
        bola.left = 26 if ativo else 2
        bola.update()

        # Atualizar fundo
        fundo.bgcolor = "#FFD54F" if ativo else "#5A5A5A"
        fundo.update()

        # Atualizar texto
        label.value = "Modo Claro" if ativo else "Modo Escuro"
        label.update()

        # Trocar tema
        page.theme_mode = ft.ThemeMode.LIGHT if ativo else ft.ThemeMode.DARK
        page.update()

        # Atualizar ícone no menu
        atualizar_icon_callback()

    fundo.on_click = alternar
    return ft.Row([fundo, label], spacing=10)


def criar_botao_menu(texto, icone, ativo=False, acao=None):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icone, color=ft.Colors.WHITE if ativo else cor_primaria, size=20),
                ft.Text(
                    texto,
                    size=14,
                    weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.W_500,
                    color=ft.Colors.WHITE if ativo else cor_texto_claro,
                ),
            ],
            spacing=12,
        ),
        padding=ft.padding.symmetric(horizontal=14, vertical=12),
        border_radius=12,
        ink=True,
        on_click=acao,
        bgcolor=cor_primaria if ativo else "transparent",
    )


def criar_menu_lateral(page, trocar_vista):

    # Ícone dinâmico depende do tema
    tema_icon = ft.Icon(
        ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE,
        color=cor_texto_claro,
        size=22
    )

    def atualizar_icone():
        tema_icon.name = (
            ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE
        )
        tema_icon.update()

    switch_tema = criar_switch_tema(page, atualizar_icone)

    return ft.Container(
        width=260,
        bgcolor=cor_card,
        padding=24,
        border=ft.border.all(1, cor_borda),
        content=ft.Column(
            [
                ft.Text("Menu Principal", size=18, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                ft.Divider(height=20, color=cor_borda),

                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD, acao=lambda e: trocar_vista("dashboard")),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE, acao=lambda e: trocar_vista("alunos")),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL, acao=lambda e: trocar_vista("escolas")),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT, acao=lambda e: trocar_vista("registos")),
                criar_botao_menu("Técnicos", ft.Icons.PERSON, acao=lambda e: trocar_vista("tecnicos")),

                ft.Container(expand=True),
                ft.Divider(height=20, color=cor_borda),

                # 🔥 Linha com o ícone dinâmico + switch animado
                ft.Row(
                    [
                        tema_icon,
                        switch_tema
                    ],
                    spacing=12
                ),

                criar_botao_menu("Configurações", ft.Icons.SETTINGS, acao=lambda e: page.go("/Config")),
                ft.Text("v1.0.0", size=11, color=cor_texto_medio),
            ],
            spacing=8,
        ),
    )
