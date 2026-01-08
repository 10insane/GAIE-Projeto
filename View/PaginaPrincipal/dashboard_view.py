import flet as ft
from .estilos import (
    cor_primaria,
    cor_secundaria,
    cor_card,
    cor_texto_claro,
    cor_texto_medio,
    cor_borda,
)


def criar_card_grande(titulo, valor, icone, subtitulo, cor_accent):
    return ft.Container(
        content=ft.Column(
            [
                # Cabeçalho do card com ícone e título
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icone, color="#FFFFFF", size=26),
                            gradient=ft.LinearGradient(
                                colors=[cor_accent, cor_secundaria],
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                            ),
                            border_radius=14,
                            padding=12,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    titulo,
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    subtitulo,
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=14,
                ),

                ft.Container(height=16),

                # Valor grande
                ft.Row(
                    [
                        ft.Text(
                            str(valor),
                            size=42,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.TRENDING_UP_ROUNDED,
                                color=cor_accent,
                                size=20,
                            ),
                            padding=ft.padding.only(left=8, top=12),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),

                # Barra de progresso decorativa
                ft.Container(
                    content=ft.Container(
                        bgcolor=cor_accent,
                        border_radius=4,
                        height=4,
                    ),
                    width=80,
                    margin=ft.margin.only(top=8),
                ),
            ],
            spacing=0,
        ),
        gradient=ft.LinearGradient(
            colors=[cor_card, "#1A2847"],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        ),
        padding=28,
        border_radius=18,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, "#000000"),
            offset=ft.Offset(0, 8),
        ),
        expand=True,
    )


def criar_card_estado(titulo, valor, icone, cor_destaque):
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icone, color="#FFFFFF", size=22),
                            gradient=ft.LinearGradient(
                                colors=[cor_destaque, cor_secundaria],
                                begin=ft.alignment.top_center,
                                end=ft.alignment.bottom_center,
                            ),
                            border_radius=12,
                            padding=12,
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            str(valor),
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                    ],
                ),
                ft.Container(height=8),
                ft.Text(
                    titulo,
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=cor_texto_medio,
                ),
                ft.Container(
                    content=ft.ProgressBar(
                        value=min(valor / 50, 1.0) if valor > 0 else 0,
                        color=cor_destaque,
                        bgcolor=ft.Colors.with_opacity(0.2, cor_destaque),
                        height=3,
                    ),
                    margin=ft.margin.only(top=6),
                ),
            ],
            spacing=2,
        ),
        gradient=ft.LinearGradient(
            colors=[cor_card, "#1A2847"],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        ),
        padding=22,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=16,
            color=ft.Colors.with_opacity(0.25, "#000000"),
            offset=ft.Offset(0, 6),
        ),
        expand=True,
    )


def criar_dashboard_view(alunos, escolas, registos):
    conteudo = ft.Column(
        [
            # Cabeçalho estilizado
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Dashboard",
                                            size=32,
                                            weight=ft.FontWeight.BOLD,
                                            color=cor_texto_claro,
                                        ),
                                        ft.Text(
                                            "Visão geral e estatísticas do sistema",
                                            size=14,
                                            color=cor_texto_medio,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                ft.Container(expand=True),
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.DASHBOARD_ROUNDED,
                                        color=cor_primaria,
                                        size=36,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                padding=ft.padding.only(bottom=24),
            ),

            # Cards principais
            ft.Row(
                [
                    criar_card_grande(
                        "Alunos",
                        len(alunos),
                        ft.Icons.PEOPLE_ALT_ROUNDED,
                        "Registados no sistema",
                        "#4A90E2",
                    ),
                    criar_card_grande(
                        "Registos",
                        len(registos),
                        ft.Icons.ASSIGNMENT_ROUNDED,
                        "Processos totais",
                        "#E24A90",
                    ),
                    criar_card_grande(
                        "Escolas",
                        len(escolas),
                        ft.Icons.SCHOOL_ROUNDED,
                        "Instituições registadas",
                        "#90E24A",
                    ),
                ],
                spacing=18,
                expand=True,
            ),

            ft.Container(height=24),

            # Separador
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            bgcolor=cor_borda,
                            height=2,
                            border_radius=2,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "ESTADOS DOS PROCESSOS",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=cor_texto_medio,
                            ),
                            padding=ft.padding.symmetric(horizontal=16),
                        ),
                        ft.Container(
                            bgcolor=cor_borda,
                            height=2,
                            border_radius=2,
                            expand=True,
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=8),
            ),

            ft.Container(height=16),

            # Grid de estados
            ft.Column(
                [
                    ft.Row(
                        [
                            criar_card_estado(
                                "A Aguardar",
                                len([r for r in registos if r.get("idEstado") == 1]),
                                ft.Icons.PENDING_ACTIONS,
                                "#FFA726",
                            ),
                            criar_card_estado(
                                "Em Avaliação",
                                len([r for r in registos if r.get("idEstado") == 2]),
                                ft.Icons.ASSESSMENT,
                                "#42A5F5",
                            ),
                            criar_card_estado(
                                "Em Intervenção",
                                len([r for r in registos if r.get("idEstado") == 3]),
                                ft.Icons.PSYCHOLOGY,
                                "#AB47BC",
                            ),
                        ],
                        spacing=14,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            criar_card_estado(
                                "Pendente",
                                len([r for r in registos if r.get("idEstado") == 4]),
                                ft.Icons.SCHEDULE,
                                "#EF5350",
                            ),
                            criar_card_estado(
                                "Arquivado",
                                len([r for r in registos if r.get("idEstado") == 5]),
                                ft.Icons.ARCHIVE,
                                "#78909C",
                            ),
                            criar_card_estado(
                                "Em Vigilância",
                                len([r for r in registos if r.get("idEstado") == 6]),
                                ft.Icons.VISIBILITY,
                                "#26A69A",
                            ),
                        ],
                        spacing=14,
                        expand=True,
                    ),
                ],
                spacing=14,
                expand=True,
            ),

            ft.Container(height=24),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Container(
        content=conteudo,
        padding=20,
        alignment=ft.alignment.center,
        expand=True,
        width=1200,   # largura fixa "máxima" em vez de max_width
    )
