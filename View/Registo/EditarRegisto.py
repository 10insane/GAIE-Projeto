import flet as ft
from Models.RegistoModel import buscarRegistoPorId, atualizarRegisto
from Models.ProblematicaSPO import criarProblematica
from Models.AlunosModel import listarAlunos
from Models.TecnicoModel import listarTecnico
from Controller.EstadoProcessoController import Listar as listarEstadosProcesso
from datetime import date

def PaginaEditarRegisto(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    # === CORES (do estilos.py) ===
    cor_primaria = "#8B5CF6"
    cor_secundaria = "#A78BFA"
    cor_roxo_escuro = "#6D28D9"
    cor_fundo = "#0F0F0F"
    cor_card = "#121212"
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#9CA3AF"
    cor_texto_escuro = "#D1D5DB"
    cor_borda = "#242424"
    cor_sucesso = "#10B981"
    cor_erro = "#DC2626"

    # ===== PEGAR ID DO REGISTO =====
    idRegisto = page.session.get("registo_editar_id")
    if not idRegisto:
        return ft.View(controls=[ft.Text("Erro: Nenhum registo selecionado")])

    # ===== BUSCAR REGISTO =====
    registo = buscarRegistoPorId(idRegisto)
    if not registo:
        return ft.View(controls=[ft.Text("Erro: Registo não encontrado")])

    # Carregar dados
    alunos = listarAlunos()
    tecnicos = listarTecnico()
    estados = listarEstadosProcesso()

    # -----------------------------------------------------------
    #  CAMPOS — Nº PROCESSO ALUNO + ALUNO AUTOMÁTICO
    # -----------------------------------------------------------

    txt_num_processo = ft.TextField(
        label="Número de Processo (Aluno)",
        hint_text="Digite o nº processo do aluno",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.NUMBERS,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    txt_nome_aluno = ft.TextField(
        label="Aluno",
        read_only=True,
        border_color=cor_borda,
        prefix_icon=ft.Icons.PERSON,
        text_size=15,
        color=cor_secundaria,
        label_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    def preencher_nome_aluno(e=None):
        nproc = txt_num_processo.value.strip()

        if nproc.isdigit():
            aluno = next((a for a in alunos if str(a["nProcessoAluno"]) == nproc), None)
            txt_nome_aluno.value = aluno["NomeAluno"] if aluno else "Aluno não encontrado"
        else:
            txt_nome_aluno.value = ""

        page.update()

    txt_num_processo.on_change = preencher_nome_aluno

    # -----------------------------------------------------------
    #  CAMPOS — Nº PROCESSO TÉCNICO + TÉCNICO AUTOMÁTICO
    # -----------------------------------------------------------

    txt_num_tecnico = ft.TextField(
        label="Número de Processo do Técnico",
        hint_text="Digite o nº processo do técnico",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.BADGE,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    txt_nome_tecnico = ft.TextField(
        label="Técnico",
        read_only=True,
        border_color=cor_borda,
        prefix_icon=ft.Icons.PERSON_SEARCH,
        text_size=15,
        color=cor_secundaria,
        label_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    def preencher_nome_tecnico(e=None):
        nproc = txt_num_tecnico.value.strip()

        if nproc.isdigit():
            tecnico = next((t for t in tecnicos if str(t["nProcTecnico"]) == nproc), None)
            txt_nome_tecnico.value = tecnico["NomeTecnico"] if tecnico else "Técnico não encontrado"
        else:
            txt_nome_tecnico.value = ""

        page.update()

    txt_num_tecnico.on_change = preencher_nome_tecnico

    # -----------------------------------------------------------   

    dropdown_estadosprocesso = ft.Dropdown(
        label="Estado do Processo",
        hint_text="Selecione o estado",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.FLAG,
        options=[ft.dropdown.Option(key=str(e["idEstado"]), text=e["Estado"]) for e in estados]
                if estados else [ft.dropdown.Option("0", "Nenhum estado disponível")],
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    # Container para mostrar a data selecionada
    data_registo = {"valor": None, "display": "Selecionar Data"}

    def abrir_calendario(e):
        def ao_selecionar_data(e):
            if date_picker.value:
                data_registo["valor"] = date_picker.value.strftime("%Y-%m-%d")
               
                # Formatar data em português
                meses_pt = {
                    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
                }
               
                data_obj = date_picker.value
                data_registo["display"] = f"{data_obj.day} de {meses_pt[data_obj.month]} de {data_obj.year}"
               
                btn_selecionar_data.content.controls[0] = ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=cor_primaria)
                btn_selecionar_data.content.controls[1] = ft.Text(data_registo["display"], size=15, color=cor_texto_claro)
                page.update()
            date_picker.open = False
            page.update()

        def fechar_calendario(e):
            date_picker.open = False
            page.update()

        date_picker = ft.DatePicker(
            first_date=date(2000, 1, 1),
            last_date=date(2100, 12, 31),
            on_change=ao_selecionar_data,
            on_dismiss=fechar_calendario,
        )
       
        page.overlay.append(date_picker)
        page.update()
        date_picker.open = True
        page.update()

    btn_selecionar_data = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=cor_texto_medio),
                ft.Text("Selecionar Data", size=15, color=cor_texto_medio),
            ],
            spacing=10,
        ),
        bgcolor=cor_fundo,
        padding=ft.padding.only(left=15, right=15, top=16, bottom=16),
        border_radius=4,
        border=ft.border.all(1, cor_borda),
        on_click=abrir_calendario,
        ink=True,
    )

    txt_descricao = ft.TextField(
        label="Descrição",
        hint_text="Descrição opcional",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.DESCRIPTION,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        multiline=True,
        max_lines=3,
    )

    txt_problematica = ft.TextField(
        label="Problemática",
        hint_text="Digite a problemática",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.BUG_REPORT,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        multiline=True,
        max_lines=2,
    )

    mensagem_feedback = ft.Container(visible=False)

    # ------------------ Pré-preencher com dados existentes -----------------
    txt_num_processo.value = str(registo.get("nProcessoAluno", ""))
    txt_nome_aluno.value = registo.get("NomeAluno", "")
    txt_num_tecnico.value = str(registo.get("nProcTecnico", "")) if registo.get("nProcTecnico") else ""
    txt_nome_tecnico.value = registo.get("NomeTecnico", "") or ""
    dropdown_estadosprocesso.value = str(registo.get("idEstado")) if registo.get("idEstado") else None
    txt_descricao.value = registo.get("Observacoes", "") or ""
    txt_problematica.value = registo.get("tipoProblematica", "") or ""

    # Preparar data para visualização
    raw_data = registo.get("DataArquivo")
    try:
        if raw_data:
            if isinstance(raw_data, str):
                data_obj = date.fromisoformat(raw_data)
            else:
                data_obj = raw_data
            meses_pt = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
            data_registo["valor"] = data_obj.strftime("%Y-%m-%d")
            data_registo["display"] = f"{data_obj.day} de {meses_pt[data_obj.month]} de {data_obj.year}"
            btn_selecionar_data.content = ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=cor_primaria),
                ft.Text(data_registo["display"], size=15, color=cor_texto_claro)
            ], spacing=10)
    except Exception:
        pass

    # ======================= SALVAR (Atualizar) ==========================

    def salvar_registo(e):
        erros = []

        if not txt_num_processo.value.strip():
            erros.append("Número de processo do aluno é obrigatório")
        if txt_nome_aluno.value in ["", "Aluno não encontrado"]:
            erros.append("Número de processo do aluno inválido")

        if txt_num_tecnico.value.strip() and txt_nome_tecnico.value == "Técnico não encontrado":
            erros.append("Número de processo do técnico inválido")

        if not dropdown_estadosprocesso.value:
            erros.append("Estado do processo é obrigatório")

        if not data_registo["valor"]:
            erros.append("Data é obrigatória")

        if not txt_problematica.value.strip():
            erros.append("Problemática é obrigatória")

        if erros:
            mensagem_feedback.content = ft.Container(
                content=ft.Text("\n".join(erros), color=cor_erro, size=14),
                bgcolor="#1A0000",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()
            return

        try:
            idProblematica = criarProblematica(txt_problematica.value.strip()) if txt_problematica.value.strip() else None

            nProcTecnico = txt_num_tecnico.value.strip() or None

            sucesso = atualizarRegisto(
                idRegisto=idRegisto,
                nProcessoAluno=txt_num_processo.value.strip(),
                idEstado=int(dropdown_estadosprocesso.value),
                DataArquivo=data_registo["valor"],
                Observacoes=txt_descricao.value.strip() or None,
                nProcTecnico=nProcTecnico,
                idProblematica=idProblematica
            )

            if sucesso:
                mensagem_feedback.content = ft.Container(
                    content=ft.Text("✓ Registo atualizado com sucesso!", color=cor_sucesso, size=14),
                    bgcolor="#001A0A",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, cor_sucesso),
                )
                mensagem_feedback.visible = True
                page.update()
                import time
                time.sleep(1)
                page.go("/pagina-principal")

        except Exception as ex:
            mensagem_feedback.content = ft.Container(
                content=ft.Text(f"✗ Erro: {str(ex)}", color=cor_erro, size=14),
                bgcolor="#1A0000",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()

    # ======================= BOTÕES ==========================

    btn_salvar = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SAVE, size=18),
                    ft.Text("Guardar Registo", size=15, weight=ft.FontWeight.BOLD),
                ],
                tight=True,
                spacing=8,
            ),
            bgcolor=cor_primaria,
            color=ft.Colors.WHITE,
            on_click=salvar_registo,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
            ),
        ),
    )

    btn_cancelar = ft.Container(
        content=ft.OutlinedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CLOSE, size=18),
                    ft.Text("Cancelar", size=15),
                ],
                tight=True,
                spacing=8,
            ),
            on_click=lambda e: page.go("/pagina-principal"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
                side=ft.BorderSide(1, cor_borda),
                color=cor_texto_claro,
            ),
        ),
    )

    # ======================= CABEÇALHO ==========================

    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=cor_primaria, size=32),
                        ft.Text("Sistema SPO", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ],
                    spacing=12,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.PERSON, color=cor_secundaria, size=20),
                        ft.Text(tecnico_nome, size=15, color=cor_texto_medio),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
    )

    # ======================= FORMULÁRIO ==========================

    formulario = ft.Container(
        content=ft.Column(
            [
                # Header com gradiente visual
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=cor_primaria,
                            icon_size=24,
                            on_click=lambda e: page.go("/pagina-principal"),
                            tooltip="Voltar",
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Editar Registo",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Atualize os campos abaixo para editar o registo",
                                    size=13,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=4,
                        ),
                    ]),
                    padding=ft.padding.only(bottom=15),
                ),

                mensagem_feedback,

                # Linha 1: Aluno e Técnico lado a lado
                ft.Row(
                    [
                        # Seção Aluno
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.SCHOOL, color=cor_primaria, size=18),
                                        ft.Text("Dados do Aluno", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_num_processo,
                                    txt_nome_aluno,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),

                        # Seção Técnico
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.ENGINEERING, color=cor_secundaria, size=18),
                                        ft.Text("Dados do Técnico", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_num_tecnico,
                                    txt_nome_tecnico,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
                    ],
                    spacing=15,
                ),

                # Seção Processo
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Icon(ft.Icons.ARTICLE, color=cor_roxo_escuro, size=18),
                                ft.Text("Detalhes do Processo", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ], spacing=8),
                            ft.Container(height=5),
                            ft.Row([dropdown_estadosprocesso, btn_selecionar_data], spacing=15),
                            txt_descricao,
                            txt_problematica,
                        ],
                        spacing=10
                    ),
                    bgcolor=cor_card,
                    padding=15,
                    border_radius=12,
                    border=ft.border.all(1, cor_borda),
                ),

                # Botões
                ft.Container(
                    content=ft.Row(
                        [btn_cancelar, btn_salvar],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=12,
                    ),
                    padding=ft.padding.only(top=5),
                ),
            ],
            spacing=15,
        ),
        bgcolor=cor_card,
        padding=30,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        width=900,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, cor_primaria),
        ),
    )

    return ft.View(
        route="/EditarRegisto",
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
