import flet as ft
from .estilos import *
import os

TOKEN_FILE = "token.json"  

def logout(page: ft.Page):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

    page.session.clear()
    page.views.clear()

    from View.Login.Login import LoginView 
    page.views.append(LoginView(page))

    page.go("/login")
    page.update()


def criar_cabecalho(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=28, vertical=16),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[cor_primaria, cor_secundaria],
        ),
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
        ),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.WHITE, size=30),
                            bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
                            padding=10,
                            border_radius=15,
                        ),
                        ft.Column(
                            [
                                ft.Text("GAIE", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text(
                                    "Gestão Integrada de Alunos e Educação",
                                    size=12,
                                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(tecnico_nome, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                                    ft.Text(
                                        "Técnico Responsável",
                                        size=11,
                                        color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                    ),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            ft.PopupMenuButton(
                                icon=ft.Icons.ACCOUNT_CIRCLE,
                                icon_color=ft.Colors.WHITE,
                                icon_size=36,
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.PERSON_ROUNDED, size=20, color=ft.Colors.WHITE),
                                                ft.Text("Meu Perfil", size=14, color=ft.Colors.WHITE),
                                            ],
                                            spacing=12,
                                        ),
                                       on_click=lambda e: (
                                         page.session.set("tecnico", {
                                        "NomeTecnico": page.session.get("tecnico_nome"),
                                        "nProcTecnico": page.session.get("nProcTecnico"),
                                      }),
                                        page.go("/TecnicoPerfil")
                                      )
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.SETTINGS_ROUNDED, size=20, color=ft.Colors.WHITE),
                                                ft.Text("Configurações", size=14, color=ft.Colors.WHITE),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/Config"),
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#FF6B6B"),
                                                ft.Text("Terminar Sessão", size=14, color="#FF6B6B", weight=ft.FontWeight.W_600),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: logout(page),  # <- chama logout corretamente
                                    ),
                                ],
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=25,
                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                ),
            ]
        ),
    )
