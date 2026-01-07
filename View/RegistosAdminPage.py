import flet as ft
from datetime import datetime
from Models.RegistoModel import listarRegistos
from Models.TecnicoModel import listarTecnico
from Models.AlunosModel import listarAlunos
from Models.EscolasModel import listarEscolas
from View.PaginaPrincipalAdmin.estilosAdmin import *


def RegistosAdminPage(page: ft.Page):
    # Carregar dados
    registos = listarRegistos()
    tecnicos = listarTecnico()
    alunos = listarAlunos()
    escolas = listarEscolas()

    tecnico_dict = {t['nProcTecnico']: t['NomeTecnico'] for t in tecnicos}
    aluno_dict = {a['nProcessoAluno']: a['NomeAluno'] for a in alunos}
    escola_dict = {e['idEscola']: e['NomeEscola'] for e in escolas}

    # Estados possíveis
    estados = {
        1: "A Aguardar",
        2: "Em Avaliação",
        3: "Em Intervenção",
        4: "Pendente",
        5: "Arquivado",
        6: "Em Vigilância"
    }

    # Paleta de cores
    p = {
        "cor_primaria": cor_primaria,
        "cor_secundaria": cor_secundaria,
        "cor_card": cor_card,
        "cor_fundo": cor_fundo,
        "cor_texto_claro": cor_texto_claro,
        "cor_texto_medio": cor_texto_medio,
        "cor_borda": cor_borda,
    }

    # Filtros
    filtro_estado = ft.Dropdown(
        label="Filtrar por Estado",
        options=[ft.dropdown.Option(key=str(k), text=v) for k, v in estados.items()],
        value="",
        width=200,
    )

    filtro_tecnico = ft.Dropdown(
        label="Filtrar por Técnico",
        options=[ft.dropdown.Option(key=str(t['nProcTecnico']), text=t['NomeTecnico']) for t in tecnicos],
        value="",
        width=200,
    )

    search_field = ft.TextField(
        label="Pesquisar",
        hint_text="Nome do aluno ou número...",
        width=300,
    )

    # Lista de registos
    registos_list = ft.ListView(spacing=10, expand=True)

    def criar_card_registo_completo(registo):
        estado_nome = estados.get(registo.get('idEstado'), 'Desconhecido')
        tecnico_nome = tecnico_dict.get(registo.get('nProcTecnico'), 'Desconhecido')
        aluno_nome = aluno_dict.get(registo.get('nProcessoAluno'), 'Desconhecido')
        escola_nome = escola_dict.get(registo.get('idEscola', 0), 'Desconhecida')

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.ASSIGNMENT, color=ft.Colors.WHITE, size=24),
                                bgcolor=p["cor_primaria"],
                                padding=12,
                                border_radius=12,
                            ),
                            ft.Column(
                                [
                                    ft.Text(f"Registo #{registo.get('nPIA', 'N/A')}", size=18, weight=ft.FontWeight.BOLD, color=p["cor_texto_claro"]),
                                    ft.Text(f"Aluno: {aluno_nome}", size=14, color=p["cor_texto_medio"]),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Text(estado_nome, size=12, weight=ft.FontWeight.BOLD),
                                bgcolor=ft.Colors.with_opacity(0.2, p["cor_primaria"]),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=20,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Text(f"Técnico: {tecnico_nome}", size=13, color=p["cor_texto_medio"]),
                            ft.Text(f"Escola: {escola_nome}", size=13, color=p["cor_texto_medio"]),
                        ],
                        spacing=20,
                    ),
                    ft.Text(f"Data: {registo.get('DataArquivo', 'N/A')}", size=13, color=p["cor_texto_medio"]),
                    ft.Text(f"Observações: {registo.get('Observacoes', 'Nenhuma')}", size=13, color=p["cor_texto_medio"]),
                ],
                spacing=5,
            ),
            bgcolor=p["cor_card"],
            padding=20,
            border_radius=16,
            border=ft.border.all(1, p["cor_borda"]),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
        )

    def filtrar_registos():
        filtrados = registos[:]

        # Filtro por estado
        if filtro_estado.value:
            filtrados = [r for r in filtrados if str(r.get('idEstado')) == filtro_estado.value]

        # Filtro por técnico
        if filtro_tecnico.value:
            filtrados = [r for r in filtrados if str(r.get('nProcTecnico')) == filtro_tecnico.value]

        # Filtro por search
        if search_field.value:
            termo = search_field.value.lower()
            filtrados = [r for r in filtrados if termo in aluno_dict.get(r.get('nProcessoAluno'), '').lower() or termo in str(r.get('nPIA', ''))]

        return filtrados

    def atualizar_lista():
        registos_list.controls.clear()
        filtrados = filtrar_registos()
        for registo in filtrados:
            registos_list.controls.append(criar_card_registo_completo(registo))
        page.update()

    # Eventos
    filtro_estado.on_change = lambda e: atualizar_lista()
    filtro_tecnico.on_change = lambda e: atualizar_lista()
    search_field.on_change = lambda e: atualizar_lista()

    # Botão voltar
    def voltar(e):
        page.go("/TelaPrincipalAdmin")

    botao_voltar = ft.ElevatedButton(
        "Voltar ao Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=voltar,
        style=ft.ButtonStyle(bgcolor=p["cor_secundaria"], color=ft.Colors.WHITE),
    )

    # Gráfico simples de estados
    def criar_grafico_estados():
        contagem_estados = {}
        for r in registos:
            estado = estados.get(r.get('idEstado'), 'Desconhecido')
            contagem_estados[estado] = contagem_estados.get(estado, 0) + 1

        grafico = ft.Column(
            [
                ft.Text("Distribuição por Estado", size=16, weight=ft.FontWeight.BOLD, color=p["cor_texto_claro"]),
                ft.Container(height=10),
            ] + [
                ft.Row(
                    [
                        ft.Text(f"{estado}: {count}", size=14, color=p["cor_texto_medio"]),
                        ft.Container(
                            content=ft.Text(""),
                            bgcolor=p["cor_primaria"],
                            height=20,
                            width=min(count * 20, 200),  # Barra simples
                            border_radius=10,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ) for estado, count in contagem_estados.items()
            ],
            spacing=8,
        )
        return grafico

    # Layout
    atualizar_lista()

    content = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        botao_voltar,
                        ft.Container(expand=True),
                        ft.Text("Todos os Registos", size=28, weight=ft.FontWeight.BOLD, color=p["cor_texto_claro"]),
                        ft.Container(expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),

                # Gráfico
                ft.Container(
                    content=criar_grafico_estados(),
                    bgcolor=p["cor_card"],
                    padding=20,
                    border_radius=16,
                    border=ft.border.all(1, p["cor_borda"]),
                ),
                ft.Container(height=20),

                # Filtros
                ft.Row(
                    [
                        filtro_estado,
                        filtro_tecnico,
                        search_field,
                    ],
                    spacing=15,
                ),
                ft.Container(height=20),

                # Lista
                ft.Text(f"Total de Registos: {len(registos)}", size=16, color=p["cor_texto_medio"]),
                ft.Container(height=10),
                registos_list,
            ],
            spacing=0,
            expand=True,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[p["cor_fundo"], "#131A33"],
        ),
        padding=32,
        expand=True,
    )

    return ft.View(
        route="/registos",
        controls=[content],
    )