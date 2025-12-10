import flet as ft

def PainelAdmin(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Administrador"

    # === CORES ===
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
    cor_texto_medio = "#334155"
    cor_texto_claro = "#64748B"

    # === CABEÇALHO ===
    cabecalho = ft.Container(
        padding=ft.padding.symmetric(horizontal=30, vertical=18),
        bgcolor=cor_primaria,
        shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.WHITE, size=32),
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                            padding=10,
                            border_radius=12,
                        ),
                        ft.Column(
                            [
                                ft.Text("GAIE", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text(
                                    "Gestão Integrada de Alunos e Educação",
                                    size=12,
                                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(tecnico_nome, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                                    ft.Text(
                                        "Administrador",
                                        size=11,
                                        color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
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
                                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#DC2626"),
                                                ft.Text(
                                                    "Terminar Sessão",
                                                    size=14,
                                                    color="#DC2626",
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/login"),
                                    ),
                                ],
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    border_radius=30,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                ),
            ]
        ),
    )

    # === PAINEL ADMIN ===
    painel_admin = ft.Container(
        bgcolor=cor_card,
        padding=40,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.09, ft.Colors.BLACK)
        ),
        content=ft.Column(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: page.go("/TelaPrincipalAdmin"),
                    icon_color=cor_primaria
                ),
                
                ft.Text("Painel do Administrador", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                ft.Text("Ferramentas exclusivas para gestão do sistema", size=14, color=cor_texto_claro),
                ft.Container(height=30),

                # === Botão Criar Técnico ===
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_ADD, size=22),
                            ft.Text("Criar Técnico", size=16, weight=ft.FontWeight.W_600),
                        ],
                        spacing=10,
                    ),
                    bgcolor=cor_primaria,
                    color=ft.Colors.WHITE,
                    height=50,
                    width=220,
                    on_click=lambda e: page.go("/criar-tecnico"),
                ),

                # === Botão para entrar no Painel Geral do Admin ===
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=22),
                            ft.Text("Painel Geral do Admin", size=16, weight=ft.FontWeight.W_600),
                        ],
                        spacing=10,
                    ),
                    bgcolor=cor_primaria,
                    color=ft.Colors.WHITE,
                    height=50,
                    width=250,
                    on_click=lambda e: page.go("/TelaPrincipalAdmin"),
                ),
            ],
            spacing=20,
        ),
    )

    layout = ft.Column(
        [
            ft.Container(height=20),
            painel_admin,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.View(
        route="/painel-admin",
        controls=[cabecalho, ft.Container(content=layout, padding=30, bgcolor=cor_fundo, expand=True)],
        bgcolor=cor_fundo,
    )
