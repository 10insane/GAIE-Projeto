import flet as ft
from .estilosAdmin import *
from .util_buttons import estilo_botao_acao


def criar_card_tecnico(tecnico):
    nome = tecnico.get("NomeTecnico", tecnico.get("nomeTecnico", ""))
    funcao = tecnico.get("Funcao", "")

    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.PERSON,
                        color=cor_primaria,
                        size=30,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.12, cor_primaria),
                    padding=12,
                    border_radius=10,
                ),
                ft.Column(
                    [
                        ft.Text(
                            nome,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            funcao,
                            size=13,
                            color=cor_texto_medio,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        bgcolor=cor_card,
        padding=16,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
        ),
    )


def criar_tecnicos_view(tecnicos, page):
    # Container raiz a ocupar o espaço disponível
    if tecnicos:
        # HEADER
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.ENGINEERING, size=28, color=ft.Colors.WHITE),
                                width=48,
                                height=48,
                                bgcolor=cor_primaria,
                                border_radius=12,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text("Lista de Técnicos", size=26, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ft.Text("Gestão dos técnicos do sistema", size=12, color=cor_texto_medio),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            # Botão para criar técnico
                            estilo_botao_acao(
                                "Criar Técnico",
                                ft.Icons.PERSON_ADD,
                                lambda e: page.go("/criar-tecnico"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=12,
                    ),
                ],
                spacing=0,
            ),
            padding=20,
            bgcolor=cor_card,
            border_radius=12,
        )

        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Container(height=15),
                    ft.ListView(
                        controls=[criar_card_tecnico(t) for t in tecnicos],
                        spacing=12,
                        padding=0,
                        expand=True,          # ocupa o máximo de altura
                        auto_scroll=False,    # scroll manual para baixo
                    ),
                ],
                expand=True,
                spacing=0,
            ),
            expand=True,
            padding=ft.padding.only(top=8, left=12, right=12, bottom=12),
            alignment=ft.alignment.top_center,  # “puxa” a lista para cima
        )

    # Nenhum técnico registado
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.ENGINEERING_OUTLINED,
                    size=90,
                    color=cor_texto_medio,
                ),
                ft.Text(
                    "Nenhum técnico registado",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                ),
                ft.Text(
                    "A lista de técnicos está vazia.",
                    size=13,
                    color=cor_texto_medio,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
