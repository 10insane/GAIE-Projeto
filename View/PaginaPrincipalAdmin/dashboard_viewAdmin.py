import flet as ft
from datetime import datetime
import asyncio
from .estilosAdmin import (
    cor_primaria,
    cor_secundaria,
    cor_card,
    cor_fundo,
    cor_texto_claro,
    cor_texto_medio,
    cor_borda,
)
from Models.TecnicoModel import listarTecnico
from Models.RegistoModel import listarRegistos


def criar_dashboard_viewAdmin(page: ft.Page, alunos, escolas, registos):

    # ========= PALETA ADMIN =========
    p = {
        "cor_primaria": cor_primaria,
        "cor_secundaria": cor_secundaria,

        "cor_sucesso": "#38BDF8",
        "cor_alerta": "#FBBF24",
        "cor_perigo": "#FB7185",
        "cor_info": "#38BDF8",

        "cor_card": cor_card,
        "cor_fundo": cor_fundo,

        "cor_texto_claro": cor_texto_claro,
        "cor_texto_medio": cor_texto_medio,

        "cor_borda": cor_borda,
        "cor_shadow": "#000000",

        "gradient_prim": [cor_primaria, cor_secundaria],
        "gradient_sec": ["#93C5FD", "#60A5FA"],
        "gradient_alt": ["#818CF8", "#6366F1"],
        "gradient_warm": ["#FBBF24", "#F59E0B"],
        "gradient_bg": [cor_fundo, "#131A33"],
    }

    # ========= DADOS =========
    tecnicos = listarTecnico()
    tecnico_dict = {t['nProcTecnico']: t['NomeTecnico'] for t in tecnicos}

    # Atividades recentes (últimos 10 registos)
    atividades_recentes = []
    for r in sorted(registos, key=lambda x: x.get('DataArquivo', ''), reverse=True)[:10]:
        tecnico_nome = tecnico_dict.get(r.get('nProcTecnico'), 'Desconhecido')
        atividades_recentes.append({
            'acao': 'Criou registo',
            'detalhe': f"Registo para aluno {r.get('nProcessoAluno', 'N/A')}",
            'quem': tecnico_nome,
            'data': r.get('DataArquivo', 'N/A')
        })

    estados_data = [
        {"nome": "A Aguardar", "valor": len([r for r in registos if r.get("idEstado") == 1]), "cor": p["gradient_warm"][0]},
        {"nome": "Em Avaliação", "valor": len([r for r in registos if r.get("idEstado") == 2]), "cor": p["gradient_alt"][0]},
        {"nome": "Em Intervenção", "valor": len([r for r in registos if r.get("idEstado") == 3]), "cor": p["cor_primaria"]},
        {"nome": "Pendente", "valor": len([r for r in registos if r.get("idEstado") == 4]), "cor": p["gradient_warm"][1]},
        {"nome": "Arquivado", "valor": len([r for r in registos if r.get("idEstado") == 5]), "cor": "#94A3B8"},
        {"nome": "Em Vigilância", "valor": len([r for r in registos if r.get("idEstado") == 6]), "cor": p["gradient_sec"][0]},
    ]

    # ========= COMPONENTES =========
    def metric_card(titulo, valor, icone, gradient, subtitulo):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=gradient[0], size=24),
                        bgcolor=ft.Colors.with_opacity(0.15, gradient[0]),
                        border_radius=12,
                        padding=12,
                    ),
                    ft.Container(height=20),
                    ft.Text(str(valor), size=36, weight=ft.FontWeight.BOLD, color=p["cor_texto_claro"]),
                    ft.Text(titulo, size=14, weight=ft.FontWeight.W_600, color=p["cor_texto_claro"]),
                    ft.Text(subtitulo, size=12, color=p["cor_texto_medio"]),
                ],
                spacing=4,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[p["cor_card"], "#1A2352"],
            ),
            padding=24,
            border_radius=22,
            border=ft.border.all(1, p["cor_borda"]),
            shadow=ft.BoxShadow(
                blur_radius=24,
                color=ft.Colors.with_opacity(0.4, "#000000"),
                offset=ft.Offset(0, 10),
            ),
            expand=True,
        )

    # Componente para atividades recentes
    atividades_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    def atualizar_atividades():
        atividades_list.controls.clear()
        for atividade in atividades_recentes:
            atividades_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.HISTORY, color=p["cor_primaria"], size=20),
                                bgcolor=ft.Colors.with_opacity(0.1, p["cor_primaria"]),
                                border_radius=10,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(f"{atividade['acao']}: {atividade['detalhe']}", size=14, weight=ft.FontWeight.W_600, color=p["cor_texto_claro"]),
                                    ft.Text(f"Por: {atividade['quem']} • {atividade['data']}", size=12, color=p["cor_texto_medio"]),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    bgcolor=p["cor_card"],
                    padding=16,
                    border_radius=12,
                    border=ft.border.all(1, p["cor_borda"]),
                )
            )
        page.update()

    # Botão para ver todas as ações
    def ver_todas_acoes(e):
        page.go("/registos")  # Navega para a vista de registos

    def refresh_atividades(e):
        nonlocal registos, tecnicos, tecnico_dict, atividades_recentes
        # Re-fetch data
        registos = listarRegistos()
        tecnicos = listarTecnico()
        tecnico_dict = {t['nProcTecnico']: t['NomeTecnico'] for t in tecnicos}
        atividades_recentes = []
        for r in sorted(registos, key=lambda x: x.get('DataArquivo', ''), reverse=True)[:10]:
            tecnico_nome = tecnico_dict.get(r.get('nProcTecnico'), 'Desconhecido')
            atividades_recentes.append({
                'acao': 'Criou registo',
                'detalhe': f"Registo para aluno {r.get('nProcessoAluno', 'N/A')}",
                'quem': tecnico_nome,
                'data': r.get('DataArquivo', 'N/A')
            })
        atualizar_atividades()

    botao_ver_todas = ft.ElevatedButton(
        "Ver Todas as Ações",
        icon=ft.Icons.VISIBILITY,
        on_click=ver_todas_acoes,
        style=ft.ButtonStyle(
            bgcolor=p["cor_primaria"],
            color=ft.Colors.WHITE,
        ),
    )

    botao_refresh = ft.ElevatedButton(
        "Atualizar",
        icon=ft.Icons.REFRESH,
        on_click=refresh_atividades,
        style=ft.ButtonStyle(
            bgcolor=p["cor_secundaria"],
            color=ft.Colors.WHITE,
        ),
    )

    # Inicializar atividades
    atualizar_atividades()

    # Função assíncrona para atualização periódica
    async def atualizar_periodicamente():
        while True:
            await asyncio.sleep(30)  # Espera 30 segundos
            refresh_atividades(None)  # Chama a função de refresh

    # Iniciar a tarefa assíncrona
    page.run_task(atualizar_periodicamente)

    # ========= LAYOUT =========
    return ft.Container(
        content=ft.Column(
            [
                # HEADER
                ft.Text(
                    "Dashboard Administrativo",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=p["cor_texto_claro"],
                ),
                ft.Text(
                    "Painel de controlo do sistema",
                    size=14,
                    color=p["cor_texto_medio"],
                ),

                ft.Container(height=32),

                # MÉTRICAS
                ft.Row(
                    [
                        metric_card(
                            "Alunos",
                            len(alunos),
                            ft.Icons.PEOPLE_ALT_ROUNDED,
                            p["gradient_prim"],
                            "Registados",
                        ),
                        metric_card(
                            "Registos",
                            len(registos),
                            ft.Icons.ASSIGNMENT_ROUNDED,
                            p["gradient_sec"],
                            "Processos",
                        ),
                        metric_card(
                            "Escolas",
                            len(escolas),
                            ft.Icons.SCHOOL_ROUNDED,
                            p["gradient_alt"],
                            "Instituições",
                        ),
                    ],
                    spacing=20,
                ),

                ft.Container(height=40),

                # ATIVIDADES RECENTES
                ft.Text(
                    "Atividades Recentes",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=p["cor_texto_claro"],
                ),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column(
                        [
                            atividades_list,
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    botao_refresh,
                                    ft.Container(expand=True),
                                    botao_ver_todas,
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.05, p["cor_card"]),
                    padding=20,
                    border_radius=16,
                    border=ft.border.all(1, p["cor_borda"]),
                ),

                ft.Container(height=40),
                ft.Text(
                    f"© {datetime.now().year} • Administração do Sistema",
                    size=11,
                    color=p["cor_texto_medio"],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=p["gradient_bg"],
        ),
        padding=32,
        expand=True,
    )
