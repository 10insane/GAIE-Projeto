import flet as ft
from .estilosAdmin import *
from .util_buttons import estilo_botao_acao
import re

# ======================
# CONFIGURAÇÃO
# ======================

PAGE_SIZE = 50
CARD_SIMPLES = True


# ======================
# CARDS
# ======================

def card_aluno_simples(a,  page):
    """Card moderno e leve com hover"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=24),
                    width=50,
                    height=50,
                    bgcolor=cor_primaria,
                    border_radius=25,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4),
                    ),
                ),
                ft.Column(
                    [
                        ft.Text(
                            a.get("NomeAluno", "Sem Nome"),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=cor_texto_claro,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        f"{a.get('Ano', '?')}º ano",
                                        size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=cor_primaria,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                    border_radius=12,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"Turma {a.get('Turma', '?')}",
                                        size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=cor_secundaria,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                    border_radius=12,
                                ),
                                ft.Text(
                                    f"Nº {a.get('nProcessoAluno', 'N/A')}",
                                    size=11,
                                    color=cor_texto_medio,
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    color=ft.Colors.GREY_400,
                    size=18,
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=16,
         on_click=lambda e : (
            page.session.set("aluno_detalhes_id", a["nProcessoAluno"]),
            page.go("/maisDetalhesAlunos")
        ),
        border_radius=12,
        bgcolor=cor_card,
        shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def card_aluno_completo(a):
    """Card detalhado do aluno"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=40),
                    width=80,
                    height=80,
                    bgcolor=cor_primaria,
                    border_radius=40,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=10),
                ft.Text(
                    a.get("NomeAluno", ""),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, size=16, color=ft.Colors.GREY_600),
                        ft.Text(
                            a.get("NomeEscola", "Sem escola"),
                            size=14,
                            color=cor_texto_medio,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Divider(height=20, color=cor_borda),
                ft.Row(
                    [
                        _info_box("Ano", f"{a.get('Ano', '?')}º", cor_primaria),
                        _info_box("Turma", a.get("Turma", "?"), cor_primaria),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.BADGE, size=16, color=ft.Colors.GREY_600),
                            ft.Text(
                                f"Nº Processo: {a.get('nProcessoAluno', 'N/A')}",
                                size=13,
                                color=cor_texto_medio,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    margin=ft.margin.only(top=10),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=cor_card,
        padding=25,
        border_radius=16,
        width=400,
    )


def _info_box(label, valor, cor):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(label, size=11, color=cor_texto_medio),
                ft.Text(
                    valor,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=cor,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, cor),
        padding=15,
        border_radius=12,
        expand=True,
    )


# ======================
# VIEW PRINCIPAL
# ======================

def criar_alunos_view(alunos, page):
    estado = {"pagina": 0, "total": len(alunos), "filtro": ""}
    lista = ft.ListView(expand=True, spacing=12, padding=10)


    def carregar_pagina():
        lista.controls.clear()
        filtro = estado["filtro"].strip().lower()
        filtrados = [
            a
            for a in alunos
            if filtro in a.get("NomeAluno", "").lower()
            or filtro in str(a.get("nProcessoAluno", ""))
        ] if filtro else alunos

        estado["total"] = len(filtrados)
        inicio, fim = estado["pagina"] * PAGE_SIZE, (estado["pagina"] + 1) * PAGE_SIZE
        pagina = filtrados[inicio:fim]

        for a in pagina:
            lista.controls.append(card_aluno_simples(a, page) if CARD_SIMPLES else card_aluno_completo(a))

        total_paginas = max(1, (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE)
        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado['pagina'] + 1)
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} alunos"
        page.update()

    def prox_page(e):
        total_paginas = max(1, (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE)
        if estado["pagina"] + 1 < total_paginas:
            estado["pagina"] += 1
            carregar_pagina()

    def prev_page(e):
        if estado["pagina"] > 0:
            estado["pagina"] -= 1
            carregar_pagina()

    def on_search(e):
        estado["filtro"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def ir_para_pagina(e):
        try:
            nova = int(campo_pagina.value) - 1
            total_paginas = max(1, (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE)
            if 0 <= nova < total_paginas:
                estado["pagina"] = nova
                carregar_pagina()
            else:
                campo_pagina.value = str(estado['pagina'] + 1)
            page.update()
        except ValueError:
            campo_pagina.value = str(estado['pagina'] + 1)
            page.update()

    def on_enter_pagina(e):
        ir_para_pagina(e)

    # HEADER
    info_resultados = ft.Text(
        f"A mostrar {min(PAGE_SIZE, len(alunos))} de {len(alunos)} alunos",
        size=13,
        color=cor_texto_medio,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.GROUPS, size=28, color=ft.Colors.WHITE),
                            width=48,
                            height=48,
                            bgcolor=cor_primaria,
                            border_radius=12,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text("Lista de Alunos", size=26, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Text("Gestão rápida e visual dos alunos", size=12, color=cor_texto_medio),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),

                        # ✅ Botão restaurado
                        estilo_botao_acao(
                            "Adicionar Aluno",
                            ft.Icons.ADD_CIRCLE_ROUNDED,
                            lambda e: page.go("/CriarAluno"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=12,
                ),
                ft.Container(height=15),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SEARCH, size=20, color=cor_texto_medio),
                        ft.Container(
                            content=ft.TextField(
                                hint_text="Pesquisar por nome ou número...",
                                on_change=on_search,
                                border_radius=12,
                                bgcolor=cor_borda,
                                focused_border_color=cor_primaria,
                                text_size=14,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=5),
                info_resultados,
            ],
            spacing=0,
        ),
        padding=20,
        bgcolor=cor_card,
        border_radius=12,
    )

    # FOOTER
    indicador_pagina_text = ft.Text("Página 1 de 1", size=14, weight=ft.FontWeight.W_600, color=cor_texto_medio)
    campo_pagina = ft.TextField(value="1", width=60, text_align=ft.TextAlign.CENTER, on_submit=on_enter_pagina)

    footer = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton("← Anterior", on_click=prev_page, style=ft.ButtonStyle(bgcolor=cor_borda)),
                ft.Container(expand=True),
                ft.Row(
                    [
                        indicador_pagina_text,
                        ft.Text("Ir para:", size=14, color=cor_texto_medio),
                        campo_pagina,
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=cor_primaria,
                            on_click=ir_para_pagina,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton("Seguinte →", on_click=prox_page, style=ft.ButtonStyle(bgcolor=cor_primaria)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=15,
        bgcolor=cor_card,
        border_radius=12,
    )

    carregar_pagina()

    # LAYOUT FINAL
    return ft.Container(
        content=ft.Column(
            [header, ft.Container(height=15), lista, ft.Container(height=15), footer],
            expand=True,
            spacing=0,
        ),
        bgcolor=cor_fundo,
        padding=20,
        expand=True,
    )
