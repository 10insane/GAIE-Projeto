import flet as ft
from Models.RegistoModel import buscarRegistoPorId

def MaisDetalhesRegistos(page: ft.Page):
    
    registo_id = page.session.get("registo_detalhes_id")
    if not registo_id:
        return ft.View(
            route="/MaisDetalhesRegistos",
            controls=[ft.Text("Nenhum registo selecionado.")],
        )

    registo = buscarRegistoPorId(registo_id)
    if not registo:
        return ft.View(
            route="/MaisDetalhesRegistos",
            controls=[ft.Text(f"Registo {registo_id} não encontrado.")],
        )

    # ===== Cores =====
    cor_fundo = "#0F172A"
    cor_card = "#1E293B"
    cor_card_destaque = "#2D3B4F"
    cor_texto_claro = "#F1F5F9"
    cor_texto_medio = "#94A3B8"
    cor_borda = "#334155"
    cor_primaria = "#3B82F6"
    cor_editar = "#F59E0B"
    cor_voltar = "#EF4444"
    cor_acento = "#10B981"

    # ===== Cabeçalho Melhorado =====
    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.ARTICLE_ROUNDED, color=cor_primaria, size=28),
                            bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                            padding=10,
                            border_radius=10
                        ),
                        ft.Column(
                            [
                                ft.Text("Sistema SPO", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Text("Detalhes do Registo", size=13, color=cor_texto_medio)
                            ],
                            spacing=2
                        )
                    ],
                    spacing=15
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_color=cor_texto_claro,
                        icon_size=20,
                        tooltip="Voltar",
                        on_click=lambda e: page.go("/pagina-principal"),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, cor_primaria)}
                        )
                    ),
                    bgcolor=ft.Colors.with_opacity(0.05, cor_primaria),
                    border_radius=8
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.1, "#000000")
        )
    )

    # ===== Card de Informação =====
    def criar_info_card(icone, label, valor, cor_icone=cor_primaria):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icone, size=20, color=cor_icone),
                        bgcolor=ft.Colors.with_opacity(0.1, cor_icone),
                        padding=8,
                        border_radius=8
                    ),
                    ft.Column(
                        [
                            ft.Text(label, size=12, color=cor_texto_medio, weight=ft.FontWeight.W_500),
                            ft.Text(str(valor), size=15, color=cor_texto_claro, weight=ft.FontWeight.W_600)
                        ],
                        spacing=2,
                        expand=True
                    )
                ],
                spacing=12
            ),
            bgcolor=cor_card_destaque,
            padding=15,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            expand=True
        )

    # ===== Badge de Estado =====
    estado = registo.get("Estado", "N/A")
    cor_badge = cor_acento if estado.lower() in ["ativo", "em curso"] else cor_editar
    
    badge_estado = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CIRCLE, size=8, color=cor_badge),
                ft.Text(estado, size=13, color=cor_texto_claro, weight=ft.FontWeight.W_600)
            ],
            spacing=6
        ),
        bgcolor=ft.Colors.with_opacity(0.15, cor_badge),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, cor_badge))
    )

    # ===== Header do Registo =====
    header_registo = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            f"Registo #{registo.get('nPIA', 'N/A')}", 
                            size=28, 
                            weight=ft.FontWeight.BOLD, 
                            color=cor_texto_claro
                        ),
                        badge_estado
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=cor_borda)
            ],
            spacing=15
        ),
        padding=ft.padding.only(bottom=10)
    )

    # ===== Grid de Informações Principais =====
    info_grid = ft.Column(
        [
            ft.Row(
                [
                    criar_info_card(ft.Icons.PERSON_ROUNDED, "Aluno", registo.get("NomeAluno", "N/A"), cor_primaria),
                    criar_info_card(ft.Icons.CALENDAR_TODAY_ROUNDED, "Data Entrada", registo.get("DataEntradaSPO", "N/A"), cor_acento)
                ],
                spacing=15
            ),
            criar_info_card(ft.Icons.PERSON_OUTLINE_ROUNDED, "Técnico Responsável", registo.get("NomeTecnico", "N/A"), cor_editar)
        ],
        spacing=15
    )

    # ===== Seção de Descrição =====
    secao_descricao = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, size=18, color=cor_primaria),
                        ft.Text("Descrição", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro)
                    ],
                    spacing=8
                ),
                ft.Container(
                    content=ft.Text(
                        registo.get("Observacoes", "Sem descrição disponível"), 
                        size=14, 
                        color=cor_texto_medio,
                        weight=ft.FontWeight.W_400
                    ),
                    padding=15,
                    bgcolor=cor_card_destaque,
                    border_radius=10,
                    border=ft.border.all(1, cor_borda)
                )
            ],
            spacing=10
        )
    )

    # ===== Seção de Problemática =====
    secao_problematica = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=18, color=cor_editar),
                        ft.Text("Problemática", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro)
                    ],
                    spacing=8
                ),
                ft.Container(
                    content=ft.Text(
                        registo.get("tipoProblematica", "Não especificado"), 
                        size=14, 
                        color=cor_texto_medio,
                        weight=ft.FontWeight.W_400
                    ),
                    padding=15,
                    bgcolor=cor_card_destaque,
                    border_radius=10,
                    border=ft.border.all(1, cor_borda)
                )
            ],
            spacing=10
        )
    )

    # ===== Botões Modernos =====
    btn_voltar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=18),
                ft.Text("Voltar", size=14, weight=ft.FontWeight.W_600)
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=cor_voltar,
        color="#FFFFFF",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=2,
            shadow_color=ft.Colors.with_opacity(0.3, cor_voltar)
        ),
        on_click=lambda e: page.go("/pagina-principal")
    )

    btn_editar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.EDIT_ROUNDED, size=18),
                ft.Text("Editar Registo", size=14, weight=ft.FontWeight.W_600)
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=cor_editar,
        color="#FFFFFF",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=2,
            shadow_color=ft.Colors.with_opacity(0.3, cor_editar)
        ),
        on_click=lambda e: (
            page.session.set("registo_editar_id", registo["nPIA"]),
            page.go("/EditarRegisto")
        )
    )

    # ===== Container Principal =====
    formulario = ft.Container(
        content=ft.Column(
            [
                header_registo,
                info_grid,
                secao_descricao,
                secao_problematica,
                ft.Container(height=10),
                ft.Row(
                    [btn_voltar, btn_editar], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=15
                )
            ],
            spacing=20
        ),
        bgcolor=cor_card,
        padding=30,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        width=850,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.2, cor_primaria),
            offset=ft.Offset(0, 4)
        )
    )

    # ===== View Final =====
    return ft.View(
        route="/MaisDetalhesRegistos",
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(height=20),
                    formulario
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        bgcolor=cor_fundo,
        padding=30,
        scroll=ft.ScrollMode.AUTO
    )