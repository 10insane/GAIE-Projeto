import flet as ft
from Models.RegistoModel import criarRegisto
from Models.ProblematicaSPO import criarProblematica, listarProblematicas
from Models.AlunosModel import listarAlunos
from Models.TecnicoModel import listarTecnico
from Controller.EstadoProcessoController import Listar as listarEstadosProcesso
from datetime import date
import time

# Constantes de cores para o tema da aplicação
CORES = {
    "primaria": "#3B82F6",
    "secundaria": "#60A5FA",
    "azul_escuro": "#1E40AF",
    "fundo": "#0F172A",
    "card": "#1E293B",
    "card_hover": "#2D3B52",
    "texto_claro": "#F1F5F9",
    "texto_medio": "#94A3B8",
    "texto_escuro": "#CBD5E1",
    "borda": "#334155",
    "sucesso": "#10B981",
    "erro": "#DC2626",
    "aviso": "#F59E0B",
    "info": "#3B82F6"
}

# Mapeamento de meses em português
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def PaginaCriarRegisto(page: ft.Page):
    """
    Página para criar um novo registo no sistema SPO.
    """
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    # Carregar dados necessários
    alunos = listarAlunos()
    tecnicos = listarTecnico()
    estados = listarEstadosProcesso()
    problematicas = listarProblematicas()

    # Estado da data de registo
    data_registo = {"valor": None, "display": "Selecionar Data"}

    # Campos do formulário
    campos = criar_campos_formulario(alunos, tecnicos, estados, problematicas, page, data_registo)

    # Botões
    btn_salvar, btn_cancelar = criar_botoes(campos, data_registo, page, problematicas)

    # Componentes da UI
    cabecalho = criar_cabecalho(tecnico_nome)
    formulario = criar_formulario(campos, btn_salvar, btn_cancelar, page)

    return ft.View(
        route="/CriarRegisto",
        controls=[
            ft.Column(
                [cabecalho, ft.Container(content=formulario, alignment=ft.alignment.center)],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        bgcolor=CORES["fundo"],
        padding=25,
    )

def criar_campos_formulario(alunos, tecnicos, estados, problematicas, page, data_registo):
    """
    Cria e configura todos os campos do formulário.
    """
    # Campo Número de Processo do Aluno
    txt_num_processo = criar_text_field("Número de Processo", "Ex: 12345", ft.Icons.NUMBERS)
    txt_nome_aluno = criar_text_field("Nome do Aluno", "", ft.Icons.PERSON, read_only=True)

    def preencher_nome_aluno(e=None):
        atualizar_campo_automatico(txt_num_processo, txt_nome_aluno, alunos, "nProcessoAluno", "NomeAluno", page)

    txt_num_processo.on_change = preencher_nome_aluno

    # Campo Número de Processo do Técnico
    txt_num_tecnico = criar_text_field("Número de Processo", "Ex: 67890", ft.Icons.BADGE)
    txt_nome_tecnico = criar_text_field("Nome do Técnico", "", ft.Icons.PERSON_SEARCH, read_only=True)

    def preencher_nome_tecnico(e=None):
        atualizar_campo_automatico(txt_num_tecnico, txt_nome_tecnico, tecnicos, "nProcTecnico", "NomeTecnico", page)

    txt_num_tecnico.on_change = preencher_nome_tecnico

    # Dropdown Estado do Processo (bloqueado em "A Aguardar")
    estado_aguardar = next((e for e in estados if e["Estado"].lower() == "a aguardar"), None)
    estado_aguardar_id = str(estado_aguardar["idEstado"]) if estado_aguardar else None

    dropdown_estadosprocesso = ft.Dropdown(
        label="Estado do Processo",
        value=estado_aguardar_id,
        disabled=True,
        options=[ft.dropdown.Option(key=str(e["idEstado"]), text=e["Estado"]) for e in estados] or [ft.dropdown.Option("0", "Nenhum estado disponível")],
        **estilo_dropdown()
    )

    # Dropdown Problemáticas
    dropdown_problematica = ft.Dropdown(
        label="Problemática",
        hint_text="Selecione a problemática",
        options=[ft.dropdown.Option(key=str(p["idProblematica"]), text=p["TipoProblematica"]) for p in problematicas] or [ft.dropdown.Option("0", "Nenhuma problemática")],
        **estilo_dropdown()
    )

    # Botão para selecionar data
    btn_selecionar_data = criar_botao_data(page, data_registo)

    # Campo Observações
    txt_descricao = criar_text_field("Observações", "Adicione observações adicionais (opcional)", ft.Icons.DESCRIPTION, multiline=True, min_lines=3, max_lines=5)

    # Container para mensagens de feedback
    mensagem_feedback = ft.Container(visible=False)

    return {
        "txt_num_processo": txt_num_processo,
        "txt_nome_aluno": txt_nome_aluno,
        "txt_num_tecnico": txt_num_tecnico,
        "txt_nome_tecnico": txt_nome_tecnico,
        "dropdown_estadosprocesso": dropdown_estadosprocesso,
        "dropdown_problematica": dropdown_problematica,
        "btn_selecionar_data": btn_selecionar_data,
        "txt_descricao": txt_descricao,
        "mensagem_feedback": mensagem_feedback
    }

def criar_text_field(label, hint_text, icon, read_only=False, multiline=False, min_lines=1, max_lines=1):
    """
    Cria um campo de texto com estilo consistente.
    """
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        border_color=CORES["borda"],
        focused_border_color=CORES["primaria"],
        prefix_icon=icon,
        text_size=15,
        color=CORES["texto_claro"],
        label_style=ft.TextStyle(color=CORES["texto_medio"], size=13),
        hint_style=ft.TextStyle(color=CORES["texto_medio"]),
        bgcolor=CORES["fundo"],
        filled=True,
        border_radius=8,
        read_only=read_only,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=max_lines
    )

def estilo_dropdown():
    """
    Retorna o estilo padrão para dropdowns.
    """
    return {
        "border_color": CORES["borda"],
        "focused_border_color": CORES["primaria"],
        "prefix_icon": ft.Icons.FLAG,
        "text_size": 15,
        "color": CORES["texto_claro"],
        "label_style": ft.TextStyle(color=CORES["texto_medio"], size=13),
        "hint_style": ft.TextStyle(color=CORES["texto_medio"]),
        "bgcolor": CORES["fundo"],
        "filled": True,
        "border_radius": 8
    }

def atualizar_campo_automatico(campo_num, campo_nome, lista, chave_num, chave_nome, page):
    """
    Atualiza o campo de nome baseado no número de processo.
    """
    nproc = campo_num.value.strip()
    if nproc.isdigit():
        item = next((i for i in lista if str(i[chave_num]) == nproc), None)
        if item:
            campo_nome.value = item[chave_nome]
            campo_nome.border_color = CORES["sucesso"]
        else:
            campo_nome.value = "⚠ Item não encontrado"
            campo_nome.border_color = CORES["erro"]
    else:
        campo_nome.value = ""
        campo_nome.border_color = CORES["borda"]
    page.update()

def criar_botao_data(page, data_registo):
    """
    Cria o botão para seleção de data com calendário.
    """
    def abrir_calendario(e):
        def ao_selecionar_data(e):
            if date_picker.value:
                data_registo["valor"] = date_picker.value.strftime("%Y-%m-%d")
                data_obj = date_picker.value
                data_registo["display"] = f"{data_obj.day} de {MESES_PT[data_obj.month]} de {data_obj.year}"
                btn_selecionar_data.content.controls[0] = ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=CORES["sucesso"])
                btn_selecionar_data.content.controls[1] = ft.Text(data_registo["display"], size=15, color=CORES["texto_claro"], weight=ft.FontWeight.W_500)
                btn_selecionar_data.border = ft.border.all(1, CORES["sucesso"])
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
        content=ft.Row([
            ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=CORES["texto_medio"]),
            ft.Text("Selecionar Data", size=15, color=CORES["texto_medio"])
        ], spacing=10),
        bgcolor=CORES["fundo"],
        padding=ft.padding.only(left=15, right=15, top=16, bottom=16),
        border_radius=8,
        border=ft.border.all(1, CORES["borda"]),
        on_click=abrir_calendario,
        ink=True,
        animate=ft.Animation(200, "easeOut"),
    )
    return btn_selecionar_data

def criar_botoes(campos, data_registo, page, problematicas):
    """
    Cria os botões Salvar e Cancelar.
    """
    def salvar_registo(e):
        erros = validar_campos(campos, data_registo)
        if erros:
            mostrar_mensagem_erro(campos["mensagem_feedback"], erros, page)
            return

        try:
            prob_selecionada = next((p for p in problematicas if str(p["idProblematica"]) == campos["dropdown_problematica"].value), None)
            tipo_problematica = prob_selecionada["TipoProblematica"] if prob_selecionada else None

            sucesso = criarRegisto(
                nProcessoAluno=campos["txt_num_processo"].value.strip(),
                idEstado=int(campos["dropdown_estadosprocesso"].value),
                DataArquivo=data_registo["valor"],
                Observacoes=campos["txt_descricao"].value.strip() or None,
                nProcTecnico=campos["txt_num_tecnico"].value.strip(),
                tipoProblematica=tipo_problematica
            )

            if sucesso:
                mostrar_mensagem_sucesso(campos["mensagem_feedback"], page)
                time.sleep(1.5)
                page.go("/pagina-principal")
        except Exception as ex:
            mostrar_mensagem_erro(campos["mensagem_feedback"], [str(ex)], page, titulo="Erro ao criar registo:")

    btn_salvar = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.Icons.SAVE, size=20), ft.Text("Guardar Registo", size=16, weight=ft.FontWeight.BOLD)], tight=True, spacing=10),
        bgcolor=CORES["primaria"],
        color=ft.Colors.WHITE,
        on_click=salvar_registo,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(horizontal=28, vertical=16), elevation=3),
        height=50,
    )

    btn_cancelar = ft.OutlinedButton(
        content=ft.Row([ft.Icon(ft.Icons.CLOSE, size=20), ft.Text("Cancelar", size=16)], tight=True, spacing=10),
        on_click=lambda e: page.go("/pagina-principal"),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(horizontal=28, vertical=16), side=ft.BorderSide(2, CORES["borda"]), color=CORES["texto_claro"]),
        height=50,
    )

    return btn_salvar, btn_cancelar

def validar_campos(campos, data_registo):
    """
    Valida os campos obrigatórios e retorna lista de erros.
    """
    erros = []
    if not campos["txt_num_processo"].value.strip():
        erros.append("• Número de processo do aluno é obrigatório")
    if campos["txt_nome_aluno"].value in ["", "⚠ Item não encontrado"]:
        erros.append("• Número de processo do aluno inválido")

    if not campos["txt_num_tecnico"].value.strip():
        erros.append("• Número de processo do técnico é obrigatório")
    if campos["txt_nome_tecnico"].value in ["", "⚠ Item não encontrado"]:
        erros.append("• Número de processo do técnico inválido")

    if not campos["dropdown_estadosprocesso"].value:
        erros.append("• Estado do processo é obrigatório")

    if not data_registo["valor"]:
        erros.append("• Data é obrigatória")

    if not campos["dropdown_problematica"].value:
        erros.append("• Problemática é obrigatória")

    return erros

def mostrar_mensagem_erro(container, erros, page, titulo="Erros de validação:"):
    """
    Exibe mensagem de erro no container.
    """
    container.content = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color=CORES["erro"], size=20), ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=CORES["erro"])], spacing=8),
            ft.Text("\n".join(erros), color=CORES["texto_claro"], size=13)
        ], spacing=8),
        bgcolor="#2D1515",
        padding=15,
        border_radius=8,
        border=ft.border.all(2, CORES["erro"])
    )
    container.visible = True
    page.update()

def mostrar_mensagem_sucesso(container, page):
    """
    Exibe mensagem de sucesso no container.
    """
    container.content = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=CORES["sucesso"], size=20), ft.Text("Registo criado com sucesso!", size=14, weight=ft.FontWeight.BOLD, color=CORES["sucesso"])], spacing=8),
        bgcolor="#0F2A1A",
        padding=15,
        border_radius=8,
        border=ft.border.all(2, CORES["sucesso"])
    )
    container.visible = True
    page.update()

def criar_cabecalho(tecnico_nome):
    """
    Cria o cabeçalho da página.
    """
    return ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(content=ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=ft.Colors.WHITE, size=28), bgcolor=CORES["primaria"], padding=10, border_radius=10),
                ft.Column([ft.Text("Sistema SPO", size=22, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]), ft.Text("Gestão de Processos", size=12, color=CORES["texto_medio"])], spacing=2)
            ], spacing=12),
            ft.Container(content=ft.Row([ft.Icon(ft.Icons.PERSON, color=CORES["primaria"], size=20), ft.Text(tecnico_nome, size=15, color=CORES["texto_claro"], weight=ft.FontWeight.W_500)], spacing=8), bgcolor=CORES["fundo"], padding=ft.padding.symmetric(horizontal=16, vertical=10), border_radius=8, border=ft.border.all(1, CORES["borda"]))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=CORES["card"],
        padding=20,
        border_radius=12,
        border=ft.border.all(1, CORES["borda"]),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.1, "#000000"))
    )

def criar_formulario(campos, btn_salvar, btn_cancelar, page):
    """
    Cria o formulário principal.
    """
    return ft.Container(
        content=ft.Column([
            # Header
            ft.Container(content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=CORES["primaria"], icon_size=24, on_click=lambda e: page.go("/pagina-principal"), tooltip="Voltar", bgcolor=CORES["fundo"], style=ft.ButtonStyle(shape=ft.CircleBorder())),
                ft.Column([ft.Text("Criar Novo Registo", size=26, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]), ft.Text("Preencha todos os campos obrigatórios para registar um novo processo", size=14, color=CORES["texto_medio"])], spacing=4)
            ]), padding=ft.padding.only(bottom=20)),

            campos["mensagem_feedback"],

            # Seção Aluno e Técnico
            ft.Row([
                ft.Container(content=ft.Column([
                    ft.Row([ft.Container(content=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=18), bgcolor=CORES["primaria"], padding=6, border_radius=6), ft.Text("Informações do Aluno", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]), ft.Container(content=ft.Text("*", color=CORES["erro"], size=16), tooltip="Campo obrigatório")], spacing=10),
                    ft.Divider(height=1, color=CORES["borda"]),
                    ft.Container(height=5),
                    campos["txt_num_processo"],
                    campos["txt_nome_aluno"]
                ], spacing=12), bgcolor=CORES["card"], padding=20, border_radius=12, border=ft.border.all(1, CORES["borda"]), expand=1),

                ft.Container(content=ft.Column([
                    ft.Row([ft.Container(content=ft.Icon(ft.Icons.ENGINEERING, color=ft.Colors.WHITE, size=18), bgcolor=CORES["secundaria"], padding=6, border_radius=6), ft.Text("Informações do Técnico", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]), ft.Container(content=ft.Text("*", color=CORES["erro"], size=16), tooltip="Campo obrigatório")], spacing=10),
                    ft.Divider(height=1, color=CORES["borda"]),
                    ft.Container(height=5),
                    campos["txt_num_tecnico"],
                    campos["txt_nome_tecnico"]
                ], spacing=12), bgcolor=CORES["card"], padding=20, border_radius=12, border=ft.border.all(1, CORES["borda"]), expand=1)
            ], spacing=15),

            # Seção Detalhes do Processo
            ft.Container(content=ft.Column([
                ft.Row([ft.Container(content=ft.Icon(ft.Icons.ARTICLE, color=ft.Colors.WHITE, size=18), bgcolor=CORES["azul_escuro"], padding=6, border_radius=6), ft.Text("Detalhes do Processo", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]), ft.Container(content=ft.Text("*", color=CORES["erro"], size=16), tooltip="Campos obrigatórios")], spacing=10),
                ft.Divider(height=1, color=CORES["borda"]),
                ft.Container(height=5),
                ft.Row([ft.Container(content=campos["dropdown_estadosprocesso"], expand=1), ft.Container(content=campos["btn_selecionar_data"], expand=1)], spacing=15),
                campos["dropdown_problematica"],
                campos["txt_descricao"]
            ], spacing=12), bgcolor=CORES["card"], padding=20, border_radius=12, border=ft.border.all(1, CORES["borda"])),

            # Botões
            ft.Container(content=ft.Row([btn_cancelar, btn_salvar], alignment=ft.MainAxisAlignment.END, spacing=15), padding=ft.padding.only(top=10))
        ], spacing=20),
        bgcolor=CORES["card"],
        padding=35,
        border_radius=16,
        border=ft.border.all(1, CORES["borda"]),
        width=1100,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.15, CORES["primaria"]))
    )
    #  CAMPOS — Nº PROCESSO ALUNO + ALUNO AUTOMÁTICO
    # -----------------------------------------------------------
 
    txt_num_processo = ft.TextField(
        label="Número de Processo",
        hint_text="Ex: 12345",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.NUMBERS,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    txt_nome_aluno = ft.TextField(
        label="Nome do Aluno",
        read_only=True,
        border_color=cor_borda,
        prefix_icon=ft.Icons.PERSON,
        text_size=15,
        color=cor_secundaria,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    def preencher_nome_aluno(e=None):
        nproc = txt_num_processo.value.strip()
 
        if nproc.isdigit():
            aluno = next((a for a in alunos if str(a["nProcessoAluno"]) == nproc), None)
            if aluno:
                txt_nome_aluno.value = aluno["NomeAluno"]
                txt_nome_aluno.border_color = cor_sucesso
            else:
                txt_nome_aluno.value = "⚠ Aluno não encontrado"
                txt_nome_aluno.border_color = cor_erro
        else:
            txt_nome_aluno.value = ""
            txt_nome_aluno.border_color = cor_borda
 
        page.update()
 
    txt_num_processo.on_change = preencher_nome_aluno
 
    # -----------------------------------------------------------
    #  CAMPOS — Nº PROCESSO TÉCNICO + TÉCNICO AUTOMÁTICO
    # -----------------------------------------------------------
 
    txt_num_tecnico = ft.TextField(
        label="Número de Processo",
        hint_text="Ex: 67890",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.BADGE,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    txt_nome_tecnico = ft.TextField(
        label="Nome do Técnico",
        read_only=True,
        border_color=cor_borda,
        prefix_icon=ft.Icons.PERSON_SEARCH,
        text_size=15,
        color=cor_secundaria,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    def preencher_nome_tecnico(e=None):
        nproc = txt_num_tecnico.value.strip()
 
        if nproc.isdigit():
            tecnico = next((t for t in tecnicos if str(t["nProcTecnico"]) == nproc), None)
            if tecnico:
                txt_nome_tecnico.value = tecnico["NomeTecnico"]
                txt_nome_tecnico.border_color = cor_sucesso
            else:
                txt_nome_tecnico.value = "⚠ Técnico não encontrado"
                txt_nome_tecnico.border_color = cor_erro
        else:
            txt_nome_tecnico.value = ""
            txt_nome_tecnico.border_color = cor_borda
 
        page.update()
 
    txt_num_tecnico.on_change = preencher_nome_tecnico
 
    # -----------------------------------------------------------
    #  DROPDOWN ESTADOS (BLOQUEADO EM "A AGUARDAR")
    # -----------------------------------------------------------
 
    # Procurar o estado "A Aguardar" e definir como padrão
    estado_aguardar = next((e for e in estados if e["Estado"].lower() == "a aguardar"), None)
    estado_aguardar_id = str(estado_aguardar["idEstado"]) if estado_aguardar else None
 
    dropdown_estadosprocesso = ft.Dropdown(
        label="Estado do Processo",
        value=estado_aguardar_id,  # Define o valor padrão
        disabled=True,  # Bloqueado
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.FLAG,
        options=[ft.dropdown.Option(key=str(e["idEstado"]), text=e["Estado"]) for e in estados]
                if estados else [ft.dropdown.Option("0", "Nenhum estado disponível")],
        text_size=15,
        color=cor_texto_medio,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    # -----------------------------------------------------------
    #  DROPDOWN PROBLEMÁTICAS (DA BASE DE DADOS)
    # -----------------------------------------------------------
 
    dropdown_problematica = ft.Dropdown(
        label="Problemática",
        hint_text="Selecione a problemática",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.BUG_REPORT,
        options=[ft.dropdown.Option(key=str(p["idProblematica"]), text=p["TipoProblematica"]) 
                 for p in problematicas] if problematicas else [ft.dropdown.Option("0", "Nenhuma problemática")],
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        border_radius=8,
    )
 
    # -----------------------------------------------------------
    #  CALENDÁRIO
    # -----------------------------------------------------------
 
    data_registo = {"valor": None, "display": "Selecionar Data"}
 
    def abrir_calendario(e):
        def ao_selecionar_data(e):
            if date_picker.value:
                data_registo["valor"] = date_picker.value.strftime("%Y-%m-%d")
               
                meses_pt = {
                    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
                }
               
                data_obj = date_picker.value
                data_registo["display"] = f"{data_obj.day} de {meses_pt[data_obj.month]} de {data_obj.year}"
               
                btn_selecionar_data.content.controls[0] = ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=cor_sucesso)
                btn_selecionar_data.content.controls[1] = ft.Text(data_registo["display"], size=15, color=cor_texto_claro, weight=ft.FontWeight.W_500)
                btn_selecionar_data.border = ft.border.all(1, cor_sucesso)
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
        border_radius=8,
        border=ft.border.all(1, cor_borda),
        on_click=abrir_calendario,
        ink=True,
        animate=ft.Animation(200, "easeOut"),
    )
 
    txt_descricao = ft.TextField(
        label="Observações",
        hint_text="Adicione observações adicionais (opcional)",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.DESCRIPTION,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio, size=13),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        multiline=True,
        min_lines=3,
        max_lines=5,
        border_radius=8,
    )
 
    mensagem_feedback = ft.Container(visible=False)
 
    # ======================= SALVAR ==========================
 
    def salvar_registo(e):
        erros = []
 
        if not txt_num_processo.value.strip():
            erros.append("• Número de processo do aluno é obrigatório")
        if txt_nome_aluno.value in ["", "⚠ Aluno não encontrado"]:
            erros.append("• Número de processo do aluno inválido")
 
        if not txt_num_tecnico.value.strip():
            erros.append("• Número de processo do técnico é obrigatório")
        if txt_nome_tecnico.value in ["", "⚠ Técnico não encontrado"]:
            erros.append("• Número de processo do técnico inválido")
 
        if not dropdown_estadosprocesso.value:
            erros.append("• Estado do processo é obrigatório")
 
        if not data_registo["valor"]:
            erros.append("• Data é obrigatória")
 
        if not dropdown_problematica.value:
            erros.append("• Problemática é obrigatória")
 
        if erros:
            mensagem_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=cor_erro, size=20),
                        ft.Text("Erros de validação:", size=14, weight=ft.FontWeight.BOLD, color=cor_erro),
                    ], spacing=8),
                    ft.Text("\n".join(erros), color=cor_texto_claro, size=13),
                ], spacing=8),
                bgcolor="#2D1515",
                padding=15,
                border_radius=8,
                border=ft.border.all(2, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()
            return
 
        try:
            # Buscar a problemática selecionada
            prob_selecionada = next((p for p in problematicas if str(p["idProblematica"]) == dropdown_problematica.value), None)
            tipo_problematica = prob_selecionada["TipoProblematica"] if prob_selecionada else None
 
            sucesso = criarRegisto(
                nProcessoAluno=txt_num_processo.value.strip(),
                idEstado=int(dropdown_estadosprocesso.value),
                DataArquivo=data_registo["valor"],
                Observacoes=txt_descricao.value.strip() or None,
                nProcTecnico=txt_num_tecnico.value.strip(),
                tipoProblematica=tipo_problematica
            )
 
            if sucesso:
                mensagem_feedback.content = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=cor_sucesso, size=20),
                        ft.Text("Registo criado com sucesso!", size=14, weight=ft.FontWeight.BOLD, color=cor_sucesso),
                    ], spacing=8),
                    bgcolor="#0F2A1A",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(2, cor_sucesso),
                )
                mensagem_feedback.visible = True
                page.update()
                import time
                time.sleep(1.5)
                page.go("/pagina-principal")
 
        except Exception as ex:
            mensagem_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                        ft.Text("Erro ao criar registo:", size=14, weight=ft.FontWeight.BOLD, color=cor_erro),
                    ], spacing=8),
                    ft.Text(str(ex), color=cor_texto_claro, size=13),
                ], spacing=8),
                bgcolor="#2D1515",
                padding=15,
                border_radius=8,
                border=ft.border.all(2, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()
 
    # ======================= BOTÕES ==========================
 
    btn_salvar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SAVE, size=20),
                ft.Text("Guardar Registo", size=16, weight=ft.FontWeight.BOLD),
            ],
            tight=True,
            spacing=10,
        ),
        bgcolor=cor_primaria,
        color=ft.Colors.WHITE,
        on_click=salvar_registo,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            elevation=3,
        ),
        height=50,
    )
 
    btn_cancelar = ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CLOSE, size=20),
                ft.Text("Cancelar", size=16),
            ],
            tight=True,
            spacing=10,
        ),
        on_click=lambda e: page.go("/pagina-principal"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            side=ft.BorderSide(2, cor_borda),
            color=cor_texto_claro,
        ),
        height=50,
    )
 
    # ======================= CABEÇALHO ==========================
 
    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=ft.Colors.WHITE, size=28),
                            bgcolor=cor_primaria,
                            padding=10,
                            border_radius=10,
                        ),
                        ft.Column(
                            [
                                ft.Text("Sistema SPO", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Text("Gestão de Processos", size=12, color=cor_texto_medio),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=20),
                            ft.Text(tecnico_nome, size=15, color=cor_texto_claro, weight=ft.FontWeight.W_500),
                        ],
                        spacing=8,
                    ),
                    bgcolor=cor_fundo,
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    border_radius=8,
                    border=ft.border.all(1, cor_borda),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=12,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, "#000000"),
        ),
    )
 
    # ======================= FORMULÁRIO ==========================
 
    formulario = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=cor_primaria,
                            icon_size=24,
                            on_click=lambda e: page.go("/pagina-principal"),
                            tooltip="Voltar",
                            bgcolor=cor_fundo,
                            style=ft.ButtonStyle(shape=ft.CircleBorder()),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Criar Novo Registo",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Preencha todos os campos obrigatórios para registar um novo processo",
                                    size=14,
                                    color=cor_texto_medio,
                                ),
                            ],
                            spacing=4,
                        ),
                    ]),
                    padding=ft.padding.only(bottom=20),
                ),
 
                mensagem_feedback,
 
                # Linha com Aluno e Técnico lado a lado
                ft.Row(
                    [
                        # Seção Aluno
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=18),
                                            bgcolor=cor_primaria,
                                            padding=6,
                                            border_radius=6,
                                        ),
                                        ft.Text("Informações do Aluno", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                        ft.Container(
                                            content=ft.Text("*", color=cor_erro, size=16),
                                            tooltip="Campo obrigatório",
                                        ),
                                    ], spacing=10),
                                    ft.Divider(height=1, color=cor_borda),
                                    ft.Container(height=5),
                                    txt_num_processo,
                                    txt_nome_aluno,
                                ],
                                spacing=12
                            ),
                            bgcolor=cor_card,
                            padding=20,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
 
                        # Seção Técnico
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.ENGINEERING, color=ft.Colors.WHITE, size=18),
                                            bgcolor=cor_secundaria,
                                            padding=6,
                                            border_radius=6,
                                        ),
                                        ft.Text("Informações do Técnico", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                        ft.Container(
                                            content=ft.Text("*", color=cor_erro, size=16),
                                            tooltip="Campo obrigatório",
                                        ),
                                    ], spacing=10),
                                    ft.Divider(height=1, color=cor_borda),
                                    ft.Container(height=5),
                                    txt_num_tecnico,
                                    txt_nome_tecnico,
                                ],
                                spacing=12
                            ),
                            bgcolor=cor_card,
                            padding=20,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
                    ],
                    spacing=15,
                ),
 
                # Seção Detalhes do Processo
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ARTICLE, color=ft.Colors.WHITE, size=18),
                                    bgcolor=cor_azul_escuro,
                                    padding=6,
                                    border_radius=6,
                                ),
                                ft.Text("Detalhes do Processo", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Container(
                                    content=ft.Text("*", color=cor_erro, size=16),
                                    tooltip="Campos obrigatórios",
                                ),
                            ], spacing=10),
                            ft.Divider(height=1, color=cor_borda),
                            ft.Container(height=5),
                            
                            # Estado e Data
                            ft.Row([
                                ft.Container(content=dropdown_estadosprocesso, expand=1),
                                ft.Container(content=btn_selecionar_data, expand=1),
                            ], spacing=15),
                            
                            # Problemática
                            dropdown_problematica,
                            
                            # Observações
                            txt_descricao,
                        ],
                        spacing=12
                    ),
                    bgcolor=cor_card,
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, cor_borda),
                ),
 
                # Botões
                ft.Container(
                    content=ft.Row(
                        [btn_cancelar, btn_salvar],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=15,
                    ),
                    padding=ft.padding.only(top=10),
                ),
            ],
            spacing=20,
        ),
        bgcolor=cor_card,
        padding=35,
        border_radius=16,
        border=ft.border.all(1, cor_borda),
        width=1100,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.15, cor_primaria),
        ),
    )
 
    return ft.View(
        route="/CriarRegisto",
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(
                        content=formulario,
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        bgcolor=cor_fundo,
        padding=25,
    )