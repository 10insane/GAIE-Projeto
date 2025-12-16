import flet as ft
from Models.AlunosModel import buscarAlunoPorProcesso


def DetalhesAluno(page: ft.Page):

    aluno_id = page.session.get("aluno_detalhes_id")

    if not aluno_id:
        return ft.View(controls=[ft.Text("Nenhum aluno selecionado.")])

    aluno = buscarAlunoPorProcesso(aluno_id)

    if not aluno:
        return ft.View(controls=[ft.Text(f"Aluno {aluno_id} não encontrado.")])

    # ===== CORES =====
    cor_fundo = "#0F0F0F"
    cor_card = "#1A1A1A"
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#A0A0A0"
    cor_borda = "#2A2A2A"
    cor_primaria = "#8B5CF6"
    cor_voltar = "#F50B0B"

    # ===== HEADER =====
    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=cor_primaria, size=34),
                        ft.Column(
                            [
                                ft.Text(
                                    "Sistema SPO",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Detalhes do Aluno",
                                    size=12,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=cor_primaria,
                    tooltip="Voltar",
                    on_click=lambda e: page.go("/pagina-principal"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=14,
        border=ft.border.all(1, cor_borda),
    )

    # ===== FUNÇÃO INFO =====
    def info_item(icon, label, value):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=cor_primaria),
                    ft.Column(
                        [
                            ft.Text(label, size=12, color=cor_texto_medio),
                            ft.Text(value, size=15, color=cor_texto_claro, weight=ft.FontWeight.W_500),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=10,
            ),
            padding=10,
            border_radius=10,
            bgcolor="#141414",
        )

    # ===== TOPO DO CARD =====
    topo_aluno = ft.Column(
        [
            ft.Text(
                aluno.get("NomeAluno", "N/A"),
                size=26,
                weight=ft.FontWeight.BOLD,
                color=cor_texto_claro,
            ),
            ft.Text(
                f"Processo nº {aluno.get('nProcessoAluno', 'N/A')}",
                size=14,
                color=cor_texto_medio,
            ),
        ],
        spacing=4,
    )

    # ===== GRID DE INFORMAÇÕES =====
    infos = ft.ResponsiveRow(
        [
            info_item(ft.Icons.CALENDAR_TODAY, "Ano", f"{aluno.get('Ano', 'N/A')}º"),
            info_item(ft.Icons.GROUP_ROUNDED, "Turma", aluno.get("Turma", "N/A")),
            info_item(ft.Icons.SCHOOL, "Escola", aluno.get("NomeEscola", "N/A")),
        ],
        columns=12,
        spacing=12,
        run_spacing=12,
    )

    # ===== BOTÃO =====
    btn_voltar = ft.ElevatedButton(
        text="Voltar",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=cor_voltar,
        color="#FFFFFF",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=lambda e: page.go("/pagina-principal"),
    )

    # ===== CARD PRINCIPAL =====
    card = ft.Container(
        content=ft.Column(
            [
                topo_aluno,
                ft.Divider(color=cor_borda),
                infos,
                ft.Container(height=10),
                ft.Row(
                    [btn_voltar],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=20,
        ),
        width=760,
        padding=30,
        bgcolor=cor_card,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.2, cor_primaria),
        ),
    )

    # ===== VIEW FINAL =====
    return ft.View(
        bgcolor=cor_fundo,
        padding=20,
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(
                        content=card,
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )
