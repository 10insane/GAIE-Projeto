# Views/PaginaPrincipal/alunos_view.py

import flet as ft
from .estilos import *
from .util_buttons import estilo_botao_acao

def criar_card_aluno(aluno, page):
    """Card de aluno com design moderno e clean"""
    return ft.Container(
        content=ft.Row(
            [
                # Ícone do aluno
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color="#FFFFFF", size=24),
                    bgcolor=cor_primaria,
                    padding=10,
                    border_radius=12,
                ),

                # Informações do aluno
                ft.Column(
                    [
                        # Nome
                        ft.Text(
                            aluno.get("NomeAluno", ""), 
                            size=15, 
                            weight=ft.FontWeight.BOLD, 
                            color=cor_texto_claro,
                        ),
                        
                        ft.Container(height=2),
                        
                        # Detalhes em linha
                        ft.Row(
                            [
                                # Escola
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.SCHOOL, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                aluno.get("NomeEscola", "N/A"),
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

                                # Ano e Turma
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.MEETING_ROOM, size=13, color=cor_texto_medio),
                                            ft.Text(
                                                f"{aluno.get('Ano', 'N/A')}º - Turma {aluno.get('Turma', 'N/A')}",
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
                    ],
                    spacing=0,
                    expand=True,
                ),

                # Botão de editar
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_color="#FFFFFF",
                        bgcolor="#F59E0B",
                        tooltip="Editar aluno",
                        icon_size=18,
                        on_click=lambda e, a=aluno: (
                            page.session.set("aluno_editar_id", a["nProcessoAluno"]),
                            page.go("/EditarAluno")
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
        border=ft.border.all(2, ft.Colors.with_opacity(0.15, cor_primaria)),
        shadow=ft.BoxShadow(
            blur_radius=20, 
            spread_radius=1,
            color=ft.Colors.with_opacity(0.12, cor_primaria),
            offset=ft.Offset(0, 4),
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def criar_alunos_view(alunos, page):
    """View principal da lista de alunos"""

    if alunos:
        return ft.Column(
            [
                # Cabeçalho fixo
                ft.Container(
                    content=ft.Row(
                        [
                            # Título e contador
                            ft.Column(
                                [
                                    ft.Text(
                                        "Lista de Alunos", 
                                        size=26, 
                                        weight=ft.FontWeight.BOLD, 
                                        color=cor_texto_claro,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Text(
                                                    f"{len(alunos)}",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=cor_primaria,
                                                ),
                                                bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                                border_radius=8,
                                            ),
                                            ft.Text(
                                                "alunos registados",
                                                size=13, 
                                                color=cor_texto_medio,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                ],
                                spacing=8,
                            ),

                            ft.Container(expand=True),

                            # Botão adicionar
                            estilo_botao_acao(
                                "Adicionar Aluno", 
                                ft.Icons.ADD_CIRCLE_ROUNDED,
                                lambda e: page.go("/CriarAluno")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),

                # Divider
                ft.Divider(height=1, color=cor_borda),
                
                ft.Container(height=16),

                # Lista de alunos com scroll
                ft.Container(
                    content=ft.Column(
                        [criar_card_aluno(a, page) for a in alunos],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    # ——— Estado vazio ———
    return ft.Container(
        content=ft.Column(
            [
                # Ícone grande
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.PEOPLE_OUTLINED, 
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
                    "Nenhum aluno encontrado", 
                    size=22, 
                    weight=ft.FontWeight.BOLD, 
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                # Subtexto
                ft.Text(
                    "Comece por adicionar o primeiro registo ao sistema",
                    size=14, 
                    color=cor_texto_medio,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(height=20),
                
                # Botão
                estilo_botao_acao(
                    "Adicionar Primeiro Aluno", 
                    ft.Icons.ADD_CIRCLE_ROUNDED,
                    lambda e: page.go("/CriarAluno")
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=40,
    )