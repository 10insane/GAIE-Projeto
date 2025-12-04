import flet as ft
from Models.EscolasModel import *
from View.PaginaPrincipal.estilos import *
from View.PaginaPrincipal.util_buttons import estilo_botao_acao


def PaginaEditarEscola(page: ft.Page):

    # Buscar ID que veio pela sessão
    id_escola = page.session.get("escola_editar_id")

    if not id_escola:
        page.go("/TelaPrincipalAdmin")
        return

    # Buscar dados da escola
    try:
        escolas = listarEscolas()
    except:
        escolas = []

    escola = next((e for e in escolas if e["idEscola"] == id_escola), None)

    if not escola:
        page.go("/TelaPrincipalAdmin")
        return

    # Campo do formulário
    nome_input = ft.TextField(
        label="Nome da Escola",
        value=escola["NomeEscola"],
        prefix_icon=ft.Icons.LOCATION_CITY,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        color=cor_texto_claro,
        text_size=15,
    )

    # Feedback
    mensagem_feedback = ft.Container(visible=False)

    def mostrar_feedback(msg, cor):
        mensagem_feedback.content = ft.Text(msg, size=14, color=cor)
        mensagem_feedback.visible = True
        page.update()

    def atualizar_escola(e):
        novo_nome = nome_input.value.strip()
        if not novo_nome:
            mostrar_feedback("⚠️ Preenche o Nome da escola.", "#EF4444")
            return

        try:
            sucesso = atualizarEscola(id_escola, novo_nome)
            if sucesso:
                mostrar_feedback("✅ Escola atualizada com sucesso!", "#10B981")
                import time
                time.sleep(1)
                page.go("/TelaPrincipalAdmin")
            else:
                mostrar_feedback("Nenhuma alteração foi realizada.", "#EF4444")
        except Exception as ex:
            mostrar_feedback(str(ex), "#EF4444")

    # Botões
    btn_salvar = estilo_botao_acao(
        "Salvar Alterações",
        ft.Icons.SAVE_ROUNDED,
        atualizar_escola,
    )

    btn_voltar = ft.OutlinedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ARROW_BACK, color=cor_texto_medio, size=18),
             ft.Text("Voltar", color=cor_texto_medio, size=14)],
            spacing=8
        ),
        style=ft.ButtonStyle(
            padding=12,
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.border.all(1, cor_borda)
        ),
        on_click=lambda e: page.go("/TelaPrincipalAdmin")
    )

    # Card central
    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Text("Editar Escola", size=26, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                ft.Text(escola["NomeEscola"], size=14, color=cor_texto_medio),
                ft.Divider(height=30, color=cor_borda),
                mensagem_feedback,
                nome_input,
                ft.Row([btn_voltar, btn_salvar], alignment=ft.MainAxisAlignment.END, spacing=12),
            ],
            spacing=20
        ),
        padding=40,
        width=600,
        bgcolor=cor_card,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=30,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.35, cor_primaria),
            offset=ft.Offset(0, 6)
        ),
    )

    # View final centralizada
    return ft.View(
        "/editar-escola",
        [
            ft.Container(
                content=ft.Column(
                    [formulario],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                expand=True,
                bgcolor=cor_fundo,
            )
        ],
        bgcolor=cor_fundo,
    )
