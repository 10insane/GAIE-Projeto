import flet as ft
from Models.RegistoModel import buscarRegistoPorId

def MaisDetalhesRegistos(page: ft.Page):
    """
    Página de detalhes de um registo com design apelativo,
    cores consistentes, e botões Editar e Voltar.
    """

    # ===== Buscar registo pelo ID salvo na sessão =====
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
    cor_fundo = "#0F0F0F"
    cor_card = "#1A1A1A"
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#A0A0A0"
    cor_borda = "#2A2A2A"
    cor_primaria = "#8B5CF6"
    cor_editar = "#F59E0B"
    cor_voltar = "#F50B0B"

    # ===== Cabeçalho =====
    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=cor_primaria, size=32),
                        ft.Text("Sistema SPO", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ],
                    spacing=12
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=cor_primaria,
                    icon_size=24,
                    tooltip="Voltar",
                    on_click=lambda e: page.go("/pagina-principal")
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
    )

    # ===== Função auxiliar para linhas de informação =====
    def linha_info(icone, label, valor):
        return ft.Row([
            ft.Icon(icone, size=18, color=cor_texto_medio),
            ft.Text(f"{label}: {valor}", size=15, color=cor_texto_medio)
        ], spacing=8)

    # ===== Detalhes do registo =====
    detalhes_registo = ft.Column(
        [
            ft.Text(f"Registo #{registo.get('nPIA', 'N/A')}", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Container(height=15),
            linha_info(ft.Icons.PERSON, "Aluno", registo.get("NomeAluno", "N/A")),
            linha_info(ft.Icons.FLAG, "Estado", registo.get("Estado", "N/A")),
            linha_info(ft.Icons.CALENDAR_TODAY, "Data de Entrada", registo.get("DataEntradaSPO", "N/A")),
            linha_info(ft.Icons.PERSON_OUTLINE, "Técnico", registo.get("NomeTecnico", "N/A")),
            ft.Container(height=15),
            ft.Text("Descrição", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Text(registo.get("Observacoes", "N/A"), size=15, color=cor_texto_medio),
            ft.Container(height=10),
            ft.Text("Problemática", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Text(registo.get("tipoProblematica", "N/A"), size=15, color=cor_texto_medio),
        ],
        spacing=10
    )

    # ===== Botões =====
    btn_editar = ft.Container(
        content=ft.ElevatedButton(
            "Editar Registo",
            bgcolor=cor_editar,
            color="#FFFFFF",
            icon=ft.Icons.EDIT,
            on_click=lambda e: (
                page.session.set("registo_editar_id", registo["nPIA"]),
                page.go("/EditarRegisto")
            )
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
    )

    btn_voltar = ft.Container(
        content=ft.ElevatedButton(
            "Voltar",
            bgcolor=cor_voltar,
            color="#FFFFFF",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: page.go("/pagina-principal")
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
    )

    # ===== Container principal do formulário =====
    formulario = ft.Container(
        content=ft.Column(
            [
                detalhes_registo,
                ft.Row([btn_voltar, btn_editar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ],
            spacing=20
        ),
        bgcolor=cor_card,
        padding=25,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        width=750,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.15, cor_primaria)
        )
    )

    # ===== View final =====
    return ft.View(
        route="/MaisDetalhesRegistos",
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(content=formulario, alignment=ft.alignment.center)
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        bgcolor=cor_fundo,
        padding=20
    )
