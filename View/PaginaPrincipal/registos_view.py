# Views/PaginaPrincipal/registos_view.py
 
import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao


PAGE_SIZE = 50
 
 
def criar_card_registo(registo, page):
    """Card de registo compacto e moderno"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone do registo
                ft.Container(
                    content=ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED, color="#FFFFFF", size=18),
                    bgcolor=cor_secundaria,
                    width=36,
                    height=36,
                    border_radius=18,
                    alignment=ft.alignment.center,
                ),
 
                # Informações do registo
                ft.Column(
                    [
                        # Número do registo
                        ft.Text(
                            f"Registo #{registo.get('nPIA', 'N/A')}",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=cor_texto_claro,
                        ),
                       
                        # Linha 1: Aluno e Estado
                        ft.Row(
                            [
                                # Aluno
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PERSON, size=11, color=cor_primaria),
                                            ft.Text(
                                                registo.get('NomeAluno', 'N/A'),
                                                size=10,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.12, cor_primaria),
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=6,
                                ),
 
                                # Estado
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.FLAG, size=11, color=cor_secundaria),
                                            ft.Text(
                                                registo.get('Estado', 'N/A'),
                                                size=10,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.12, cor_secundaria),
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=6,
                                ),
                            ],
                            spacing=6,
                        ),
                       
                        # Linha 2: Data e Técnico
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=10, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('DataEntradaSPO', 'N/A'),
                                    size=10,
                                    color=cor_texto_medio,
                                ),
                                ft.Text("•", size=10, color=cor_texto_medio),
                                ft.Icon(ft.Icons.PERSON_OUTLINE, size=10, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('NomeTecnico', 'N/A'),
                                    size=10,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
 
                # Botão de ação
                ft.IconButton(
                    icon=ft.Icons.VISIBILITY,
                    icon_color=cor_secundaria,
                    icon_size=18,
                    tooltip="Ver detalhes",
                    on_click=lambda e, a=registo: (
                        page.session.set("registo_detalhes_id", a["nPIA"]),
                        page.go("/maisDetalhesRegisto")
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
 
        bgcolor=cor_card,
        padding=10,
        border_radius=10,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ink=True,
    )
 
 
def criar_registos_view(registos, page):
    """View principal da lista de registos - OTIMIZADO com paginação"""

    if not registos:
        # ——— Estado vazio ———
        return ft.Container(
            content=ft.Column(
                [
                    # Ícone grande
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ASSIGNMENT_OUTLINED,
                            size=80,
                            color=cor_texto_medio,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.05, cor_texto_medio),
                        padding=30,
                        border_radius=100,
                    ),
                   
                    ft.Container(height=8),
                   
                    # Texto principal
                    ft.Text(
                        "Nenhum registo criado",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=cor_texto_claro,
                        text_align=ft.TextAlign.CENTER,
                    ),
                   
                    # Subtexto
                    ft.Text(
                        "Comece por adicionar o primeiro registo",
                        size=14,
                        color=cor_texto_medio,
                        text_align=ft.TextAlign.CENTER,
                    ),
                   
                    ft.Container(height=20),
                   
                    # Botão
                    estilo_botao_acao(
                        "Adicionar Primeiro Registo",
                        ft.Icons.ADD_CIRCLE_ROUNDED,
                        lambda e: page.go("/criar-registo")
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=40,
        )

    # ——— VIEW COM REGISTOS (COM PAGINAÇÃO) ———

    estado = {
        "pagina": 0,
        "total": len(registos),
        "filtro_numero": "",
        "filtro_aluno": "",
        "filtro_estado": "",
    }

    lista = ft.ListView(expand=True, spacing=6, padding=ft.padding.symmetric(horizontal=4, vertical=6))

    def carregar_pagina():
        """Carrega apenas a página atual com filtros"""
        lista.controls.clear()

        filtro_numero = estado["filtro_numero"].strip().lower()
        filtro_aluno = estado["filtro_aluno"].strip().lower()
        filtro_estado = estado["filtro_estado"].strip().lower()

        registos_filtrados = []

        for r in registos:
            passa_filtro = True

            if filtro_numero:
                npia = str(r.get("nPIA", "")).lower()
                if filtro_numero not in npia:
                    passa_filtro = False

            if filtro_aluno and passa_filtro:
                aluno = r.get("NomeAluno", "").lower()
                if filtro_aluno not in aluno:
                    passa_filtro = False

            if filtro_estado and passa_filtro:
                estado_reg = r.get("Estado", "").lower()
                if filtro_estado not in estado_reg:
                    passa_filtro = False

            if passa_filtro:
                registos_filtrados.append(r)

        estado["total"] = len(registos_filtrados)

        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE
        pagina = registos_filtrados[inicio:fim]

        for r in pagina:
            lista.controls.append(criar_card_registo(r, page))

        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if total_paginas == 0:
            total_paginas = 1

        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado["pagina"] + 1)
        info_resultados.value = f"{len(pagina)} de {estado['total']} registos"
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

    def on_search_numero(e):
        estado["filtro_numero"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def on_search_aluno(e):
        estado["filtro_aluno"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def on_search_estado(e):
        estado["filtro_estado"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def limpar_filtros(e):
        campo_numero.value = ""
        campo_aluno.value = ""
        campo_estado.value = ""
        estado["filtro_numero"] = ""
        estado["filtro_aluno"] = ""
        estado["filtro_estado"] = ""
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
        f"{min(PAGE_SIZE, len(registos))} de {len(registos)} registos",
        size=12,
        color=cor_texto_medio,
        weight=ft.FontWeight.W_500,
    )

    campo_numero = ft.TextField(
        hint_text="Nº Registo",
        on_change=on_search_numero,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=120,
    )

    campo_aluno = ft.TextField(
        hint_text="Nome do aluno",
        on_change=on_search_aluno,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        expand=True,
        prefix_icon=ft.Icons.PERSON_SEARCH,
    )

    campo_estado = ft.TextField(
        hint_text="Estado",
        on_change=on_search_estado,
        border_radius=8,
        filled=True,
        bgcolor=cor_fundo,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
        color=cor_texto_claro,
        text_size=12,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=120,
    )

    header = ft.Container(
        content=ft.Column(
            [
                # Título principal
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.ASSIGNMENT_ROUNDED,
                                size=24,
                                color=ft.Colors.WHITE,
                            ),
                            width=48,
                            height=48,
                            bgcolor=cor_secundaria,
                            border_radius=14,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.4, cor_secundaria),
                                offset=ft.Offset(0, 3),
                            ),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Registos",
                                    size=20,
                                    weight=ft.FontWeight.W_700,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão de registos de alunos",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=1,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        str(len(registos)),
                                        size=20,
                                        weight=ft.FontWeight.W_700,
                                        color=cor_secundaria,
                                    ),
                                    ft.Text(
                                        "Total",
                                        size=10,
                                        color=cor_texto_medio,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.12, cor_secundaria),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=10,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.2, cor_secundaria)),
                        ),
                        ft.Container(width=12),
                        estilo_botao_acao(
                            "Adicionar",
                            ft.Icons.ADD_CIRCLE_ROUNDED,
                            lambda e: page.go("/criar-registo")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),
                
                ft.Container(height=12),

                # Card de filtros
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.TUNE_ROUNDED,
                                        size=16,
                                        color=cor_secundaria,
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
                                    campo_numero,
                                    campo_aluno,
                                    campo_estado,
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
                                            overlay_color=ft.Colors.with_opacity(0.1, cor_secundaria),
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
        focused_border_color=cor_secundaria,
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
                        overlay_color=ft.Colors.with_opacity(0.1, cor_secundaria),
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
                                bgcolor=cor_secundaria,
                                on_click=ir_para_pagina,
                                tooltip="Ir para página",
                                icon_size=18,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.08, cor_secundaria),
                    padding=ft.padding.symmetric(horizontal=20, vertical=8),
                    border_radius=12,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Seguinte",
                    on_click=prox_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_secundaria,
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