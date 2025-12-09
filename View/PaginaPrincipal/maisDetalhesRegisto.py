# Views/PaginaDetalhes/mais_detalhes_registos_view.py

import flet as ft
from .estilos import *

def MaisDetalhesRegistos(page: ft.Page, registo):
    """
    Página para mostrar detalhes de um registo em modo leitura.
    """
    cor_fundo = "#0F0F0F"
    cor_card = "#121212"
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#9CA3AF"
    cor_borda = "#242424"
    cor_primaria = "#8B5CF6"
    cor_editar = "#F59E0B"  # Amarelo para botão de editar

    # Cabeçalho
    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=cor_primaria, size=32),
                        ft.Text("Sistema SPO", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ],
                    spacing=12,
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=cor_primaria,
                    icon_size=24,
                    tooltip="Voltar",
                    on_click=lambda e: page.go("/pagina-principal")
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
    )

    # Informações do registo
    detalhes_registo = ft.Column(
        [
            ft.Text(f"Registo #{registo.get('nPIA', 'N/A')}", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Container(height=10),
            ft.Row([
                ft.Icon(ft.Icons.PERSON, size=16, color=cor_texto_medio),
                ft.Text(f"Aluno: {registo.get('NomeAluno', 'N/A')}", size=15, color=cor_texto_medio),
            ]),
            ft.Row([
                ft.Icon(ft.Icons.FLAG, size=16, color=cor_texto_medio),
                ft.Text(f"Estado: {registo.get('Estado', 'N/A')}", size=15, color=cor_texto_medio),
            ]),
            ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=cor_texto_medio),
                ft.Text(f"Data de Entrada: {registo.get('DataEntradaSPO', 'N/A')}", size=15, color=cor_texto_medio),
            ]),
            ft.Row([
                ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=cor_texto_medio),
                ft.Text(f"Técnico: {registo.get('NomeTecnico', 'N/A')}", size=15, color=cor_texto_medio),
            ]),
            ft.Container(height=10),
            ft.Text("Descrição:", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Text(registo.get('Observacoes', 'N/A'), size=15, color=cor_texto_medio),
            ft.Container(height=10),
            ft.Text("Problemática:", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Text(registo.get('tipoProblematica', 'N/A'), size=15, color=cor_texto_medio),
        ],
        spacing=8
    )

    # Botão Editar
    btn_editar = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.EDIT_ROUNDED,
            icon_color="#FFFFFF",
            bgcolor=cor_editar,
            tooltip="Editar registo",
            icon_size=20,
            on_click=lambda e: (
                page.session.set("registo_editar_id", registo["nPIA"]),
                page.go("/EditarRegisto")
            )
        ),
        alignment=ft.alignment.center_right
    )

    formulario = ft.Container(
        content=ft.Column(
            [
                detalhes_registo,
                btn_editar
            ],
            spacing=20,
        ),
        bgcolor=cor_card,
        padding=25,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        width=800,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.1, cor_primaria),
        )
    )

    return ft.View(
        route="/MaisDetalhesRegistos",
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(content=formulario, alignment=ft.alignment.center),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        bgcolor=cor_fundo,
        padding=20,
    )
