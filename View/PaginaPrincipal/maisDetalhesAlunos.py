import flet as ft
from Models.AlunosModel import buscarAlunoPorProcesso


def DetalhesAluno(page: ft.Page):
    """
    Página de detalhes do aluno com design moderno
    """

    # ===== Buscar aluno pelo ID salvo na sessão =====
    aluno_id = page.session.get("aluno_detalhes_id")

    if not aluno_id:
        return ft.View(
            controls=[ft.Text("Nenhum aluno selecionado.")]
        )

    aluno = buscarAlunoPorProcesso(aluno_id)

    if not aluno:
        return ft.View(
            controls=[ft.Text(f"Aluno {aluno_id} não encontrado.")]
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
                        ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=cor_primaria, size=32),
                        ft.Text(
                            "Sistema SPO",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                    ],
                    spacing=12,
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=cor_primaria,
                    icon_size=24,
                    tooltip="Voltar",
                    on_click=lambda e: page.go("/pagina-alunos"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
    )

    # ===== Função auxiliar =====
    def linha_info(icone, label, valor):
        return ft.Row(
            [
                ft.Icon(icone, size=18, color=cor_texto_medio),
                ft.Text(
                    f"{label}: {valor}",
                    size=15,
                    color=cor_texto_medio,
                ),
            ],
            spacing=8,
        )

    # ===== Detalhes do aluno =====
    detalhes_aluno = ft.Column(
        [
            ft.Text(
                aluno.get("NomeAluno", "N/A"),
                size=22,
                weight=ft.FontWeight.BOLD,
                color=cor_texto_claro,
            ),

            ft.Container(height=15),

            linha_info(ft.Icons.BADGE_ROUNDED, "Nº Processo", aluno.get("nProcessoAluno", "N/A")),
            linha_info(ft.Icons.CALENDAR_TODAY, "Ano", f"{aluno.get('Ano', 'N/A')}º"),
            linha_info(ft.Icons.GROUP_ROUNDED, "Turma", aluno.get("Turma", "N/A")),
            linha_info(ft.Icons.SCHOOL, "Escola", aluno.get("NomeEscola", "N/A")),

            ft.Container(height=15),

            ft.Text(
                "Observações",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=cor_texto_claro,
            ),
            ft.Text(
                aluno.get("Observacoes", "Sem observações."),
                size=15,
                color=cor_texto_medio,
            ),
        ],
        spacing=10,
    )

    # ===== Botões =====
    btn_editar = ft.ElevatedButton(
        text="Editar Aluno",
        bgcolor=cor_editar,
        color="#FFFFFF",
        icon=ft.Icons.EDIT,
        on_click=lambda e: (
            page.session.set("aluno_editar_id", aluno["nProcessoAluno"]),
            page.go("/EditarAluno"),
        ),
    )

    btn_voltar = ft.ElevatedButton(
        text="Voltar",
        bgcolor=cor_voltar,
        color="#FFFFFF",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: page.go("/pagina-alunos"),
    )

    # ===== Card principal =====
    formulario = ft.Container(
        content=ft.Column(
            [
                detalhes_aluno,
                ft.Row(
                    [btn_voltar, btn_editar],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=20,
        ),
        bgcolor=cor_card,
        padding=25,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        width=750,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.15, cor_primaria),
        ),
    )

    # ===== View final =====
    return ft.View(
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(
                        content=formulario,
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        bgcolor=cor_fundo,
        padding=20,
    )
