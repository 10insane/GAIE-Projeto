import flet as ft
from .estilos import *
import re
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
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4),
                    ),
                    alignment=ft.alignment.center,
                ),
                # Info do aluno
                ft.Column(
                    [
                        ft.Text(
                                    a.get("NomeAluno", ""),
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=cor_texto_claro,
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
                                    bgcolor=cor_primaria,
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
        bgcolor=cor_card,
        border=None,
        on_click=lambda e: abrir_detalhe(a),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=14,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
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
                    color=cor_texto_claro,
                ),
                # Escola
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, size=16, color=ft.Colors.GREY_600),
                        ft.Text(
                            a.get("NomeEscola", ""),
                            size=14,
                            color=cor_texto_medio,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Divider(height=20, color=cor_borda),
                # Info detalhada
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Ano", size=11, color=cor_texto_medio),
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
 
        filtro_raw = estado["filtro"].strip()
       
        if filtro_raw:
            alunos_filtrados = []
            filtro_lower = filtro_raw.lower()
           
            for a in alunos:
                # Verifica pelo nome (case-insensitive)
                nome = a.get("NomeAluno", "").lower()
               
                # Verifica pelo número do processo
                nproc = str(a.get("nProcessoAluno", ""))
               
                # Verifica se o filtro corresponde ao nome OU ao número do processo
                if filtro_lower in nome or filtro_raw in nproc:
                    alunos_filtrados.append(a)
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
 
        # Atualiza o indicador de página
        total_paginas = (estado["total"] + PAGE_SIZE - 1) // PAGE_SIZE  # Arredonda para cima
        if total_paginas == 0:
            total_paginas = 1
       
        # Atualiza o texto do indicador
        indicador_pagina_text.value = f"Página {estado['pagina'] + 1} de {total_paginas}"
       
        # Atualiza o valor do campo de entrada (sem disparar on_change)
        campo_pagina.value = str(estado['pagina'] + 1)
       
        # Info de resultados
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
 
    def on_search(e):
        estado["filtro"] = e.control.value
        estado["pagina"] = 0
        carregar_pagina()
 
    def ir_para_pagina(e):
        """Função para ir para uma página específica"""
        try:
            nova_pagina = int(campo_pagina.value) - 1  # Converte para índice 0-based
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
    #  HEADER MODERNO
    # ======================
 
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
                            shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.14, ft.Colors.BLACK), offset=ft.Offset(0,4)),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Lista de Alunos",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Gestão rápida e visual dos alunos",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
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
                # Barra de pesquisa moderna com ícone integrado
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
                                hint_text="Pesquisar por nome ou número do aluno...",
                                on_change=on_search,
                                border_radius=12,
                                filled=True,
                                bgcolor=cor_borda,
                                border_color=cor_borda,
                                focused_border_color=cor_primaria,
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
    #  FOOTER MODERNO COM NAVEGAÇÃO COMPLETA
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
 
    footer = ft.Container(
        content=ft.Row(
            [
                # Botão Anterior
                ft.ElevatedButton(
                    "← Anterior",
                    on_click=prev_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_borda,
                        color=cor_texto_claro,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2,
                    ),
                    icon=ft.Icons.ARROW_BACK,
                ),
               
                ft.Container(expand=True),
               
                # Seção de navegação de página
                ft.Row(
                    [
                        # Indicador de página
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
                        # Campo para digitar a página
                        campo_pagina,
                        ft.Container(width=5),
                        # Botão para ir para a página
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
                ft.ElevatedButton(
                    "Seguinte →",
                    on_click=prox_page,
                    style=ft.ButtonStyle(
                        bgcolor=cor_primaria,
                        color=cor_texto_claro,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2,
                    ),
                    icon=ft.Icons.ARROW_FORWARD,
                ),
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
 