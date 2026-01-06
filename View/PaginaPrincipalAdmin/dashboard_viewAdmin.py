# Views/PaginaPrincipal/dashboard_view.py

import flet as ft
from datetime import datetime
from .estilosAdmin import (
    cor_primaria, cor_secundaria, cor_card, cor_texto_claro,
    cor_texto_medio, cor_borda
)

def criar_dashboard_viewAdmin(page: ft.Page, alunos, escolas, registos):
    
    # --- Paleta de cores premium ---
    premium_palette = {
        "light": {
            "cor_primaria": "#10B981",        # Esmeralda
            "cor_secundaria": "#34D399",      # Verde claro
            "cor_sucesso": "#10B981",         # Esmeralda
            "cor_alerta": "#F59E0B",          # Âmbar
            "cor_perigo": "#EF4444",          # Vermelho
            "cor_info": "#0EA5E9",            # Ciano
            "cor_card": "#FFFFFF",
            "cor_fundo": "#F0FDF4",           # Verde muito claro
            "cor_texto_claro": "#065F46",     # Verde escuro
            "cor_texto_medio": "#6B7280",     # Cinza médio
            "cor_borda": "#D1FAE5",           # Verde claro
            "cor_shadow": "#A7F3D0",
            "gradient_prim": ["#10B981", "#34D399"],     # Verde
            "gradient_sec": ["#10B981", "#059669"],      # Verde
            "gradient_alt": ["#0EA5E9", "#0284C7"],      # Azul
            "gradient_warm": ["#F59E0B", "#D97706"],     # Laranja
            "gradient_bg": ["#F0FDF4", "#ECFDF5"],       # Fundo verde sutil
        },
        "dark": {
            "cor_primaria": "#34D399",        # Verde claro
            "cor_secundaria": "#10B981",      # Esmeralda
            "cor_sucesso": "#34D399",         # Esmeralda claro
            "cor_alerta": "#FBBF24",          # Âmbar claro
            "cor_perigo": "#F87171",          # Vermelho claro
            "cor_info": "#60A5FA",            # Azul claro
            "cor_card": "#1E293B",            # Azul escuro
            "cor_fundo": "#0F172A",           # Azul muito escuro
            "cor_texto_claro": "#F1F5F9",     # Branco azulado
            "cor_texto_medio": "#94A3B8",     # Cinza azulado
            "cor_borda": "#334155",           # Borda escura
            "cor_shadow": "#1E293B",
            "gradient_prim": ["#34D399", "#10B981"],
            "gradient_sec": ["#34D399", "#10B981"],
            "gradient_alt": ["#60A5FA", "#3B82F6"],
            "gradient_warm": ["#FBBF24", "#F59E0B"],
            "gradient_bg": ["#0F172A", "#1E293B"],
        }
    }

    # Determinar tema atual
    tema_atual = page.theme_mode if hasattr(page, "theme_mode") else ft.ThemeMode.LIGHT
    is_dark = tema_atual == ft.ThemeMode.DARK
    p = premium_palette["dark"] if is_dark else premium_palette["light"]

    # Extrair variáveis
    cor_prim = p["cor_primaria"]
    cor_sec = p["cor_secundaria"]
    cor_card_local = p["cor_card"]
    cor_fundo = p["cor_fundo"]
    cor_texto_claro_local = p["cor_texto_claro"]
    cor_texto_medio_local = p["cor_texto_medio"]
    cor_borda_local = p["cor_borda"]
    cor_shadow = p["cor_shadow"]

    # Dados para gráficos
    estados_data = [
        {"nome": "A Aguardar", "valor": len([r for r in registos if r.get("idEstado") == 1]), "cor": p["gradient_warm"][0]},
        {"nome": "Em Avaliação", "valor": len([r for r in registos if r.get("idEstado") == 2]), "cor": p["gradient_alt"][0]},
        {"nome": "Em Intervenção", "valor": len([r for r in registos if r.get("idEstado") == 3]), "cor": cor_prim},
        {"nome": "Pendente", "valor": len([r for r in registos if r.get("idEstado") == 4]), "cor": p["gradient_warm"][1]},
        {"nome": "Arquivado", "valor": len([r for r in registos if r.get("idEstado") == 5]), "cor": "#94A3B8"},
        {"nome": "Em Vigilância", "valor": len([r for r in registos if r.get("idEstado") == 6]), "cor": p["gradient_sec"][0]},
    ]

    total_registos = sum([d["valor"] for d in estados_data])
    
    # --- Função para o botão "Ver tudo" ---
    def ver_tudo_atividade(e):
        # Aqui você pode navegar para uma página de atividade completa
        # Por enquanto, vamos mostrar um snackbar
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Abrindo página completa de atividade..."),
            bgcolor=cor_prim,
        )
        page.snack_bar.open = True
        page.update()
        # Em um sistema real, você navegaria para outra view:
        # page.go("/atividade-completa")

    # --- Componentes Reutilizáveis ---
    def criar_metric_card(titulo, valor, icone, gradient_colors, subtitulo, crescimento=None):
        """Card de métrica com gradiente e efeitos"""
        return ft.Container(
            content=ft.Stack(
                [
                    # Fundo com gradiente sutil
                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[
                                ft.Colors.with_opacity(0.03, gradient_colors[0]),
                                ft.Colors.with_opacity(0.01, gradient_colors[1])
                            ]
                        ),
                        border_radius=16,
                    ),
                    # Conteúdo
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(icone, color=gradient_colors[0], size=24),
                                        bgcolor=ft.Colors.with_opacity(0.1, gradient_colors[0]),
                                        border_radius=12,
                                        padding=12,
                                    ),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.TRENDING_UP if crescimento and crescimento > 0 else ft.Icons.TRENDING_DOWN,
                                                    color=p["cor_sucesso"] if crescimento and crescimento > 0 else p["cor_perigo"],
                                                    size=14,
                                                ),
                                                ft.Text(
                                                    f"+{abs(crescimento)}%" if crescimento else "",
                                                    size=11,
                                                    color=p["cor_sucesso"] if crescimento and crescimento > 0 else p["cor_perigo"],
                                                    weight=ft.FontWeight.W_600,
                                                ) if crescimento else ft.Container()
                                            ],
                                            spacing=2,
                                        ),
                                        bgcolor=ft.Colors.with_opacity(0.1, p["cor_sucesso"] if crescimento and crescimento > 0 else p["cor_perigo"]),
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=8,
                                    ) if crescimento else ft.Container()
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                str(valor),
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=cor_texto_claro_local,
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                titulo,
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=cor_texto_claro_local,
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                subtitulo,
                                size=12,
                                color=cor_texto_medio_local,
                            ),
                        ],
                        spacing=0,
                    ),
                ]
            ),
            bgcolor=cor_card_local,
            padding=24,
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, cor_borda_local)),
            shadow=ft.BoxShadow(
                blur_radius=25,
                spread_radius=-8,
                color=ft.Colors.with_opacity(0.15, cor_shadow),
                offset=ft.Offset(0, 8),
            ),
            animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: setattr(e.control, "scale", ft.transform.Scale(1.02) if e.data == "true" else None) or e.control.update(),
            expand=True,
        )

    def criar_donut_chart(porcentagem, cor_gradient, tamanho=120):
        """Gráfico donut animado"""
        return ft.Stack(
            [
                # Círculo de fundo
                ft.Container(
                    width=tamanho,
                    height=tamanho,
                    border_radius=tamanho/2,
                    bgcolor=ft.Colors.with_opacity(0.1, cor_gradient[0]),
                ),
                # Círculo de progresso
                ft.Container(
                    width=tamanho,
                    height=tamanho,
                    border_radius=tamanho/2,
                    gradient=ft.SweepGradient(
                        center=ft.alignment.center,
                        start_angle=0,
                        end_angle=porcentagem * 3.6,
                        colors=[cor_gradient[0], cor_gradient[1], ft.Colors.TRANSPARENT],
                        stops=[0, 0.95, 0.95],
                    ),
                    animate=ft.Animation(1500, ft.AnimationCurve.EASE_OUT),
                ),
                # Círculo interno (furo do donut)
                ft.Container(
                    width=tamanho-24,
                    height=tamanho-24,
                    border_radius=(tamanho-24)/2,
                    bgcolor=cor_card_local,
                    top=12,
                    left=12,
                ),
                # Texto no centro
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"{porcentagem}%",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=cor_texto_claro_local,
                            ),
                            ft.Text(
                                "Concluído",
                                size=10,
                                color=cor_texto_medio_local,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    alignment=ft.alignment.center,
                    width=tamanho,
                    height=tamanho,
                ),
            ],
            width=tamanho,
            height=tamanho,
        )

    def criar_atividade_item(icone, titulo, tempo, usuario, cor):
        """Item de atividade recente"""
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Container(
                    content=ft.Icon(icone, color="#FFFFFF", size=16),
                    bgcolor=cor,
                    border_radius=10,
                    padding=8,
                    shadow=ft.BoxShadow(
                        blur_radius=8,
                        spread_radius=0,
                        color=ft.Colors.with_opacity(0.3, cor),
                    ),
                ),
                title=ft.Text(titulo, size=14, color=cor_texto_claro_local, weight=ft.FontWeight.W_500),
                subtitle=ft.Text(tempo, size=12, color=cor_texto_medio_local),
                trailing=ft.Container(
                    content=ft.Text(
                        usuario,
                        size=11,
                        color=cor_texto_medio_local,
                        weight=ft.FontWeight.W_500,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.08, cor_borda_local),
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=8,
                ),
            ),
            bgcolor=ft.Colors.with_opacity(0.03, cor_borda_local),
            border_radius=12,
            padding=ft.padding.symmetric(vertical=4),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: setattr(e.control, "bgcolor", ft.Colors.with_opacity(0.08, cor_borda_local) if e.data == "true" else ft.Colors.with_opacity(0.03, cor_borda_local)) or e.control.update(),
        )

    # --- Layout Principal ---
    return ft.Container(
        content=ft.Column(
            [
                # ====== HEADER COM GRADIENTE ======
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Dashboard Administrativo",
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=cor_texto_claro_local,
                                            ),
                                            ft.Text(
                                                "Bem-vindo de volta! Aqui está o resumo do sistema.",
                                                size=14,
                                                color=cor_texto_medio_local,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.REFRESH_OUTLINED,
                                                icon_color=cor_sec,
                                                icon_size=20,
                                                tooltip="Atualizar dados",
                                                style=ft.ButtonStyle(
                                                    bgcolor=ft.Colors.with_opacity(0.1, cor_sec),
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                ),
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.DOWNLOAD_OUTLINED,
                                                icon_color=cor_sec,
                                                icon_size=20,
                                                tooltip="Exportar relatório",
                                                style=ft.ButtonStyle(
                                                    bgcolor=ft.Colors.with_opacity(0.1, cor_sec),
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                ),
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                                                icon_color=cor_sec,
                                                icon_size=20,
                                                tooltip="Notificações",
                                                style=ft.ButtonStyle(
                                                    bgcolor=ft.Colors.with_opacity(0.1, cor_sec),
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                ),
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.only(bottom=32),
                ),

                # ====== MÉTRICAS PRINCIPAIS COM GRADIENTE ======
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Visão Geral",
                                    size=20,
                                    weight=ft.FontWeight.W_700,
                                    color=cor_texto_claro_local,
                                ),
                                ft.Container(expand=True),
                                ft.Text(
                                    datetime.now().strftime("%d %b, %Y"),
                                    size=12,
                                    color=cor_texto_medio_local,
                                ),
                            ]
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            [
                                criar_metric_card(
                                    "Total de Alunos",
                                    len(alunos),
                                    ft.Icons.PERSON_ADD_ALT_1,
                                    p["gradient_prim"],
                                    "Ativos no sistema",
                                    crescimento=5.2,
                                ),
                                criar_metric_card(
                                    "Registos Ativos",
                                    len(registos),
                                    ft.Icons.ASSESSMENT,
                                    p["gradient_sec"],
                                    "Processos em andamento",
                                    crescimento=12.5,
                                ),
                                criar_metric_card(
                                    "Escolas Parceiras",
                                    len(escolas),
                                    ft.Icons.ACCOUNT_BALANCE,
                                    p["gradient_alt"],
                                    "Instituições colaboradoras",
                                    crescimento=3.1,
                                ),
                            ],
                            spacing=20,
                        ),
                    ],
                ),

                ft.Container(height=32),

                # ====== ANÁLISE DETALHADA ======
                ft.Row(
                    [
                        # Gráfico e Distribuição
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Distribuição por Estado",
                                                size=18,
                                                weight=ft.FontWeight.W_700,
                                                color=cor_texto_claro_local,
                                                expand=True,
                                            ),
                                            ft.Container(
                                                content=ft.Text(
                                                    f"Total: {total_registos}",
                                                    size=12,
                                                    color=cor_texto_medio_local,
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.08, cor_borda_local),
                                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                                border_radius=8,
                                            ),
                                        ]
                                    ),
                                    ft.Container(height=20),
                                    ft.Row(
                                        [
                                            # Gráfico Donut
                                            ft.Column(
                                                [
                                                    criar_donut_chart(
                                                        int((len([r for r in registos if r.get("idEstado") == 5]) / len(registos)) * 100) if registos else 0,
                                                        p["gradient_sec"],
                                                        140
                                                    ),
                                                    ft.Container(height=12),
                                                    ft.Text(
                                                        "Taxa de Conclusão",
                                                        size=12,
                                                        color=cor_texto_medio_local,
                                                        text_align=ft.TextAlign.CENTER,
                                                    ),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            # Legenda
                                            ft.Container(
                                                content=ft.Column(
                                                    [
                                                        *[ft.Row(
                                                            [
                                                                ft.Container(
                                                                    width=12,
                                                                    height=12,
                                                                    border_radius=6,
                                                                    bgcolor=d["cor"],
                                                                ),
                                                                ft.Text(
                                                                    d["nome"],
                                                                    size=12,
                                                                    color=cor_texto_claro_local,
                                                                    expand=True,
                                                                ),
                                                                ft.Text(
                                                                    f"{d['valor']}",
                                                                    size=12,
                                                                    color=cor_texto_medio_local,
                                                                    weight=ft.FontWeight.W_600,
                                                                ),
                                                            ],
                                                            spacing=12,
                                                        ) for d in estados_data if d["valor"] > 0]
                                                    ],
                                                    spacing=10,
                                                ),
                                                expand=True,
                                                padding=ft.padding.only(left=20),
                                            ),
                                        ],
                                        spacing=20,
                                    ),
                                ],
                                spacing=0,
                            ),
                            bgcolor=cor_card_local,
                            padding=28,
                            border_radius=24,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_borda_local)),
                            shadow=ft.BoxShadow(
                                blur_radius=30,
                                spread_radius=-10,
                                color=ft.Colors.with_opacity(0.15, cor_shadow),
                                offset=ft.Offset(0, 10),
                            ),
                            expand=3,
                        ),

                        # Estatísticas Rápidas
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Estatísticas Rápidas",
                                        size=18,
                                        weight=ft.FontWeight.W_700,
                                        color=cor_texto_claro_local,
                                    ),
                                    ft.Container(height=20),
                                    ft.Column(
                                        [
                                            ft.Container(
                                                content=ft.Row(
                                                    [
                                                        ft.Container(
                                                            content=ft.Icon(ft.Icons.TRENDING_UP, color=p["cor_sucesso"], size=18),
                                                            bgcolor=ft.Colors.with_opacity(0.1, p["cor_sucesso"]),
                                                            border_radius=10,
                                                            padding=8,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "Novos este mês",
                                                                    size=12,
                                                                    color=cor_texto_medio_local,
                                                                ),
                                                                ft.Text(
                                                                    f"+{int(len(registos) * 0.15)}",
                                                                    size=18,
                                                                    color=cor_texto_claro_local,
                                                                    weight=ft.FontWeight.W_700,
                                                                ),
                                                            ],
                                                            spacing=2,
                                                            expand=True,
                                                        ),
                                                    ],
                                                    spacing=16,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.03, cor_borda_local),
                                                padding=16,
                                                border_radius=14,
                                            ),
                                            ft.Container(height=12),
                                            ft.Container(
                                                content=ft.Row(
                                                    [
                                                        ft.Container(
                                                            content=ft.Icon(ft.Icons.SCHOOL, color=p["cor_info"], size=18),
                                                            bgcolor=ft.Colors.with_opacity(0.1, p["cor_info"]),
                                                            border_radius=10,
                                                            padding=8,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "Média por escola",
                                                                    size=12,
                                                                    color=cor_texto_medio_local,
                                                                ),
                                                                ft.Text(
                                                                    f"{len(alunos) // max(len(escolas), 1)} alunos",
                                                                    size=18,
                                                                    color=cor_texto_claro_local,
                                                                    weight=ft.FontWeight.W_700,
                                                                ),
                                                            ],
                                                            spacing=2,
                                                            expand=True,
                                                        ),
                                                    ],
                                                    spacing=16,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.03, cor_borda_local),
                                                padding=16,
                                                border_radius=14,
                                            ),
                                            ft.Container(height=12),
                                            ft.Container(
                                                content=ft.Row(
                                                    [
                                                        ft.Container(
                                                            content=ft.Icon(ft.Icons.ACCESS_TIME, color=cor_prim, size=18),
                                                            bgcolor=ft.Colors.with_opacity(0.1, cor_prim),
                                                            border_radius=10,
                                                            padding=8,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "Tempo médio",
                                                                    size=12,
                                                                    color=cor_texto_medio_local,
                                                                ),
                                                                ft.Text(
                                                                    "14.5 dias",
                                                                    size=18,
                                                                    color=cor_texto_claro_local,
                                                                    weight=ft.FontWeight.W_700,
                                                                ),
                                                            ],
                                                            spacing=2,
                                                            expand=True,
                                                        ),
                                                    ],
                                                    spacing=16,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.03, cor_borda_local),
                                                padding=16,
                                                border_radius=14,
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                                spacing=0,
                            ),
                            bgcolor=cor_card_local,
                            padding=28,
                            border_radius=24,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_borda_local)),
                            shadow=ft.BoxShadow(
                                blur_radius=30,
                                spread_radius=-10,
                                color=ft.Colors.with_opacity(0.15, cor_shadow),
                                offset=ft.Offset(0, 10),
                            ),
                            expand=2,
                        ),
                    ],
                    spacing=24,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),

                ft.Container(height=32),

                # ====== ATIVIDADE RECENTE ======
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "Atividade Recente",
                                        size=20,
                                        weight=ft.FontWeight.W_700,
                                        color=cor_texto_claro_local,
                                        expand=True,
                                    ),
                                    # BOTÃO CORRIGIDO - agora com on_click
                                    ft.TextButton(
                                        content=ft.Row(
                                            [
                                                ft.Text(
                                                    "Ver tudo",
                                                    size=13,
                                                    weight=ft.FontWeight.W_600,
                                                    color=cor_sec,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.CHEVRON_RIGHT,
                                                    size=16,
                                                    color=cor_sec,
                                                ),
                                            ],
                                            spacing=6,
                                        ),
                                        on_click=ver_tudo_atividade,  # CORREÇÃO AQUI
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                            overlay_color=ft.Colors.with_opacity(0.1, cor_sec),
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                    ),
                                ]
                            ),
                            ft.Container(height=20),
                            ft.Column(
                                [
                                    criar_atividade_item(
                                        ft.Icons.PERSON_ADD,
                                        "Novo aluno registado",
                                        "Há 2 minutos",
                                        "João Silva",
                                        p["gradient_sec"][0]
                                    ),
                                    criar_atividade_item(
                                        ft.Icons.TASK_ALT,
                                        "Processo concluído",
                                        "Há 15 minutos",
                                        "#PRC-045",
                                        p["gradient_prim"][0]
                                    ),
                                    criar_atividade_item(
                                        ft.Icons.PRIORITY_HIGH,
                                        "Alerta de prioridade alta",
                                        "Há 1 hora",
                                        "Urgente",
                                        p["gradient_warm"][0]
                                    ),
                                    criar_atividade_item(
                                        ft.Icons.SCHOOL,
                                        "Escola adicionada",
                                        "Hoje, 10:30",
                                        "EB 2,3",
                                        p["gradient_alt"][0]
                                    ),
                                    criar_atividade_item(
                                        ft.Icons.UPDATE,
                                        "Sistema atualizado",
                                        "Hoje, 09:15",
                                        "v1.2.0",
                                        p["cor_info"]
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=cor_card_local,
                    padding=28,
                    border_radius=24,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_borda_local)),
                    shadow=ft.BoxShadow(
                        blur_radius=30,
                        spread_radius=-10,
                        color=ft.Colors.with_opacity(0.15, cor_shadow),
                        offset=ft.Offset(0, 10),
                    ),
                ),

                # ====== RODAPÉ ======
                ft.Container(height=32),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Resumo do Sistema",
                                        size=12,
                                        color=cor_texto_medio_local,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Text(
                                        f"📊 {len(alunos)} alunos • 🏫 {len(escolas)} escolas • 📁 {len(registos)} processos",
                                        size=11,
                                        color=cor_texto_medio_local,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                f"© {datetime.now().year} Sistema Educacional • v2.1.0",
                                size=11,
                                color=cor_texto_medio_local,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(vertical=16),
                    border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.with_opacity(0.1, cor_borda_local))),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=p["gradient_bg"] if "gradient_bg" in p else [cor_fundo, cor_fundo]
        ),
        padding=ft.padding.all(32),
        expand=True,
    )