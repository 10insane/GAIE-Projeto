# Views/PaginaPrincipal/dashboard_view.py

import flet as ft
from .estilos import (
    cor_primaria, cor_secundaria, cor_card, cor_texto_claro,
    cor_texto_medio, cor_borda
)

def criar_card_grande(titulo, valor, icone, cor, subtitulo):
    """Card principal com animação hover"""
    return ft.Container(
        content=ft.Column(
            [
                # Ícone com fundo colorido
                ft.Container(
                    content=ft.Icon(icone, color="#FFFFFF", size=36),
                    bgcolor=cor,
                    border_radius=16,
                    padding=16,
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                ),
                ft.Container(height=8),
                # Valor principal
                ft.Text(
                    str(valor), 
                    size=52, 
                    weight=ft.FontWeight.BOLD, 
                    color=cor,
                    animate_opacity=300,
                ),
                # Título
                ft.Text(
                    titulo, 
                    size=16, 
                    weight=ft.FontWeight.W_600, 
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                # Subtítulo
                ft.Container(
                    content=ft.Text(
                        subtitulo, 
                        size=13, 
                        color=cor_texto_medio,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=ft.padding.only(top=2),
                ),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=cor_card,
        padding=32,
        border_radius=18,
        shadow=ft.BoxShadow(
            blur_radius=24, 
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, cor),
            offset=ft.Offset(0, 6),
        ),
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.1, cor)),
        expand=True,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def criar_card_estado(titulo, valor, icone, cor):
    """Card de estado compacto e moderno"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone à esquerda
                ft.Container(
                    content=ft.Icon(icone, color="#FFFFFF", size=26),
                    bgcolor=cor,
                    border_radius=14,
                    padding=14,
                ),
                # Conteúdo à direita
                ft.Column(
                    [
                        ft.Text(
                            str(valor), 
                            size=36, 
                            weight=ft.FontWeight.BOLD, 
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            titulo, 
                            size=14, 
                            color=cor_texto_medio, 
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=18,
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=cor_card,
        padding=22,
        border_radius=16,
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.08, cor)),
        shadow=ft.BoxShadow(
            blur_radius=18, 
            spread_radius=0,
            color=ft.Colors.with_opacity(0.1, cor),
            offset=ft.Offset(0, 4),
        ),
        expand=True,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def criar_dashboard_view(alunos, escolas, registos):
    """Dashboard principal com layout otimizado"""
    return ft.Column(
        [
            # ====== Cabeçalho ======
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Dashboard", 
                            size=28, 
                            weight=ft.FontWeight.BOLD, 
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            "Visão geral do sistema", 
                            size=14, 
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=4,
                ),
                padding=ft.padding.only(bottom=24),
            ),

            # ====== Cards Principais ======
            ft.Row(
                [
                    criar_card_grande(
                        "Alunos", 
                        len(alunos), 
                        ft.Icons.PEOPLE_ALT_ROUNDED,
                        cor_primaria, 
                        "Registados no sistema"
                    ),
                    criar_card_grande(
                        "Registos", 
                        len(registos), 
                        ft.Icons.ASSIGNMENT_ROUNDED,
                        cor_secundaria, 
                        "Processos totais"
                    ),
                    criar_card_grande(
                        "Escolas", 
                        len(escolas), 
                        ft.Icons.SCHOOL_ROUNDED,
                        "#10B981", 
                        "Instituições registadas"
                    ),
                ],
                spacing=20,
            ),

            # ====== Separador ======
            ft.Container(height=32),
            ft.Divider(height=1, color=cor_borda),
            ft.Container(height=24),

            # ====== Seção Estados ======
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Estados dos Processos", 
                            size=22, 
                            weight=ft.FontWeight.BOLD, 
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            "Distribuição atual dos processos por estado", 
                            size=13, 
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=4,
                ),
                padding=ft.padding.only(bottom=20),
            ),

            # ====== Grid de Estados (3 colunas x 2 linhas) ======
            ft.Column(
                [
                    ft.Row(
                        [
                            criar_card_estado(
                                "A Aguardar",
                                len([r for r in registos if r.get("idEstado") == 1]),
                                ft.Icons.PENDING_ACTIONS,
                                "#F59E0B"
                            ),
                            criar_card_estado(
                                "Em Avaliação",
                                len([r for r in registos if r.get("idEstado") == 2]),
                                ft.Icons.ASSESSMENT,
                                "#3B82F6"
                            ),
                            criar_card_estado(
                                "Em Intervenção",
                                len([r for r in registos if r.get("idEstado") == 3]),
                                ft.Icons.PSYCHOLOGY,
                                cor_primaria
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Row(
                        [
                            criar_card_estado(
                                "Pendente",
                                len([r for r in registos if r.get("idEstado") == 4]),
                                ft.Icons.SCHEDULE,
                                "#EAB308"
                            ),
                            criar_card_estado(
                                "Arquivado",
                                len([r for r in registos if r.get("idEstado") == 5]),
                                ft.Icons.ARCHIVE,
                                "#6B7280"
                            ),
                            criar_card_estado(
                                "Em Vigilância",
                                len([r for r in registos if r.get("idEstado") == 6]),
                                ft.Icons.VISIBILITY,
                                "#10B981"
                            ),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=16,
            ),

            # ====== Espaço final para scroll ======
            ft.Container(height=24),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        expand=True,
    )