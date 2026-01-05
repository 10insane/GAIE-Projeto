import flet as ft
from .estilos import *

def PerfilTecnico(tecnico):
    nome = tecnico.get("NomeTecnico", "")
    nproc = tecnico.get("nProcTecnico", "")

    return ft.Container(
        content=ft.Column(
            [
                # Avatar com gradiente e anel
                ft.Stack(
                    [
                        # Anel decorativo externo
                        ft.Container(
                            width=130,
                            height=130,
                            border_radius=65,
                            border=ft.border.all(3, cor_primaria),
                            bgcolor=ft.Colors.TRANSPARENT,
                        ),
                        # Avatar principal
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.PERSON,
                                size=70,
                                color=ft.Colors.WHITE,
                            ),
                            width=120,
                            height=120,
                            alignment=ft.alignment.center,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[cor_primaria, ft.Colors.with_opacity(0.8, cor_primaria)],
                            ),
                            border_radius=60,
                            shadow=ft.BoxShadow(
                                blur_radius=20,
                                spread_radius=2,
                                color=ft.Colors.with_opacity(0.3, cor_primaria),
                                offset=ft.Offset(0, 4),
                            ),
                        ),
                    ],
                    width=130,
                    height=130,
                ),

                ft.Container(height=8),

                # Nome do técnico
                ft.Text(
                    nome,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto_claro,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                # Badge com número de processo
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.BADGE_OUTLINED,
                                size=18,
                                color=cor_primaria,
                            ),
                            ft.Text(
                                nproc,
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=cor_primaria,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, cor_primaria)),
                ),

                ft.Container(height=8),

                # Linha decorativa
                ft.Container(
                    width=60,
                    height=3,
                    bgcolor=cor_primaria,
                    border_radius=2,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        padding=32,
        border_radius=20,
        bgcolor=cor_card,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=24,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 8),
        ),
        width=400,
        animate=300,  # Sintaxe correta para animação no Flet
    )