import flet as ft
from .estilosAdmin import *
from .util_buttons import estilo_botao_acao

PAGE_SIZE = 20  

def gerar_sigla(nome: str) -> str:
    if not nome:
        return ""
    partes = [p for p in nome.split() if p]
    sigla = "".join([p[0] for p in partes])
    return ''.join([c for c in sigla.upper() if c.isalnum()])


# ======================
#  CARDS
# ======================

def criar_card_escola(escola, page):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color="#FFFFFF", size=18),
                    bgcolor=cor_primaria,
                    width=36,
                    height=36,
                    border_radius=18,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(
                            gerar_sigla(escola.get("NomeEscola", "")),
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            escola.get("NomeEscola", ""),
                            size=11,
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    color=cor_primaria,
                    size=12,
                ),
            ],
            spacing=10,
        ),
        bgcolor=cor_card,
        tooltip=escola.get("NomeEscola", ""),
        on_click=lambda e, esc=escola: (
            page.session.set("escola_detalhes_id", esc["idEscola"]),
            page.go("/maisDetalhesEscolas"),
        ),
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


# ======================
#  VIEW PRINCIPAL
# ======================

def criar_escolas_view(escolas, page):

    # ——— ESTADO VAZIO ———
    if not escolas:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SCHOOL_OUTLINED,
                            size=80,
                            color=cor_texto_medio,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.05, cor_texto_medio),
                        padding=30,
                        border_radius=100,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Nenhuma escola registada",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=cor_texto_claro,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "A lista de escolas está vazia",
                        size=14,
                        color=cor_texto_medio,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=20),
                    estilo_botao_acao(
                        "Adicionar Primeira Escola",
                        ft.Icons.ADD_CIRCLE_ROUNDED,
                        lambda e: page.go("/criar-escola"),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=40,
        )

    # ——— ESTADO ———
    estado = {
        "pagina": 0,
        "total": len(escolas),
        "filtro": "",
        "escolas_filtradas": escolas,
    }

    lista = ft.ListView(expand=True, spacing=6, padding=ft.padding.symmetric(horizontal=4, vertical=6))

    # ======================
    #  FUNÇÕES DE FILTRO E PAGINAÇÃO
    # ======================

    def filtrar_escolas():
        filtro_raw = estado["filtro"].strip()
        if not filtro_raw:
            estado["escolas_filtradas"] = escolas
            return
        filtro_lower = filtro_raw.lower()
        estado["escolas_filtradas"] = [
            e for e in escolas
            if filtro_lower in e.get("NomeEscola", "").lower()
        ]

    def carregar_pagina():
        lista.controls.clear()
        filtrar_escolas()

        estado["total"] = len(estado["escolas_filtradas"])
        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE
        pagina = estado["escolas_filtradas"][inicio:fim]

        for e in pagina:
            lista.controls.append(criar_card_escola(e, page))

        # Atualiza info resultados
        info_resultados.value = f"{len(pagina)} de {estado['total']} escolas"

        # Total de páginas
        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if total_paginas == 0:
            total_paginas = 1

        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado['pagina'] + 1)

        # Botões anteriores/seguinte
        btn_anterior.disabled = (estado["pagina"] == 0)
        btn_seguinte.disabled = (estado["pagina"] + 1) >= total_paginas

        page.update()

    def prox_page(e):
        if not btn_seguinte.disabled:
            estado["pagina"] += 1
            carregar_pagina()

    def prev_page(e):
        if not btn_anterior.disabled:
            estado["pagina"] -= 1
            carregar_pagina()

    def on_search(e):
        estado["filtro"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def ir_para_pagina(e):
        try:
            nova_pagina = int(campo_pagina.value) - 1
            total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
            if total_paginas == 0:
                total_paginas = 1
            if 0 <= nova_pagina < total_paginas:
                estado["pagina"] = nova_pagina
                carregar_pagina()
            else:
                campo_pagina.value = str(estado['pagina'] + 1)
        except ValueError:
            campo_pagina.value = str(estado['pagina'] + 1)
        page.update()

    def on_enter_pagina(e):
        ir_para_pagina(e)

    # ======================
    #  HEADER
    # ======================

    info_resultados = ft.Text(
        f"{min(PAGE_SIZE, len(escolas))} de {len(escolas)} escolas",
        size=12,
        color=cor_texto_medio,
        weight=ft.FontWeight.W_500,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=24, color=ft.Colors.WHITE),
                            width=48,
                            height=48,
                            bgcolor=cor_primaria,
                            border_radius=14,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.4, cor_primaria),
                                offset=ft.Offset(0, 3),
                            ),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Escolas",
                                    size=20,
                                    weight=ft.FontWeight.W_700,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão de escolas registadas",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=1,
                        ),
                        ft.Container(expand=True),
                        # BOTÃO DO ADMIN
                        estilo_botao_acao(
                            "Adicionar Escola",
                            ft.Icons.ADD_CIRCLE_ROUNDED,
                            lambda e: page.go("/criar-escola"),
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(height=12),
                # CARD DE PESQUISA
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.SEARCH_ROUNDED, size=16, color=cor_primaria),
                                    ft.Text("Pesquisa", size=13, weight=ft.FontWeight.W_600, color=cor_texto_claro),
                                    ft.Container(expand=True),
                                    info_resultados,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),
                            ft.TextField(
                                hint_text="Pesquisar escolas por nome...",
                                on_change=on_search,
                                border_radius=8,
                                filled=True,
                                bgcolor=cor_fundo,
                                border_color=cor_borda,
                                focused_border_color=cor_primaria,
                                hint_style=ft.TextStyle(color=cor_texto_medio, size=12),
                                color=cor_texto_claro,
                                text_size=12,
                                content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                                prefix_icon=ft.Icons.SEARCH,
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
    #  FOOTER
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

    btn_anterior = ft.ElevatedButton(
        "Anterior",
        on_click=prev_page,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor=cor_fundo,
            color=cor_texto_claro,
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=0,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            overlay_color=ft.Colors.with_opacity(0.1, cor_primaria),
        ),
        icon=ft.Icons.ARROW_BACK_ROUNDED,
    )

    btn_seguinte = ft.ElevatedButton(
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
    )

    footer = ft.Container(
        content=ft.Row(
            [
                btn_anterior,
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
                btn_seguinte,
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

    # ======================
    #  LAYOUT FINAL
    # ======================

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
