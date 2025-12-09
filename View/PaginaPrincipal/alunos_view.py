import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao

# ======================
#  CONFIGURAÇÃO
# ======================

PAGE_SIZE = 50   # Quantos alunos carregar por página
CARD_SIMPLES = True  # Usa cards leves na lista (MUITO recomendado)

# ======================
#  CARDS
# ======================

def card_aluno_simples(a, abrir_detalhe):
    """Card LEVE — ideal para listas grandes"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=22),
                ft.Column(
                    [
                        ft.Text(a.get("NomeAluno", ""), size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            f"{a.get('Ano','?')}º  -  Turma {a.get('Turma','?')}",
                            size=12, color=cor_texto_medio
                        )
                    ],
                    spacing=2
                )
            ],
            spacing=12
        ),
        padding=12,
        border_radius=10,
        bgcolor=cor_card,
        on_click=lambda e: abrir_detalhe(a)
    )

def card_aluno_completo(a):
    """Card completo — apenas no detalhe do aluno"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(a.get("NomeAluno",""), size=20, weight=ft.FontWeight.BOLD),
                ft.Text(a.get("NomeEscola",""), size=14, color=cor_texto_medio),
                ft.Text(f"{a.get('Ano','?')}º  -  Turma {a.get('Turma','?')}",
                        size=14, color=cor_texto_medio),
            ],
            spacing=6
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=16,
    )

# ======================
#  VIEW PRINCIPAL
# ======================

def criar_alunos_view(alunos, page):

    # Estado de paginação e filtro
    estado = {
        "pagina": 0,
        "total": len(alunos),
        "filtro": "",  # texto da pesquisa
    }

    # Layout principal
    lista = ft.ListView(expand=True, spacing=10, padding=0)

    # ---- Função para abrir detalhe (card completo) ----
    def abrir_detalhe(a):
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalhes do aluno"),
            content=card_aluno_completo(a),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: fechar_dialog()),
            ],
        )
        page.dialog.open = True
        page.update()

    def fechar_dialog():
        page.dialog.open = False
        page.update()

    # ---- Função para atualizar a lista ----
    def carregar_pagina():
        lista.controls.clear()

        # Filtra alunos pelo filtro atual (ignora maiúsculas, minúsculas e espaços)
        filtro_normalizado = estado["filtro"].strip().replace(" ", "").lower()
        if filtro_normalizado:
            alunos_filtrados = [
                a for a in alunos
                if filtro_normalizado in a.get("NomeAluno", "").replace(" ", "").lower()
                or filtro_normalizado in str(a.get("NProcesso", "")).replace(" ", "").lower()
            ]
        else:
            alunos_filtrados = alunos

        estado["total"] = len(alunos_filtrados)

        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE

        pagina = alunos_filtrados[inicio:fim]

        for a in pagina:
            if CARD_SIMPLES:
                lista.controls.append(card_aluno_simples(a, abrir_detalhe))
            else:
                lista.controls.append(card_aluno_completo(a))

        page.update()

    carregar_pagina()

    # ---- Botões de navegação ----
    def prox_page(e):
        if (estado["pagina"] + 1) * PAGE_SIZE < estado["total"]:
            estado["pagina"] += 1
            carregar_pagina()

    def prev_page(e):
        if estado["pagina"] > 0:
            estado["pagina"] -= 1
            carregar_pagina()

    # ---- Função para atualizar filtro ----
    def on_search(e):
        estado["filtro"] = e.control.value
        estado["pagina"] = 0  # volta para a primeira página ao pesquisar
        carregar_pagina()

    # ======================
    #  HEADER + barra de pesquisa
    # ======================

    header = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Lista de Alunos", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(f"{len(alunos)}", size=13, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.with_opacity(0.10, cor_primaria),
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border_radius=8,
                    ),
                    ft.Text("alunos registados", size=13, color=cor_texto_medio),
                    ft.Container(expand=True),
                    ft.TextField(
                        hint_text="Pesquisar por nome ou nº de processo...",
                        on_change=on_search,
                        width=300,
                        suffix_icon=ft.Icons.SEARCH,
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        spacing=6
    )

    # ======================
    #  FOOTER – paginação
    # ======================

    footer = ft.Row(
        [
            ft.TextButton("◀  Anterior", on_click=prev_page),
            ft.TextButton("Seguinte  ▶", on_click=prox_page),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # ======================
    #  ECRÃ COMPLETO
    # ======================

    return ft.Column(
        [
            header,
            ft.Divider(height=1, color=cor_borda),
            ft.Container(height=10),
            lista,
            ft.Container(height=10),
            footer,
        ],
        expand=True,
        spacing=0
    )
