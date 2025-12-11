import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao
import re

PAGE_SIZE = 50
CARD_SIMPLES = True


# ======================
# CARDS
# ======================

def card_aluno_simples(a, abrir_detalhe):
    """Card compacto e clean"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=20),
                    width=40,
                    height=40,
                    bgcolor=cor_primaria,
                    border_radius=20,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(
                            a.get("NomeAluno", ""),
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=cor_texto_claro,
                        ),
                        ft.Row(
                            [
                                ft.Text(
                                    f"{a.get('Ano','?')}º ano",
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                                ft.Text(
                                    f"Turma {a.get('Turma','?')}",
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                                ft.Text(
                                    f"Nº {a.get('nProcessoAluno', 'N/A')}",
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    color=ft.Colors.GREY_400,
                    size=16,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=10,
        border_radius=8,
        bgcolor=cor_card,
        on_click=lambda e: abrir_detalhe(a),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )


def card_aluno_completo(a):
    """Card de detalhes mais leve e compacto"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=32),
                    width=64,
                    height=64,
                    bgcolor=cor_primaria,
                    border_radius=32,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=6),
                ft.Text(
                    a.get("NomeAluno", ""),
                    size=18,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER,
                    color=cor_texto_claro,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, size=14, color=cor_texto_medio),
                        ft.Text(
                            a.get("NomeEscola", ""),
                            size=12,
                            color=cor_texto_medio,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                ),
                ft.Divider(height=16, color=cor_borda),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Ano", size=11, color=cor_texto_medio),
                                    ft.Text(
                                        f"{a.get('Ano','?')}º",
                                        size=18,
                                        weight=ft.FontWeight.W_600,
                                        color=cor_primaria,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=10,
                            border_radius=10,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Turma", size=11, color=cor_texto_medio),
                                    ft.Text(
                                        a.get("Turma", "?"),
                                        size=18,
                                        weight=ft.FontWeight.W_600,
                                        color=cor_primaria,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=10,
                            border_radius=10,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.BADGE, size=14, color=cor_texto_medio),
                            ft.Text(
                                f"Nº Processo: {a.get('nProcessoAluno', 'N/A')}",
                                size=12,
                                color=cor_texto_medio,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                    ),
                    margin=ft.margin.only(top=8),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        width=360,
    )


# ======================
# VIEW PRINCIPAL
# ======================

def criar_alunos_view(alunos, page):
    estado = {
        "pagina": 0,
        "total": len(alunos),
        "filtro_nome": "",
        "filtro_turma": "",
        "filtro_ano": "",
    }

    lista = ft.ListView(expand=True, spacing=8, padding=8)

    # --------- Dialog de detalhe ---------

    def abrir_detalhe(a):
        page.dialog = ft.AlertDialog(
            modal=True,
            content=card_aluno_completo(a),
            actions=[
                ft.TextButton(
                    "Fechar",
                    on_click=lambda e: fechar_dialog(),
                    style=ft.ButtonStyle(
                        color=cor_primaria,
                    ),
                ),
            ],
            shape=ft.RoundedRectangleBorder(radius=12),
        )
        page.dialog.open = True
        page.update()

    def fechar_dialog():
        page.dialog.open = False
        page.update()

    # --------- Paginação e filtros ---------

    def carregar_pagina():
        lista.controls.clear()

        filtro_nome = estado["filtro_nome"].strip().lower()
        filtro_turma = estado["filtro_turma"].strip().upper()
        filtro_ano = estado["filtro_ano"].strip()

        alunos_filtrados = []

        for a in alunos:
            passa_filtro = True

            if filtro_nome:
                nome = a.get("NomeAluno", "").lower()
                nproc = str(a.get("nProcessoAluno", ""))
                if filtro_nome not in nome and filtro_nome not in nproc:
                    passa_filtro = False

            if filtro_turma and passa_filtro:
                turma = str(a.get("Turma", "")).upper()
                if filtro_turma != turma:
                    passa_filtro = False

            if filtro_ano and passa_filtro:
                ano = str(a.get("Ano", ""))
                if filtro_ano != ano:
                    passa_filtro = False

            if passa_filtro:
                alunos_filtrados.append(a)

        estado["total"] = len(alunos_filtrados)

        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE
        pagina = alunos_filtrados[inicio:fim]

        for a in pagina:
            if CARD_SIMPLES:
                lista.controls.append(card_aluno_simples(a, abrir_detalhe))
            else:
                lista.controls.append(card_aluno_completo(a))

        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if total_paginas == 0:
            total_paginas = 1

        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado["pagina"] + 1)
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} alunos"
        page.update()

    def prox_page(e):
        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if (estado["pagina"] + 1) < total_paginas:
            estado["pagina"] += 1
            carregar_pagina()

    def prev_page(e):
        if estado["pagina"] > 0:
            estado["pagina"] -= 1
            carregar_pagina()

    def on_search_nome(e):
        estado["filtro_nome"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def on_search_turma(e):
        estado["filtro_turma"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def on_search_ano(e):
        estado["filtro_ano"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def limpar_filtros(e):
        campo_nome.value = ""
        campo_turma.value = ""
        campo_ano.value = ""
        estado["filtro_nome"] = ""
        estado["filtro_turma"] = ""
        estado["filtro_ano"] = ""
        estado["pagina"] = 0
        carregar_pagina()

    def ir_para_pagina(e):
        try:
            nova_pagina = int(campo_pagina.value) - 1
            total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE

            if 0 <= nova_pagina < total_paginas:
                estado["pagina"] = nova_pagina
                carregar_pagina()
            else:
                campo_pagina.value = str(estado["pagina"] + 1)
                page.update()
        except ValueError:
            campo_pagina.value = str(estado["pagina"] + 1)
            page.update()

    def on_enter_pagina(e):
        ir_para_pagina(e)

    # ======================
    # HEADER + FILTROS
    # ======================

    info_resultados = ft.Text(
        f"A mostrar {min(PAGE_SIZE, len(alunos))} de {len(alunos)} alunos",
        size=12,
        color=cor_texto_medio,
    )

    # Campos em dark theme com as tuas cores
    campo_nome = ft.TextField(
        hint_text="Nome ou nº do aluno",
        on_change=on_search_nome,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio),
        color=cor_texto_claro,
        text_size=13,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        expand=True,
    )

    campo_turma = ft.TextField(
        hint_text="Turma (ex: A, B, C)",
        on_change=on_search_turma,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio),
        color=cor_texto_claro,
        text_size=13,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        width=110,
    )

    campo_ano = ft.TextField(
        hint_text="Ano (ex: 5, 6, 7)",
        on_change=on_search_ano,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio),
        color=cor_texto_claro,
        text_size=13,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        width=90,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.GROUPS,
                                size=24,
                                color=ft.Colors.WHITE,
                            ),
                            width=40,
                            height=40,
                            bgcolor=cor_primaria,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Alunos",
                                    size=20,
                                    weight=ft.FontWeight.W_600,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão rápida dos alunos",
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                str(len(alunos)),
                                size=16,
                                weight=ft.FontWeight.W_600,
                                color=cor_primaria,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.12, cor_primaria),
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=16,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                ft.Container(height=10),

                # Card de filtros com as tuas cores
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "Filtros",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=cor_primaria,
                                    ),
                                    ft.Container(expand=True),
                                    ft.Icon(
                                        ft.Icons.FILTER_ALT,
                                        size=18,
                                        color=cor_primaria,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=8),
                            ft.Row(
                                [
                                    # Nome / Número
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(
                                                            ft.Icons.PERSON_SEARCH,
                                                            size=16,
                                                            color=cor_primaria,
                                                        ),
                                                        ft.Text(
                                                            "Nome ou Número",
                                                            size=12,
                                                            weight=ft.FontWeight.W_500,
                                                            color=cor_texto_claro,
                                                        ),
                                                    ],
                                                    spacing=4,
                                                ),
                                                campo_nome,
                                            ],
                                            spacing=4,
                                        ),
                                        expand=True,
                                        padding=8,
                                        bgcolor=cor_card,
                                        border_radius=10,
                                        border=ft.border.all(1, cor_borda),
                                    ),
                                    ft.Container(width=8),
                                    # Turma
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(
                                                            ft.Icons.GROUP_WORK,
                                                            size=16,
                                                            color=cor_secundaria,
                                                        ),
                                                        ft.Text(
                                                            "Turma",
                                                            size=12,
                                                            weight=ft.FontWeight.W_500,
                                                            color=cor_texto_claro,
                                                        ),
                                                    ],
                                                    spacing=4,
                                                ),
                                                campo_turma,
                                            ],
                                            spacing=4,
                                        ),
                                        padding=8,
                                        bgcolor=cor_card,
                                        border_radius=10,
                                        border=ft.border.all(1, cor_borda),
                                    ),
                                    ft.Container(width=8),
                                    # Ano
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(
                                                            ft.Icons.SCHEDULE,
                                                            size=16,
                                                            color=ft.Colors.ORANGE_400,
                                                        ),
                                                        ft.Text(
                                                            "Ano",
                                                            size=12,
                                                            weight=ft.FontWeight.W_500,
                                                            color=cor_texto_claro,
                                                        ),
                                                    ],
                                                    spacing=4,
                                                ),
                                                campo_ano,
                                            ],
                                            spacing=4,
                                        ),
                                        padding=8,
                                        bgcolor=cor_card,
                                        border_radius=10,
                                        border=ft.border.all(1, cor_borda),
                                    ),
                                    ft.Container(width=8),
                                    # Limpar
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "Limpar",
                                                    size=12,
                                                    weight=ft.FontWeight.W_500,
                                                    color=cor_texto_claro,
                                                ),
                                                ft.ElevatedButton(
                                                    "Limpar",
                                                    on_click=limpar_filtros,
                                                    icon=ft.Icons.DELETE_SWEEP,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=cor_fundo,
                                                        color=cor_texto_claro,
                                                        shape=ft.RoundedRectangleBorder(
                                                            radius=8
                                                        ),
                                                        elevation=0,
                                                        padding=ft.padding.symmetric(
                                                            horizontal=10, vertical=8
                                                        ),
                                                    ),
                                                    height=36,
                                                ),
                                            ],
                                            spacing=4,
                                        ),
                                        padding=8,
                                        bgcolor=cor_card,
                                        border_radius=10,
                                        border=ft.border.all(1, cor_borda),
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=12,
                    bgcolor=cor_card,
                    border_radius=10,
                    border=ft.border.all(1, cor_borda),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4),
                    ),
                ),
                ft.Container(height=8),
                info_resultados,
            ],
            spacing=0,
        ),
        padding=16,
        bgcolor=cor_card,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 1),
        ),
    )

    # ======================
    # FOOTER
    # ======================

    indicador_pagina_text = ft.Text(
        "Página 1 de 1",
        size=13,
        weight=ft.FontWeight.W_500,
        color=cor_texto_medio,
    )

    campo_pagina = ft.TextField(
        value="1",
        width=60,
        height=34,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        content_padding=ft.padding.all(6),
        border_radius=6,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_claro,
        bgcolor=cor_fundo,
        on_submit=on_enter_pagina,
    )

    footer = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    "← Anterior",
                    on_click=prev_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_borda,
                        color=cor_texto_claro,
                        shape=ft.RoundedRectangleBorder(radius=6),
                        elevation=1,
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    ),
                    icon=ft.Icons.ARROW_BACK,
                ),
                ft.Container(expand=True),
                ft.Row(
                    [
                        ft.Container(
                            content=indicador_pagina_text,
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=16,
                            border=ft.border.all(
                                1,
                                ft.Colors.with_opacity(0.2, cor_primaria),
                            ),
                        ),
                        ft.Container(width=8),
                        ft.Text("Ir para:", size=13, color=cor_texto_medio),
                        ft.Container(width=4),
                        campo_pagina,
                        ft.Container(width=4),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=cor_primaria,
                            on_click=ir_para_pagina,
                            tooltip="Ir para página",
                            icon_size=16,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Seguinte →",
                    on_click=prox_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_primaria,
                        color=cor_texto_claro,
                        shape=ft.RoundedRectangleBorder(radius=6),
                        elevation=1,
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    ),
                    icon=ft.Icons.ARROW_FORWARD,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=10,
        bgcolor=cor_card,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, -1),
        ),
    )

    carregar_pagina()

    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(height=10),
                lista,
                ft.Container(height=10),
                footer,
            ],
            expand=True,
            spacing=0,
        ),
        bgcolor=cor_fundo,
        padding=16,
        expand=True,
    )
