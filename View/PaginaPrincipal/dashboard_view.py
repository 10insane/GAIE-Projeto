import flet as ft
from .estilos import (
    cor_primaria,
    cor_secundaria,
    cor_card,
    cor_texto_claro,
    cor_texto_medio,
    cor_borda,
)


def criar_card_grande(titulo, valor, icone, subtitulo):
    return ft.Container(
        content=ft.Column(
            [
                # Ícone
                ft.Container(
                    content=ft.Icon(icone, color="#FFFFFF", size=34),
                    gradient=ft.LinearGradient(
                        colors=[cor_primaria, cor_secundaria],
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                    ),
                    border_radius=16,
                    padding=16,
                ),

                ft.Container(height=12),

                # Valor
                ft.Text(
                    str(valor),
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                ),

                # Título
                ft.Text(
                    titulo,
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=cor_texto_claro,
                ),

                # Subtítulo
                ft.Text(
                    subtitulo,
                    size=13,
                    color=cor_texto_medio,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            colors=[cor_card, "#1B2A4A"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        padding=30,
        border_radius=20,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        expand=True,
    )


def criar_card_estado(titulo, valor, icone):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icone, color="#FFFFFF", size=24),
                    gradient=ft.LinearGradient(
                        colors=[cor_primaria, cor_secundaria],
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                    ),
                    border_radius=14,
                    padding=14,
                ),

                ft.Column(
                    [
                        ft.Text(
                            str(valor),
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            titulo,
                            size=14,
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=2,
                ),
            ],
            spacing=18,
        ),
        gradient=ft.LinearGradient(
            colors=[cor_card, "#1B2A4A"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        padding=22,
        border_radius=18,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.3, "#000000"),
            offset=ft.Offset(0, 8),
        ),
        expand=True,
    )


def criar_dashboard_view(alunos, escolas, registos):
    return ft.Column(
        [
            # Cabeçalho
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

            ft.Container(height=28),

            # Cards principais
            ft.Row(
                [
                    criar_card_grande(
                        "Alunos",
                        len(alunos),
                        ft.Icons.PEOPLE_ALT_ROUNDED,
                        "Registados no sistema",
                    ),
                    criar_card_grande(
                        "Registos",
                        len(registos),
                        ft.Icons.ASSIGNMENT_ROUNDED,
                        "Processos totais",
                    ),
                    criar_card_grande(
                        "Escolas",
                        len(escolas),
                        ft.Icons.SCHOOL_ROUNDED,
                        "Instituições registadas",
                    ),
                ],
                spacing=20,
            ),

            ft.Container(height=36),
            ft.Divider(color=cor_borda),
            ft.Container(height=24),

            # Estados
            ft.Text(
                "Estados dos Processos",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=cor_texto_claro,
            ),
            ft.Text(
                "Distribuição atual dos processos",
                size=13,
                color=cor_texto_medio,
            ),

            ft.Container(height=20),

            ft.Column(
                [
                    ft.Row(
                        [
                            criar_card_estado(
                                "A Aguardar",
                                len([r for r in registos if r.get("idEstado") == 1]),
                                ft.Icons.PENDING_ACTIONS,
                            ),
                            criar_card_estado(
                                "Em Avaliação",
                                len([r for r in registos if r.get("idEstado") == 2]),
                                ft.Icons.ASSESSMENT,
                            ),
                            criar_card_estado(
                                "Em Intervenção",
                                len([r for r in registos if r.get("idEstado") == 3]),
                                ft.Icons.PSYCHOLOGY,
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
                            ),
                            criar_card_estado(
                                "Arquivado",
                                len([r for r in registos if r.get("idEstado") == 5]),
                                ft.Icons.ARCHIVE,
                            ),
                            criar_card_estado(
                                "Em Vigilância",
                                len([r for r in registos if r.get("idEstado") == 6]),
                                ft.Icons.VISIBILITY,
                            ),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=16,
            ),

            ft.Container(height=32),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
