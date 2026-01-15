import flet as ft
from .estilosAdmin import *
from .util_buttons import estilo_botao_acao
import re

PAGE_SIZE = 50
CARD_SIMPLES = True


# ======================
# CARDS
# ======================

def card_aluno_simples(a, page):
    """Card compacto com efeito neon"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=18),
                    width=36,
                    height=36,
                    bgcolor=cor_primaria,
                    border_radius=18,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(
                            a.get("NomeAluno", ""),
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=cor_texto_claro,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        f"{a.get('Ano','?')}º",
                                        size=10,
                                        weight=ft.FontWeight.W_500,
                                        color=cor_primaria,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.15, cor_primaria),
                                    padding=ft.padding.symmetric(horizontal=6, vertical=1),
                                    border_radius=8,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"Turma {a.get('Turma','?')}",
                                        size=10,
                                        weight=ft.FontWeight.W_500,
                                        color=cor_secundaria,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.15, cor_secundaria),
                                    padding=ft.padding.symmetric(horizontal=6, vertical=1),
                                    border_radius=8,
                                ),
                                ft.Text(
                                    f"Nº {a.get('nProcessoAluno', 'N/A')}",
                                    size=10,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    color=cor_primaria,
                    size=12,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=10,
        border_radius=10,
        bgcolor=cor_card,
        border=ft.border.all(1, cor_borda),
        on_click=lambda e: (
            page.session.set("aluno_detalhes_id", a["nProcessoAluno"]),
            page.go("/maisDetalhesAlunos")
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ink=True,
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

    lista = ft.ListView(expand=True, spacing=6, padding=ft.padding.symmetric(horizontal=4, vertical=6))

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
            lista.controls.append(card_aluno_simples(a, page))

        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if total_paginas == 0:
            total_paginas = 1

        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado["pagina"] + 1)
        info_resultados.value = f"{len(pagina)} de {estado['total']} alunos"
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
    # HEADER + FILTROS ADMIN
    # ======================

    info_resultados = ft.Text(
        f"{min(PAGE_SIZE, len(alunos))} de {len(alunos)} alunos",
        size=12,
        color=cor_texto_medio,
        weight=ft.FontWeight.W_500,
    )

    campo_nome = ft.TextField(
        hint_text="Procurar por nome ou número...",
        on_change=on_search_nome,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        expand=True,
        prefix_icon=ft.Icons.SEARCH,
    )

    campo_turma = ft.TextField(
        hint_text="Turma",
        on_change=on_search_turma,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=100,
    )

    campo_ano = ft.TextField(
        hint_text="Ano",
        on_change=on_search_ano,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=90,
    )

    header = ft.Container(
        content=ft.Column(
            [
                # Título e botão adicionar
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.GROUPS_ROUNDED,
                                size=24,
                                color=ft.Colors.WHITE,
                            ),
                            width=48,
                            height=48,
                            bgcolor=cor_primaria,
                            border_radius=14,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Alunos",
                                    size=20,
                                    weight=ft.FontWeight.W_700,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão e consulta rápida",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=1,
                        ),
                        ft.Container(expand=True),
                        # Botão Adicionar
                        estilo_botao_acao(
                            "Adicionar Aluno",
                            ft.Icons.ADD_CIRCLE_ROUNDED,
                            lambda e: page.go("/CriarAluno"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),
                
                ft.Container(height=12),

                # Card de filtros moderno
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.TUNE_ROUNDED,
                                        size=16,
                                        color=cor_primaria,
                                    ),
                                    ft.Text(
                                        "Filtros",
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=cor_texto_claro,
                                    ),
                                    ft.Container(expand=True),
                                    info_resultados,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    campo_nome,
                                    campo_turma,
                                    campo_ano,
                                    ft.ElevatedButton(
                                        "Limpar",
                                        on_click=limpar_filtros,
                                        icon=ft.Icons.CLEAR_ALL_ROUNDED,
                                        style=ft.ButtonStyle(
                                            bgcolor=cor_fundo,
                                            color=cor_texto_claro,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            elevation=0,
                                            padding=ft.padding.symmetric(horizontal=12, vertical=10),
                                            overlay_color=ft.Colors.with_opacity(0.1, cor_primaria),
                                        ),
                                        height=38,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=14,
                    bgcolor=cor_card,
                    border_radius=10,
                    border=ft.border.all(1, cor_borda),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                        offset=ft.Offset(0, 3),
                    ),
                ),
            ],
            spacing=0,
        ),
        padding=14,
        bgcolor=cor_card,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )

    # ======================
    # FOOTER
    # ======================

    indicador_pagina_text = ft.Text(
        "Página 1 de 1",
        size=14,
        weight=ft.FontWeight.W_600,
        color=cor_texto_claro,
    )

    campo_pagina = ft.TextField(
        value="1",
        width=70,
        height=40,
        text_size=14,
        text_align=ft.TextAlign.CENTER,
        content_padding=ft.padding.all(8),
        border_radius=10,
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
                    "Anterior",
                    on_click=prev_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_fundo,
                        color=cor_texto_claro,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=0,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        overlay_color=ft.Colors.with_opacity(0.1, cor_primaria),
                    ),
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            indicador_pagina_text,
                            ft.Container(
                                content=ft.Container(width=1, height=24, bgcolor=cor_borda),
                                margin=ft.margin.symmetric(horizontal=16),
                            ),
                            ft.Text("Ir para:", size=13, color=cor_texto_medio),
                            campo_pagina,
                            ft.IconButton(
                                icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=cor_primaria,
                                on_click=ir_para_pagina,
                                tooltip="Ir para página",
                                icon_size=18,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                    padding=ft.padding.symmetric(horizontal=20, vertical=8),
                    border_radius=12,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Seguinte",
                    on_click=prox_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_primaria,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=2,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        overlay_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    ),
                    icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=16,
        bgcolor=cor_card,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, -2),
        ),
    )

    carregar_pagina()

    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(height=12),
                lista,
                ft.Container(height=12),
                footer,
            ],
            expand=True,
            spacing=0,
        ),
        bgcolor=cor_fundo,
        padding=16,
        expand=True,
    )