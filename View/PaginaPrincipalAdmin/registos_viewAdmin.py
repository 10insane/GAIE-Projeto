# Views/PaginaPrincipal/registos_view.py

import flet as ft
from .estilosAdmin import *
from .util_buttons import estilo_botao_acao


def criar_card_registo(registo, page):
    """Card de registo com design moderno e clean"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone do registo
                ft.Container(
                    content=ft.Icon(ft.Icons.ASSIGNMENT, color="#FFFFFF", size=24),
                    bgcolor=cor_secundaria,
                    padding=10,
                    border_radius=12,
                ),

                # Informações do registo
                ft.Column(
                    [
                        # Número do registo
                        ft.Text(
                            f"Registo #{registo.get('nPIA', 'N/A')}",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                        
                        ft.Container(height=4),
                        
                        # Linha 1: Aluno e Estado
                        ft.Row(
                            [
                                # Aluno
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PERSON, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                registo.get('NomeAluno', 'N/A'),
                                                size=12,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.08, cor_texto_medio),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=6,
                                ),

                                # Estado
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.FLAG, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                registo.get('Estado', 'N/A'),
                                                size=12,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.08, cor_texto_medio),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=6,
                                ),
                            ],
                            spacing=8,
                        ),
                        
                        ft.Container(height=2),
                        
                        # Linha 2: Data e Técnico
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=11, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('DataEntradaSPO', 'N/A'),
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                                ft.Text("•", size=11, color=cor_texto_medio),
                                ft.Icon(ft.Icons.PERSON_OUTLINE, size=11, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('NomeTecnico', 'N/A'),
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),

                # Botões de ação
                ft.Row(
                    [
                        # Botão Ver
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.VISIBILITY_ROUNDED,
                                icon_color="#FFFFFF",
                                bgcolor=cor_primaria,
                                tooltip="Ver detalhes",
                                icon_size=18,
                                on_click=lambda e, r=registo:
                                    page.go(f'/registo/{r.get("idRegisto")}')
                            ),
                        ),

                        # Botão Editar
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.EDIT_ROUNDED,
                                icon_color="#FFFFFF",
                                bgcolor="#F59E0B",
                                tooltip="Editar registo",
                                icon_size=18,
                                on_click=lambda e, a=registo: (
                                    page.session.set("registo_editar_id", a["nPIA"]),
                                    page.go("/EditarRegisto")
                                ),
                            ),
                        ),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=14,
        ),

        bgcolor=cor_card,
        padding=16,
        border_radius=14,
        border=ft.border.all(2, ft.Colors.with_opacity(0.15, cor_secundaria)),
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, cor_secundaria),
            offset=ft.Offset(0, 4),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def criar_registos_view(registos, page):
    """View principal da lista de registos"""

    if registos:
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
                                        "Lista de Registos",
                                        size=26,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_texto_claro,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text(
                                                    f"{len(registos)}",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=cor_secundaria,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.1, cor_secundaria),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                                border_radius=8,
                                            ),
                                            ft.Text(
                                                "registos encontrados",
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
                                "Adicionar Registo",
                                ft.Icons.ADD_CIRCLE_ROUNDED,
                                lambda e: page.go("/criar-registo")
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

                # Lista de registos com scroll
                ft.Column(
                    [criar_card_registo(r, page) for r in registos],
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
                        ft.Icons.ASSIGNMENT_OUTLINED,
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
                    "Nenhum registo criado",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                # Subtexto
                ft.Text(
                    "Comece por adicionar o primeiro registo",
                    size=14,
                    color=cor_texto_medio,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(height=20),
                
                # Botão
                estilo_botao_acao(
                    "Adicionar Primeiro Registo",
                    ft.Icons.ADD_CIRCLE_ROUNDED,
                    lambda e: page.go("/criar-registo")
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=40,
    )