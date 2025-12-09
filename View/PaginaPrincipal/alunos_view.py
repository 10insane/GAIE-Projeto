import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao
 
# ======================
#  CONFIGURAÇÃO
# ======================
 
PAGE_SIZE = 50
CARD_SIMPLES = True
 
# ======================
#  CARDS
# ======================
 
def card_aluno_simples(a, abrir_detalhe):
    """Card moderno com gradiente e hover"""
    return ft.Container(
        content=ft.Row(
            [
                # Avatar colorido
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=24),
                    width=50,
                    height=50,
                    bgcolor=cor_primaria,
                    border_radius=25,
                    alignment=ft.alignment.center,
                ),
                # Info do aluno
                ft.Column(
                    [
                        ft.Text(
                            a.get("NomeAluno", ""),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_900,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        f"{a.get('Ano','?')}º ano",
                                        size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.BLUE_400,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                    border_radius=12,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"Turma {a.get('Turma','?')}",
                                        size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.PURPLE_400,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                    border_radius=12,
                                ),
                                ft.Text(
                                    f"Nº {a.get('NProcesso', 'N/A')}",
                                    size=11,
                                    color=ft.Colors.GREY_600,
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
                # Ícone de seta
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
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_200),
        on_click=lambda e: abrir_detalhe(a),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )
 
 
def card_aluno_completo(a):
    """Card de detalhes com visual aprimorado"""
    return ft.Container(
        content=ft.Column(
            [
                # Avatar grande
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=40),
                    width=80,
                    height=80,
                    bgcolor=cor_primaria,
                    border_radius=40,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.3, cor_primaria),
                        offset=ft.Offset(0, 4),
                    ),
                ),
                ft.Container(height=10),
                # Nome
                ft.Text(
                    a.get("NomeAluno", ""),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                # Escola
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, size=16, color=ft.Colors.GREY_600),
                        ft.Text(
                            a.get("NomeEscola", ""),
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Divider(height=20, color=ft.Colors.GREY_300),
                # Info detalhada
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Ano", size=11, color=ft.Colors.GREY_600),
                                    ft.Text(
                                        f"{a.get('Ano','?')}º",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_primaria,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=4,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=15,
                            border_radius=12,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Turma", size=11, color=ft.Colors.GREY_600),
                                    ft.Text(
                                        a.get("Turma", "?"),
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_primaria,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=4,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=15,
                            border_radius=12,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.BADGE, size=16, color=ft.Colors.GREY_600),
                            ft.Text(
                                f"Nº Processo: {a.get('NProcesso', 'N/A')}",
                                size=13,
                                color=ft.Colors.GREY_700,
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
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=16,
        width=400,
    )
 
 
# ======================
#  VIEW PRINCIPAL
# ======================
 
def criar_alunos_view(alunos, page):
    estado = {
        "pagina": 0,
        "total": len(alunos),
        "filtro": "",
    }
 
    lista = ft.ListView(expand=True, spacing=12, padding=10)
 
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
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        page.dialog.open = True
        page.update()
 
    def fechar_dialog():
        page.dialog.open = False
        page.update()
 
    def carregar_pagina():
        lista.controls.clear()
 
        filtro_norm = estado["filtro"].strip().lower()
        if filtro_norm:
            alunos_filtrados = [
                a for a in alunos
                if (
                    filtro_norm in a.get("NomeAluno", "").lower()
                    or filtro_norm in str(a.get("NProcesso", "")).lower()
                )
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
 
        # Info de resultados
        info_resultados.value = f"A mostrar {len(pagina)} de {estado['total']} alunos"
        page.update()
 
    def prox_page(e):
        if (estado["pagina"] + 1) * PAGE_SIZE < estado["total"]:
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
 
    # ======================
    #  HEADER MODERNO
    # ======================
 
    info_resultados = ft.Text(
        f"A mostrar {min(PAGE_SIZE, len(alunos))} de {len(alunos)} alunos",
        size=13,
        color=ft.Colors.GREY_600,
    )
 
    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.GROUPS, size=32, color=cor_primaria),
                        ft.Text(
                            "Lista de Alunos",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_900,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                str(len(alunos)),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=cor_primaria,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.15, cor_primaria),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),
                ft.Container(height=15),
                # Barra de pesquisa moderna
                ft.Container(
                    content=ft.TextField(
                        hint_text="🔍  Pesquisar por nome ou nº de processo...",
                        on_change=on_search,
                        border_radius=12,
                        filled=True,
                        bgcolor=ft.Colors.GREY_50,
                        border_color=ft.Colors.GREY_300,
                        focused_border_color=cor_primaria,
                        hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
                        text_size=14,
                        content_padding=ft.padding.symmetric(horizontal=20, vertical=15),
                    ),
                    width=500,
                ),
                ft.Container(height=5),
                info_resultados,
            ],
            spacing=0,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )
 
    # ======================
    #  FOOTER MODERNO
    # ======================
 
    footer = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    "← Anterior",
                    on_click=prev_page,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.WHITE,
                        color=cor_primaria,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2,
                    ),
                    icon=ft.Icons.ARROW_BACK,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Seguinte →",
                    on_click=prox_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_primaria,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2,
                    ),
                    icon=ft.Icons.ARROW_FORWARD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
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
                ft.Container(height=15),
                lista,
                ft.Container(height=15),
                footer,
            ],
            expand=True,
            spacing=0,
        ),
        bgcolor=ft.Colors.GREY_50,
        padding=20,
        expand=True,
    )