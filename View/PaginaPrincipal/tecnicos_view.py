import flet as ft
from .estilos import *


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


def criar_tecnicos_view(tecnicos):
    # Container raiz a ocupar o espaço disponível
    if tecnicos:
        return ft.Container(
            content=ft.ListView(
                controls=[criar_card_tecnico(t) for t in tecnicos],
                spacing=12,
                padding=0,
                expand=True,          # ocupa o máximo de altura
                auto_scroll=False,    # scroll manual para baixo
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
