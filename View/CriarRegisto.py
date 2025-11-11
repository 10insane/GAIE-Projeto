import flet as ft
from Models.RegistoModel import criarRegisto
from Models.AlunosModel import listarAlunos
from Models.TecnicoModel import listarTecnico
from Controller.EstadoProcessoController import Listar as listarEstadosProcesso

def PaginaCriarRegisto(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    # === CORES ===
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
    cor_texto_medio = "#334155"
    cor_texto_claro = "#64748B"
    cor_borda = "#E2E8F0"
    cor_sucesso = "#10B981"
    cor_erro = "#DC2626"

    # Carregar dados
    alunos = listarAlunos()
    tecnicos = listarTecnico()
    estados = listarEstadosProcesso()

    # Dropdown Aluno
    dropdown_aluno = ft.Dropdown(
        label="Aluno",
        hint_text="Selecione o aluno",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.PERSON,
        options=[ft.dropdown.Option(key=str(a["nProcessoAluno"]), text=a["NomeAluno"]) for a in alunos] if alunos else [ft.dropdown.Option("0", "Nenhum aluno disponível")],
        text_size=15,
        color="#000000",
    )

    # Dropdown Estado do Processo
    dropdown_estadosprocesso = ft.Dropdown(
        label="Estado do Processo",
        hint_text="Selecione o estado",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.FLAG,
        options=[ft.dropdown.Option(key=str(e["idEstado"]), text=e["Estado"]) for e in estados] if estados else [ft.dropdown.Option("0", "Nenhum estado disponível")],
        text_size=15,
        color="#000000",
    )

    # Campo Data
    txt_data = ft.TextField(
        label="Data do Registo",
        hint_text="AAAA-MM-DD",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        text_size=15,
        color="#000000",
    )

    # Campo Descrição
    txt_descricao = ft.TextField(
        label="Descrição",
        hint_text="Descrição opcional",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.DESCRIPTION,
        text_size=15,
        color="#000000",
        multiline=True,
        max_lines=3,
    )

    # Dropdown Técnico
    dropdown_tecnico = ft.Dropdown(
        label="Técnico Responsável (Opcional)",
        hint_text="Selecione o técnico",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.PERSON,
        options=[ft.dropdown.Option(key=str(t["nProcTecnico"]), text=t["NomeTecnico"]) for t in tecnicos] if tecnicos else [ft.dropdown.Option("0", "Nenhum técnico disponível")],
        text_size=15,
        color="#000000",
    )

    # Mensagem de feedback
    mensagem_feedback = ft.Container(visible=False)

    # Função salvar
    def salvar_registo(e):
        erros = []

        if not dropdown_aluno.value or dropdown_aluno.value == "0":
            erros.append("Aluno é obrigatório")
        if not dropdown_estadosprocesso.value or dropdown_estadosprocesso.value == "0":
            erros.append("Estado do processo é obrigatório")
        if not txt_data.value or txt_data.value.strip() == "":
            erros.append("Data é obrigatória")

        if erros:
            mensagem_feedback.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                                ft.Text("Erros no formulário:", size=15, weight=ft.FontWeight.BOLD, color=cor_erro)],
                               spacing=10),
                        ft.Column([ft.Text(f"• {erro}", size=13, color=cor_erro) for erro in erros], spacing=5),
                    ],
                    spacing=10,
                ),
                bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
                border=ft.border.all(1, cor_erro),
                border_radius=12,
                padding=16,
            )
            mensagem_feedback.visible = True
            page.update()
            return

        try:
            nProcTecnico = dropdown_tecnico.value if dropdown_tecnico.value and dropdown_tecnico.value != "0" else None
            sucesso = criarRegisto(
                nProcessoAluno=dropdown_aluno.value,
                idEstado=int(dropdown_estadosprocesso.value),
                DataArquivo=txt_data.value.strip(),
                descricao=txt_descricao.value.strip() if txt_descricao.value else None,
                nProcTecnico=nProcTecnico
            )

            if sucesso:
                mensagem_feedback.content = ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=cor_sucesso, size=24),
                                    ft.Text("Registo criado com sucesso!", size=15, weight=ft.FontWeight.BOLD, color=cor_sucesso)],
                                   spacing=12),
                    bgcolor=ft.Colors.with_opacity(0.1, cor_sucesso),
                    border=ft.border.all(1, cor_sucesso),
                    border_radius=12,
                    padding=16,
                )
                mensagem_feedback.visible = True
                page.update()
                import time
                time.sleep(1.5)
                page.go("/pagina-principal")
            else:
                raise Exception("Erro ao criar registo")

        except Exception as ex:
            mensagem_feedback.content = ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                                ft.Text(f"Erro ao criar registo: {str(ex)}", size=14, color=cor_erro)],
                               spacing=10),
                bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
                border=ft.border.all(1, cor_erro),
                border_radius=12,
                padding=16,
            )
            mensagem_feedback.visible = True
            page.update()

    # Botões
    btn_salvar = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.Icons.SAVE, size=20),
                        ft.Text("Guardar Registo", size=15, weight=ft.FontWeight.BOLD)], spacing=8),
        bgcolor=cor_primaria,
        color=ft.Colors.WHITE,
        on_click=salvar_registo,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(horizontal=28, vertical=18)),
    )

    btn_cancelar = ft.OutlinedButton(
        content=ft.Row([ft.Icon(ft.Icons.CANCEL, size=20, color=cor_texto_medio),
                        ft.Text("Voltar", size=15, weight=ft.FontWeight.W_600, color=cor_texto_medio)], spacing=8),
        on_click=lambda e: page.go("/pagina-principal"),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(horizontal=28, vertical=18), side=ft.BorderSide(1, cor_borda)),
    )

    # Formulário
    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=cor_primaria, icon_size=28, on_click=lambda e: page.go("/pagina-principal"), tooltip="Voltar"),
                        ft.Column([ft.Text("Criar Novo Registo", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                   ft.Text("Preencha os dados do registo", size=14, color=cor_texto_claro)], spacing=5, expand=True)], spacing=15),
                ft.Divider(height=30, color=cor_borda),
                mensagem_feedback,
                ft.Container(content=ft.Column([dropdown_aluno, dropdown_estadosprocesso, txt_data, txt_descricao, dropdown_tecnico], spacing=20), padding=ft.padding.only(top=10, bottom=20)),
                ft.Row([btn_cancelar, btn_salvar], spacing=15, alignment=ft.MainAxisAlignment.END),
            ],
            spacing=15,
        ),
        bgcolor=cor_card,
        padding=40,
        border_radius=16,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)),
        width=700,
    )

    conteudo_principal = ft.Container(
        content=ft.Column([formulario], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        bgcolor=cor_fundo,
        padding=40,
        alignment=ft.alignment.center,
        expand=True,
    )

    return ft.View(route="/CriarRegisto", controls=[conteudo_principal], bgcolor=cor_fundo)
