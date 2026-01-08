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

def card_escola_simples(e, page):
    """Card moderno e leve para escolas"""
    return ft.Container(
        content=ft.Row(
            [
                # Avatar escola
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=24),
                    width=50,
                    height=50,
                    bgcolor="#10B981",
                    border_radius=25,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4),
                    ),
                ),
                # Nome da escola
                ft.Column(
                    [
                        ft.Text(
                            e.get("NomeEscola", "Sem nome"),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            f"ID: {e.get('idEscola', 'N/A')}",
                            size=12,
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                    color=ft.Colors.GREY_400,
                    size=18,
                ),
            ],
            spacing=15,
        ),
        bgcolor=cor_card,
        padding=16,
        border_radius=12,
        on_click=lambda e, esc=e: (
          page.session.set("escola_detalhes_id", e["idEscola"]),
          page.go("/maisDetalhesEscolas")
         ),
        shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.10, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def card_escola_completo(e):
    """Detalhes completos da escola em card expandido"""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=48),
                    width=80,
                    height=80,
                    bgcolor="#10B981",
                    border_radius=40,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=10),
                ft.Text(
                    e.get("NomeEscola", ""),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    f"ID Escola: {e.get('idEscola', 'N/A')}",
                    size=14,
                    color=cor_texto_medio,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=25, color=cor_borda),
                ft.Row(
                    [
                        estilo_botao_acao(
                            "Editar Escola",
                            ft.Icons.EDIT_ROUNDED,
                            lambda ev, d=e: (
                                ft.page.session.set("escola_editar_id", d.get("idEscola")),
                                ft.page.go("/EditarEscola"),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=400,
        bgcolor=cor_card,
        border_radius=16,
        padding=25,
    )


# ======================
# VIEW PRINCIPAL
# ======================

def criar_escolas_view(escolas, page):
    estado = {"pagina": 0, "total": len(escolas), "filtro": ""}
    lista = ft.ListView(expand=True, spacing=12, padding=10)

    def abrir_detalhe(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            content=card_escola_completo(e),
            actions=[ft.TextButton("Fechar", on_click=lambda ev: fechar_dialog())],
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        page.dialog.open = True
        page.update()

    def fechar_dialog():
        page.dialog.open = False
        page.update()

    def carregar_pagina():
        lista.controls.clear()
        filtro = estado["filtro"].strip().lower()
        filtradas = [
            esc
            for esc in escolas
            if filtro in esc.get("NomeEscola", "").lower()
            or filtro in str(esc.get("idEscola", ""))
        ] if filtro else escolas

        estado["total"] = len(filtradas)
        inicio, fim = estado["pagina"] * PAGE_SIZE, (estado["pagina"] + 1) * PAGE_SIZE
        pagina = filtradas[inicio:fim]

        for e in pagina:
            lista.controls.append(card_escola_simples(e, abrir_detalhe) if CARD_SIMPLES else card_escola_completo(e))

        total_paginas = max(1, (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE)
        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
        campo_pagina.value = str(estado['pagina'] + 1)
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} escolas"
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
        f"A mostrar {min(PAGE_SIZE, len(escolas))} de {len(escolas)} escolas",
        size=13,
        color=cor_texto_medio,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL, size=28, color=ft.Colors.WHITE),
                            width=48,
                            height=48,
                            bgcolor="#10B981",
                            border_radius=12,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text("Lista de Escolas", size=26, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Text("Gestão simples das escolas", size=12, color=cor_texto_medio),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        estilo_botao_acao(
                            "Adicionar Escola",
                            ft.Icons.ADD_CIRCLE_ROUNDED,
                            lambda ev: page.go("/criar-escola"),
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=15),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SEARCH, size=20, color=cor_texto_medio),
                        ft.Container(
                            content=ft.TextField(
                                hint_text="Pesquisar por nome ou ID da escola...",
                                on_change=on_search,
                                border_radius=12,
                                bgcolor=cor_borda,
                                focused_border_color="#10B981",
                                text_size=14,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=10,
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
                            bgcolor="#10B981",
                            on_click=ir_para_pagina,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton("Seguinte →", on_click=prox_page, style=ft.ButtonStyle(bgcolor="#10B981")),
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
