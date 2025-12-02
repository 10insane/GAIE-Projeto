# Views/PaginaPrincipal/util_buttons.py

import flet as ft
from .estilosAdmin import cor_primaria

def estilo_botao_acao(texto, icone, onclick):
    return ft.ElevatedButton(
        width=240,
        content=ft.Row(
            [
                ft.Icon(icone, size=20, color=ft.Colors.WHITE),
                ft.Text(texto, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=60),
            padding=ft.padding.symmetric(horizontal=22, vertical=12),
            bgcolor=cor_primaria,
            elevation=3,
        ),
        on_click=onclick,
    )
