import flet as ft
from .estilos import *


def criar_switch_tema(page, atualizar_icon_callback):

    ativo = page.theme_mode == ft.ThemeMode.LIGHT

    bola = ft.Container(
        width=14,
        height=14,
        border_radius=20,
        bgcolor="white",
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        left=18 if ativo else 2,
    )

    fundo = ft.Container(
        width=34,
        height=18,
        border_radius=20,
        bgcolor="#FFD54F" if ativo else "#5A5A5A",
        padding=2,
        content=ft.Stack([bola]),
        ink=True,
    )

    def alternar(e):
        nonlocal ativo
        ativo = not ativo

        bola.left = 18 if ativo else 2
        bola.update()

        fundo.bgcolor = "#FFD54F" if ativo else "#5A5A5A"
        fundo.update()

        page.theme_mode = ft.ThemeMode.LIGHT if ativo else ft.ThemeMode.DARK
        page.update()

        atualizar_icon_callback()

    fundo.on_click = alternar

    return fundo


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
        border_radius=15,
        ink=True,
        on_click=acao,
        bgcolor=ft.LinearGradient([cor_primaria, cor_secundaria]) if ativo else "transparent",
    )


def criar_menu_lateral(page, trocar_vista):

    tema_icon = ft.Icon(
        ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE,
        color=cor_texto_claro,
        size=20
    )

    def atualizar_icone():
        tema_icon.name = (
            ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE
        )
        tema_icon.update()

    switch_tema = criar_switch_tema(page, atualizar_icone)

    return ft.Container(
        width=260,
        gradient=ft.LinearGradient([cor_card, "#1A2332"]),
        padding=24,
        border=ft.border.all(1, cor_borda),
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            spread_radius=3,
        ),
        content=ft.Column(
            [
                ft.Text("Menu Principal", size=18, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                ft.Divider(height=20, color=cor_borda),

                # --- principais ---
                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD, acao=lambda e: trocar_vista("dashboard")),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT, acao=lambda e: trocar_vista("registos")),

                # empurra para baixo
                ft.Container(expand=True),

                # --- secção secundária ---
                ft.Text("Gestão Secundária", size=13, weight=ft.FontWeight.W_600, color=cor_texto_medio),
                ft.Container(height=4),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE, acao=lambda e: trocar_vista("alunos")),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL, acao=lambda e: trocar_vista("escolas")),

                ft.Divider(height=20, color=cor_borda),

                # 🔥 Switch alinhado com "Configurações"
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=14, vertical=12),
                    content=ft.Row(
                        [
                            tema_icon,
                            switch_tema
                        ],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.START
                    )
                ),

                ft.Text("v1.0.0", size=11, color=cor_texto_medio),
            ],
            spacing=8,
        ),
    )
