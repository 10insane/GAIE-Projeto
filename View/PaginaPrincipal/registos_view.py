# Views/PaginaPrincipal/registos_view.py

import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao


# ======================
#  CONFIGURAÇÃO
# ======================

PAGE_SIZE = 25  # Mostra 25 registos por página


# ======================
#  CARDS
# ======================

def criar_card_registo(registo, page):
    """Card de registo com design moderno e clean - OTIMIZADO"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone do registo
                ft.Container(
                    content=ft.Icon(ft.Icons.ASSIGNMENT, color="#FFFFFF", size=24),
                    bgcolor=cor_secundaria,
                    padding=10,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.25, cor_secundaria),
                        offset=ft.Offset(0, 4),
                    ),
                ),

                # Informações do registo
                ft.Column(
                    [
                        # Número do registo
                        ft.Text(
                            f"Registo #{registo.get('nPIA', 'N/A')}",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),

                        ft.Container(height=4),

                        # Linha 1: Aluno e Estado
                        ft.Row(
                            [
                                # Aluno
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PERSON, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                registo.get('NomeAluno', 'N/A'),
                                                size=12,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.08, cor_texto_medio),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=6,
                                ),

                                # Estado
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.FLAG, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                registo.get('Estado', 'N/A'),
                                                size=12,
                                                color=cor_texto_medio,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.08, cor_texto_medio),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=6,
                                ),
                            ],
                            spacing=8,
                        ),

                        ft.Container(height=2),

                        # Linha 2: Data e Técnico
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=11, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('DataEntradaSPO', 'N/A'),
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                                ft.Text("•", size=11, color=cor_texto_medio),
                                ft.Icon(ft.Icons.PERSON_OUTLINE, size=11, color=cor_texto_medio),
                                ft.Text(
                                    registo.get('NomeTecnico', 'N/A'),
                                    size=11,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),

                # Botão de ação
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_color="#FFFFFF",
                        bgcolor="#F59E0B",
                        tooltip="Editar registo",
                        icon_size=18,
                        on_click=lambda e, a=registo: (
                            page.session.set("registo_editar_id", a["nPIA"]),
                            page.go("/EditarRegisto")
                        ),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=14,
        ),

        bgcolor=cor_card,
        padding=16,
        border_radius=14,
        border=ft.border.all(2, ft.Colors.with_opacity(0.15, cor_secundaria)),
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, cor_secundaria),
            offset=ft.Offset(0, 4),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


# ======================
#  VIEW PRINCIPAL
# ======================

def criar_registos_view(registos, page):
    """View principal da lista de registos - OTIMIZADO com paginação e busca"""

    # ——— ESTADO VAZIO ———
    if not registos:
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

    # ——— VIEW COM REGISTOS (OTIMIZADO) ———

    estado = {
        "pagina": 0,
        "total": len(registos),
        "filtro": "",
        "registos_filtrados": registos,
    }

    lista = ft.ListView(expand=True, spacing=12, padding=10)

    def filtrar_registos():
        """Filtra registos por nPIA, nome do aluno, estado ou técnico"""
        filtro_raw = estado["filtro"].strip()

        if not filtro_raw:
            estado["registos_filtrados"] = registos
            return

        filtro_lower = filtro_raw.lower()
        estado["registos_filtrados"] = [
            r for r in registos
            if (
                filtro_raw in str(r.get("nPIA", ""))  # Busca por número
                or filtro_lower in r.get("NomeAluno", "").lower()  # Busca por nome aluno
                or filtro_lower in r.get("Estado", "").lower()  # Busca por estado
                or filtro_lower in r.get("NomeTecnico", "").lower()  # Busca por técnico
            )
        ]

    def carregar_pagina():
        """Carrega apenas a página atual - OTIMIZADO"""
        lista.controls.clear()

        # Garante que o filtro está aplicado
        filtro_raw = estado["filtro"].strip()
        if filtro_raw:
            filtrar_registos()
        else:
            estado["registos_filtrados"] = registos

        estado["total"] = len(estado["registos_filtrados"])
        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE
        pagina = estado["registos_filtrados"][inicio:fim]

        # Renderiza apenas os cards visíveis
        for r in pagina:
            lista.controls.append(criar_card_registo(r, page))

        # Atualiza info
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} registos"

        # Atualiza texto da página / indicador
        total_paginas = max(1, (estado['total'] + PAGE_SIZE - 1) // PAGE_SIZE)
        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"

        # Atualiza campo de página
        campo_pagina.value = str(estado['pagina'] + 1)

        # Atualiza botões
        btn_anterior.disabled = estado["pagina"] == 0
        btn_seguinte.disabled = (estado["pagina"] + 1) >= total_paginas

        page.update()

    def prox_page(e):
        total_paginas = max(1, (estado['total'] + PAGE_SIZE - 1) // PAGE_SIZE)
        if (estado["pagina"] + 1) < total_paginas:
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
        """Vai para uma página específica"""
        try:
            nova_pagina = int(campo_pagina.value) - 1
            total_paginas = max(1, (estado['total'] + PAGE_SIZE - 1) // PAGE_SIZE)
            if 0 <= nova_pagina < total_paginas:
                estado["pagina"] = nova_pagina
                carregar_pagina()
            else:
                campo_pagina.value = str(estado['pagina'] + 1)
                page.update()
        except ValueError:
            campo_pagina.value = str(estado['pagina'] + 1)
            page.update()

    def on_enter_pagina(e):
        """Quando pressionar Enter no campo de página"""
        ir_para_pagina(e)

    # ======================
    #  HEADER MODERNO
    # ======================

    info_resultados = ft.Text(
        f"A mostrar {min(PAGE_SIZE, len(registos))} de {len(registos)} registos",
        size=13,
        color=cor_texto_medio,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.ASSIGNMENT, size=28, color=ft.Colors.WHITE),
                            width=48,
                            height=48,
                            bgcolor=cor_secundaria,
                            border_radius=12,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=8,
                                color=ft.Colors.with_opacity(0.14, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4),
                            ),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Registos",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão de processos e acompanhamentos",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        str(len(registos)),
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_secundaria,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.15, cor_secundaria),
                                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                    border_radius=20,
                                ),
                                estilo_botao_acao(
                                    "Novo Registo",
                                    ft.Icons.ADD_CIRCLE_ROUNDED,
                                    lambda e: page.go("/criar-registo")
                                ),
                            ],
                            spacing=12,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),

                ft.Container(height=15),

                # Barra de pesquisa multi-campo
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SEARCH, size=18, color=cor_texto_medio),
                            width=44,
                            height=44,
                            bgcolor=cor_borda,
                            border_radius=12,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=10),
                        ft.Container(
                            content=ft.TextField(
                                hint_text="Pesquisar por nº registo, aluno, estado ou técnico...",
                                on_change=on_search,
                                border_radius=12,
                                filled=True,
                                bgcolor=cor_borda,
                                border_color=cor_borda,
                                focused_border_color=cor_secundaria,
                                hint_style=ft.TextStyle(color=cor_texto_medio),
                                text_size=14,
                                content_padding=ft.padding.symmetric(horizontal=18, vertical=12),
                                width=500,
                            ),
                        ),
                    ],
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
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )

    # ======================
    #  FOOTER MODERNO (IGUAL AO DOS ALUNOS)
    # ======================

    # Indicador de página
    indicador_pagina_text = ft.Text(
        "Página 1 de 1",
        size=14,
        weight=ft.FontWeight.W_600,
        color=cor_texto_medio,
    )

    # Campo para digitar o número da página
    campo_pagina = ft.TextField(
        value="1",
        width=70,
        height=40,
        text_size=14,
        text_align=ft.TextAlign.CENTER,
        content_padding=ft.padding.all(10),
        border_radius=8,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        on_submit=on_enter_pagina,
    )

    # Botões anterior e seguinte
    btn_anterior = ft.ElevatedButton(
        "← Anterior",
        on_click=prev_page,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor=cor_borda,
            color=cor_texto_claro,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2,
        ),
        icon=ft.Icons.ARROW_BACK,
    )

    btn_seguinte = ft.ElevatedButton(
        "Seguinte →",
        on_click=prox_page,
        style=ft.ButtonStyle(
            bgcolor=cor_secundaria,
            color=cor_texto_claro,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2,
        ),
        icon=ft.Icons.ARROW_FORWARD,
    )

    footer = ft.Container(
        content=ft.Row(
            [
                # Botão Anterior
                btn_anterior,

                ft.Container(expand=True),

                # Seção de navegação de página
                ft.Row(
                    [
                        ft.Container(
                            content=indicador_pagina_text,
                            bgcolor=ft.Colors.with_opacity(0.1, cor_secundaria),
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                            border_radius=20,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.2, cor_secundaria)),
                        ),
                        ft.Container(width=10),
                        ft.Text("Ir para:", size=14, color=cor_texto_medio),
                        ft.Container(width=5),
                        campo_pagina,
                        ft.Container(width=5),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=cor_secundaria,
                            on_click=ir_para_pagina,
                            tooltip="Ir para página",
                            icon_size=18,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                ft.Container(expand=True),

                # Botão Seguinte
                btn_seguinte,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        bgcolor=cor_card,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, -2),
        ),
    )

    # Carrega primeira página
    carregar_pagina()

    # ======================
    #  LAYOUT FINAL
    # ======================

    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(height=15),
                lista,
                ft.Container(height=15),
                footer,
            ],
            expand=True,
            spacing=0,
        ),
        bgcolor=cor_fundo,
        padding=20,
        expand=True,
    )
