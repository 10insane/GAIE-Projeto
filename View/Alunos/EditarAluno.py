import flet as ft
from Models.AlunosModel import *
from Models.EscolasModel import listarEscolas
from View.PaginaPrincipal.estilos import *
from View.PaginaPrincipal.util_buttons import estilo_botao_acao

def PaginaEditarAluno(page: ft.Page):

    nProcessoAluno = page.session.get("aluno_editar_id")
    if not nProcessoAluno:
        page.go("/TelaPrincipalAdmin")
        return

    aluno = buscarAlunoPorProcesso(nProcessoAluno)
    if not aluno:
        page.go("/TelaPrincipalAdmin")
        return

    # ------------------------
    # Campos do formulário
    # ------------------------
    txt_numero_processo = ft.TextField(
        label="Número de Processo",
        value=aluno["nProcessoAluno"],
        prefix_icon=ft.Icons.NUMBERS,
        read_only=True,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        color=cor_texto_claro,
        text_size=15
    )

    txt_nome = ft.TextField(
        label="Nome Completo",
        value=aluno["NomeAluno"],
        prefix_icon=ft.Icons.PERSON,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        color=cor_texto_claro,
        text_size=15
    )

    txt_turma = ft.TextField(
        label="Turma",
        value=aluno["Turma"],
        prefix_icon=ft.Icons.MEETING_ROOM,
        max_length=3,
        border_color=cor_borda,
        focused_border_color=cor_secundaria,
        color=cor_texto_claro,
        text_size=15
    )

    txt_ano = ft.Dropdown(
        label="Ano",
        value=str(aluno["Ano"]),
        prefix_icon=ft.Icons.SCHOOL,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)]
    )

    try:
        escolas = listarEscolas()
    except:
        escolas = []

    dropdown_escola = ft.Dropdown(
        label="Escola",
        value=str(aluno["idEscola"]),
        prefix_icon=ft.Icons.LOCATION_CITY,
        options=[
            ft.dropdown.Option(key=str(e["idEscola"]), text=e["NomeEscola"])
            for e in escolas
        ] if escolas else [ft.dropdown.Option("0", "Nenhuma escola disponível")]
    )

    # ------------------------
    # Feedback
    # ------------------------
    mensagem_feedback = ft.Container(visible=False)

    def mostrar_feedback(msg, cor):
        mensagem_feedback.content = ft.Text(msg, size=14, color=cor)
        mensagem_feedback.visible = True
        page.update()

    # ------------------------
    # Função atualizar
    # ------------------------
    def atualizar_aluno(e):
        erros = []
        if not txt_nome.value.strip():
            erros.append("O nome é obrigatório.")
        if not txt_ano.value:
            erros.append("Selecione o ano escolar.")
        if not txt_turma.value.strip():
            erros.append("A turma é obrigatória.")
        if not dropdown_escola.value or dropdown_escola.value == "0":
            erros.append("Selecione a escola.")

        if erros:
            mostrar_feedback("\n".join([f"• {err}" for err in erros]), "#EF4444")
            return

        try:
            sucesso = atualizarAluno(
                nProcessoAluno=txt_numero_processo.value,
                novoNome=txt_nome.value.strip(),
                novoAno=int(txt_ano.value),
                novaTurma=txt_turma.value.strip().upper(),
                novoIdEscola=int(dropdown_escola.value),
            )
            if sucesso:
                mostrar_feedback("Aluno atualizado com sucesso!", "#10B981")
                import time
                time.sleep(1)
                page.go("/TelaPrincipalAdmin")
            else:
                mostrar_feedback("Nenhuma alteração foi realizada.", "#EF4444")
        except Exception as ex:
            mostrar_feedback(str(ex), "#EF4444")

    # ------------------------
    # Botões
    # ------------------------
    btn_salvar = estilo_botao_acao(
        "Salvar Alterações",
        ft.Icons.SAVE_ROUNDED,
        atualizar_aluno
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

    # ------------------------
    # Card central
    # ------------------------
    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Text("Editar Aluno", size=26, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                ft.Text(aluno["NomeAluno"], size=14, color=cor_texto_medio),
                ft.Divider(height=30, color=cor_borda),
                mensagem_feedback,
                txt_numero_processo,
                txt_nome,
                ft.Row([txt_ano, txt_turma], spacing=12),
                dropdown_escola,
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

    # ------------------------
    # View final centralizada
    # ------------------------
    return ft.View(
        "/editar-aluno",
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
