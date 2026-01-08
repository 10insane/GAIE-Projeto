import flet as ft
from .estilosAdmin import *
 
 
def criar_botao_menu(texto, icone, ativo=False, acao=None):
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    icone,
                    color=ft.Colors.WHITE if ativo else cor_primaria,
                    size=20,
                ),
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
        bgcolor=(
            ft.LinearGradient([cor_primaria, cor_secundaria])
            if ativo
            else "transparent"
        ),
    )
 
 
def criar_menu_lateral(page, trocar_vista):
 
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
                # Título
                ft.Text(
                    "Menu Principal",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                ),
                ft.Divider(height=20, color=cor_borda),
 
                # --- Secção principal ---
                criar_botao_menu(
                    "Dashboard",
                    ft.Icons.DASHBOARD,
                    acao=lambda e: trocar_vista("dashboardAdmin"),
                ),
                criar_botao_menu(
                    "Alunos",
                    ft.Icons.PEOPLE,
                    acao=lambda e: trocar_vista("alunos"),
                ),
                criar_botao_menu(
                    "Escolas",
                    ft.Icons.SCHOOL,
                    acao=lambda e: trocar_vista("escolas"),
                ),
                criar_botao_menu(
                    "Registos",
                    ft.Icons.ASSIGNMENT,
                    acao=lambda e: trocar_vista("registos"),
                ),
                criar_botao_menu(
                    "Técnicos",
                    ft.Icons.PERSON,
                    acao=lambda e: trocar_vista("tecnicos"),
                ),
 
                # empurra conteúdo para baixo
                ft.Container(expand=True),
 
                ft.Divider(height=20, color=cor_borda),
 
                # --- Configurações ---
                criar_botao_menu(
                    "Configurações",
                    ft.Icons.SETTINGS,
                    acao=lambda e: page.go("/Config"),
                ),
 
                ft.Text("v1.0.0", size=11, color=cor_texto_medio),
            ],
            spacing=8,
        ),
    )
 
 