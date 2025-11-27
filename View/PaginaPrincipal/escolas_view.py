# Views/PaginaPrincipal/escolas_view.py

import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao


def criar_card_escola(escola, page):
    """Card de escola com design moderno e clean"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone da escola
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=24),
                    bgcolor="#10B981",
                    padding=10,
                    border_radius=12,
                ),

                # Informações da escola
                ft.Column(
                    [
                        # Nome
                        ft.Text(
                            escola.get("NomeEscola", ""),
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                # Botão de editar
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_color="#FFFFFF",
                        bgcolor="#F59E0B",
                        tooltip="Editar Escola",
                        icon_size=18,
                        on_click=lambda e, a=escola: (
                            page.session.set("escola_editar_id", a.get("idEscola")),
                            page.go("/EditarEscola")
                        ),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=14,
        ),

        bgcolor=cor_card,
        padding=16,
        border_radius=14,
        border=ft.border.all(2, ft.Colors.with_opacity(0.15, "#10B981")),
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, "#10B981"),
            offset=ft.Offset(0, 4),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def criar_escolas_view(escolas, page):
    """View principal da lista de escolas"""

    if escolas:
        return ft.Column(
            [
                # Cabeçalho fixo
                ft.Container(
                    content=ft.Row(
                        [
                            # Título e contador
                            ft.Column(
                                [
                                    ft.Text(
                                        "Lista de Escolas",
                                        size=26,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_texto_claro,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text(
                                                    f"{len(escolas)}",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#10B981",
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.1, "#10B981"),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                                border_radius=8,
                                            ),
                                            ft.Text(
                                                "escolas registadas",
                                                size=13,
                                                color=cor_texto_medio,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                ],
                                spacing=8,
                            ),

                            ft.Container(expand=True),

                            # Botão adicionar
                            estilo_botao_acao(
                                "Adicionar Escola",
                                ft.Icons.ADD_CIRCLE_ROUNDED,
                                lambda e: page.go("/criar-escola")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),

                # Divider
                ft.Divider(height=1, color=cor_borda),
                
                ft.Container(height=16),

                # Lista de escolas com scroll
                ft.Column(
                    [criar_card_escola(e, page) for e in escolas],
                    spacing=12,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    # ——— Estado vazio ———
    return ft.Container(
        content=ft.Column(
            [
                # Ícone grande
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.SCHOOL_OUTLINED,
                        size=80,
                        color=cor_texto_medio,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.05, cor_texto_medio),
                    padding=30,
                    border_radius=100,
                ),
                
                ft.Container(height=8),
                
                # Texto principal
                ft.Text(
                    "Nenhuma escola registada",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                # Subtexto
                ft.Text(
                    "A lista de escolas está vazia",
                    size=14,
                    color=cor_texto_medio,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(height=20),
                
                # Botão
                estilo_botao_acao(
                    "Adicionar Primeira Escola",
                    ft.Icons.ADD_CIRCLE_ROUNDED,
                    lambda e: page.go("/criar-escola")
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=40,
    )