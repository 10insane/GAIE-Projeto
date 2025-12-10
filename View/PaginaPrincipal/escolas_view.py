import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao


# ======================
#  CONFIGURAÇÃO
# ======================

PAGE_SIZE = 20  # Mostra 20 escolas por página


# ======================
#  FUNÇÕES AUXILIARES
# ======================

def gerar_sigla(nome: str) -> str:
    """Gera sigla a partir do nome da escola"""
    if not nome:
        return ""
    partes = [p for p in nome.split() if p]
    sigla = "".join([p[0] for p in partes])
    return ''.join([c for c in sigla.upper() if c.isalnum()])


# ======================
#  CARDS
# ======================

def criar_card_escola(escola, page):
    """Card de escola com design moderno e clean"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone da escola
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=20),
                    bgcolor="#10B981",
                    padding=8,
                    border_radius=10,
                ),

                # Informações da escola
                ft.Column(
                    [
                        ft.Text(
                            gerar_sigla(escola.get("NomeEscola", "")),
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=2),
                        ft.Text(
                            escola.get("NomeEscola", ""),
                            size=12,
                            color=cor_texto_medio,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
        bgcolor=cor_card,
        tooltip=escola.get("NomeEscola", ""),
        padding=12,
        border_radius=12,
        border=ft.border.all(2, ft.Colors.with_opacity(0.15, "#10B981")),
        shadow=ft.BoxShadow(
            blur_radius=16,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, "#10B981"),
            offset=ft.Offset(0, 3),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


# ======================
#  VIEW PRINCIPAL
# ======================

def criar_escolas_view(escolas, page):
    """View principal da lista de escolas - OTIMIZADO com paginação e busca"""

    # ——— ESTADO VAZIO ———
    if not escolas:
        return ft.Container(
            content=ft.Column(
                [
                    # Ícone grande
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

                    # Texto principal
                    ft.Text(
                        "Nenhuma escola registada",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=cor_texto_claro,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    # Subtexto
                    ft.Text(
                        "A lista de escolas está vazia",
                        size=14,
                        color=cor_texto_medio,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(height=20),

                    # Botão
                    estilo_botao_acao(
                        "Adicionar Primeira Escola",
                        ft.Icons.ADD_CIRCLE_ROUNDED,
                        lambda e: page.go("/criar-escola")
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=40,
        )

    # ——— VIEW COM ESCOLAS (OTIMIZADO) ———

    estado = {
        "pagina": 0,
        "total": len(escolas),
        "filtro": "",
        "escolas_filtradas": escolas,
    }

    lista = ft.ListView(expand=True, spacing=10, padding=10)

    def filtrar_escolas():
        """Filtra escolas por nome"""
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
        """Carrega apenas a página atual"""
        lista.controls.clear()

        filtro_raw = estado["filtro"].strip()
        if filtro_raw:
            filtrar_escolas()
        else:
            estado["escolas_filtradas"] = escolas

        estado["total"] = len(estado["escolas_filtradas"])
        inicio = estado["pagina"] * PAGE_SIZE
        fim = inicio + PAGE_SIZE
        pagina = estado["escolas_filtradas"][inicio:fim]

        # Renderiza apenas os cards visíveis
        for e in pagina:
            lista.controls.append(criar_card_escola(e, page))

        # Atualiza info de resultados
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} escolas"

        # Atualiza o indicador de página
        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE
        if total_paginas == 0:
            total_paginas = 1

        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"

        # Atualiza o valor do campo de entrada (sem disparar on_change)
        campo_pagina.value = str(estado['pagina'] + 1)

        # Atualiza botões (apenas para estado visual; a navegação real é igual ao footer dos alunos)
        btn_anterior.disabled = (estado["pagina"] == 0)
        btn_seguinte.disabled = (estado["pagina"] + 1) >= total_paginas

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

    def on_search(e):
        estado["filtro"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()

    def ir_para_pagina(e):
        """Função para ir para uma página específica"""
        try:
            nova_pagina = int(campo_pagina.value) - 1  # índice 0-based
            total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE

            if 0 <= nova_pagina < total_paginas:
                estado["pagina"] = nova_pagina
                carregar_pagina()
            else:
                # Página inválida, restaurar valor atual
                campo_pagina.value = str(estado['pagina'] + 1)
                page.update()
        except ValueError:
            # Valor inválido, restaurar valor atual
            campo_pagina.value = str(estado['pagina'] + 1)
            page.update()

    def on_enter_pagina(e):
        """Quando pressionar Enter no campo de página"""
        ir_para_pagina(e)

    # ======================
    #  HEADER
    # ======================

    info_resultados = ft.Text(
        f"A mostrar {min(PAGE_SIZE, len(escolas))} de {len(escolas)} escolas",
        size=13,
        color=cor_texto_medio,
    )

    header = ft.Container(
        content=ft.Column(
            [
                # Título e contador
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL, size=28, color=ft.Colors.WHITE),
                            width=48,
                            height=48,
                            bgcolor="#10B981",
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
                                    "Lista de Escolas",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão de escolas registadas",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                str(len(escolas)),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#10B981",
                            ),
                            bgcolor=ft.Colors.with_opacity(0.15, "#10B981"),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),

                ft.Container(height=15),

                # Barra de pesquisa
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
                                hint_text="Pesquisar escolas por nome...",
                                on_change=on_search,
                                border_radius=12,
                                filled=True,
                                bgcolor=cor_borda,
                                border_color=cor_borda,
                                focused_border_color="#10B981",
                                hint_style=ft.TextStyle(color=cor_texto_medio),
                                text_size=14,
                                content_padding=ft.padding.symmetric(horizontal=18, vertical=12),
                                width=420,
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

    # Criar o indicador de página
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
        focused_border_color=cor_primaria,
        on_submit=on_enter_pagina,  # Quando pressionar Enter
    )

    # Botões (usados também para controlar disabled, como no código original)
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
            bgcolor="#10B981",
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
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                            border_radius=20,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.2, cor_primaria)),
                        ),
                        ft.Container(width=10),
                        ft.Text("Ir para:", size=14, color=cor_texto_medio),
                        ft.Container(width=5),
                        campo_pagina,
                        ft.Container(width=5),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=cor_primaria,
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
