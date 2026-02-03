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
    cabecalho = criar_cabecalho(tecnico_nome, page)
    formulario = criar_formulario(campos, btn_salvar, btn_cancelar, page)

    return ft.View(
        route="/CriarRegisto",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        cabecalho,
                        formulario,
                    ],
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.top_center,
                expand=True,
            )
        ],
        bgcolor=CORES["fundo"],
        padding=30,
        scroll=ft.ScrollMode.AUTO,
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
    txt_descricao = criar_text_field("Observações", "Adicione observações adicionais (opcional)", ft.Icons.DESCRIPTION, multiline=True, min_lines=4, max_lines=6)

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
        text_size=14,
        color=CORES["texto_claro"],
        label_style=ft.TextStyle(color=CORES["texto_medio"], size=13),
        hint_style=ft.TextStyle(color=CORES["texto_medio"]),
        bgcolor=CORES["card"],
        filled=True,
        border_radius=10,
        read_only=read_only,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=max_lines,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

def estilo_dropdown():
    """
    Retorna o estilo padrão para dropdowns.
    """
    return {
        "border_color": CORES["borda"],
        "focused_border_color": CORES["primaria"],
        "text_size": 14,
        "color": CORES["texto_claro"],
        "label_style": ft.TextStyle(color=CORES["texto_medio"], size=13),
        "hint_style": ft.TextStyle(color=CORES["texto_medio"]),
        "bgcolor": CORES["card"],
        "filled": True,
        "border_radius": 10,
        "content_padding": ft.padding.symmetric(horizontal=16, vertical=14),
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
                btn_selecionar_data.content.controls[1] = ft.Text(data_registo["display"], size=14, color=CORES["texto_claro"], weight=ft.FontWeight.W_500)
                btn_selecionar_data.border = ft.border.all(1.5, CORES["sucesso"])
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
            ft.Text("Selecionar Data", size=14, color=CORES["texto_medio"])
        ], spacing=10),
        bgcolor=CORES["card"],
        padding=16,
        border_radius=10,
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
        content=ft.Row([
            ft.Icon(ft.Icons.SAVE, size=20),
            ft.Text("Guardar Registo", size=15, weight=ft.FontWeight.BOLD)
        ], tight=True, spacing=10),
        bgcolor=CORES["primaria"],
        color=ft.Colors.WHITE,
        on_click=salvar_registo,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=32, vertical=18),
            elevation=2,
        ),
        height=54,
    )

    btn_cancelar = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.CLOSE, size=20),
            ft.Text("Cancelar", size=15)
        ], tight=True, spacing=10),
        on_click=lambda e: page.go("/pagina-principal"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=32, vertical=18),
            side=ft.BorderSide(1.5, CORES["borda"]),
            color=CORES["texto_claro"],
        ),
        height=54,
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
            ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=CORES["erro"], size=22),
                ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD, color=CORES["erro"])
            ], spacing=10),
            ft.Container(height=8),
            ft.Text("\n".join(erros), color=CORES["texto_claro"], size=13)
        ], spacing=0),
        bgcolor="#2D1515",
        padding=20,
        border_radius=12,
        border=ft.border.all(2, CORES["erro"])
    )
    container.visible = True
    page.update()

def mostrar_mensagem_sucesso(container, page):
    """
    Exibe mensagem de sucesso no container.
    """
    container.content = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=CORES["sucesso"], size=22),
            ft.Text("Registo criado com sucesso!", size=15, weight=ft.FontWeight.BOLD, color=CORES["sucesso"])
        ], spacing=10),
        bgcolor="#0F2A1A",
        padding=20,
        border_radius=12,
        border=ft.border.all(2, CORES["sucesso"])
    )
    container.visible = True
    page.update()

def criar_cabecalho(tecnico_nome, page):
    """
    Cria o cabeçalho da página.
    """
    return ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=ft.Colors.WHITE, size=28),
                    bgcolor=CORES["primaria"],
                    padding=12,
                    border_radius=12,
                ),
                ft.Column([
                    ft.Text("Sistema SPO", size=22, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]),
                    ft.Text("Gestão de Processos", size=13, color=CORES["texto_medio"])
                ], spacing=2)
            ], spacing=14),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON, color=CORES["primaria"], size=20),
                    ft.Text(tecnico_nome, size=14, color=CORES["texto_claro"], weight=ft.FontWeight.W_500)
                ], spacing=10),
                bgcolor=CORES["fundo"],
                padding=ft.padding.symmetric(horizontal=18, vertical=12),
                border_radius=10,
                border=ft.border.all(1, CORES["borda"])
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=CORES["card"],
        padding=24,
        border_radius=14,
        border=ft.border.all(1, CORES["borda"]),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, "#000000"),
            offset=ft.Offset(0, 4)
        ),
    )

def criar_formulario(campos, btn_salvar, btn_cancelar, page):
    """
    Cria o formulário principal.
    """
    return ft.Container(
        content=ft.Column([
            # Título do formulário com botão voltar
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=CORES["primaria"],
                        icon_size=24,
                        on_click=lambda e: page.go("/pagina-principal"),
                        tooltip="Voltar",
                        style=ft.ButtonStyle(
                            bgcolor=CORES["fundo"],
                            shape=ft.CircleBorder(),
                        ),
                    ),
                    ft.Column([
                        ft.Text(
                            "Criar Novo Registo",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=CORES["texto_claro"],
                        ),
                        ft.Text(
                            "Preencha todos os campos obrigatórios para registar um novo processo",
                            size=13,
                            color=CORES["texto_medio"],
                        ),
                    ], spacing=6),
                ], spacing=12),
                padding=ft.padding.only(bottom=28),
            ),

            # Mensagem de feedback
            campos["mensagem_feedback"],

            # Linha com Aluno e Técnico lado a lado
            ft.Row([
                # Seção Informações do Aluno
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=18),
                                bgcolor=CORES["primaria"],
                                padding=8,
                                border_radius=8,
                            ),
                            ft.Text("Informações do Aluno", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]),
                            ft.Container(
                                content=ft.Text("*", color=CORES["erro"], size=16, weight=ft.FontWeight.BOLD),
                                tooltip="Campo obrigatório",
                            ),
                        ], spacing=10),
                        
                        ft.Divider(height=1, color=CORES["borda"], thickness=1),
                        
                        ft.Container(height=6),
                        
                        campos["txt_num_processo"],
                        ft.Container(height=4),
                        campos["txt_nome_aluno"],
                    ], spacing=14),
                    bgcolor=CORES["card"],
                    padding=24,
                    border_radius=14,
                    border=ft.border.all(1, CORES["borda"]),
                    expand=1,
                ),

                # Seção Informações do Técnico
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.ENGINEERING, color=ft.Colors.WHITE, size=18),
                                bgcolor=CORES["secundaria"],
                                padding=8,
                                border_radius=8,
                            ),
                            ft.Text("Informações do Técnico", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]),
                            ft.Container(
                                content=ft.Text("*", color=CORES["erro"], size=16, weight=ft.FontWeight.BOLD),
                                tooltip="Campo obrigatório",
                            ),
                        ], spacing=10),
                        
                        ft.Divider(height=1, color=CORES["borda"], thickness=1),
                        
                        ft.Container(height=6),
                        
                        campos["txt_num_tecnico"],
                        ft.Container(height=4),
                        campos["txt_nome_tecnico"],
                    ], spacing=14),
                    bgcolor=CORES["card"],
                    padding=24,
                    border_radius=14,
                    border=ft.border.all(1, CORES["borda"]),
                    expand=1,
                ),
            ], spacing=16),

            ft.Container(height=8),

            # Seção Detalhes do Processo
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.ARTICLE, color=ft.Colors.WHITE, size=18),
                            bgcolor=CORES["azul_escuro"],
                            padding=8,
                            border_radius=8,
                        ),
                        ft.Text("Detalhes do Processo", size=16, weight=ft.FontWeight.BOLD, color=CORES["texto_claro"]),
                        ft.Container(
                            content=ft.Text("*", color=CORES["erro"], size=16, weight=ft.FontWeight.BOLD),
                            tooltip="Campos obrigatórios",
                        ),
                    ], spacing=10),
                    
                    ft.Divider(height=1, color=CORES["borda"], thickness=1),
                    
                    ft.Container(height=6),
                    
                    # Estado e Data lado a lado
                    ft.Row([
                        ft.Container(content=campos["dropdown_estadosprocesso"], expand=1),
                        ft.Container(content=campos["btn_selecionar_data"], expand=1),
                    ], spacing=16),
                    
                    ft.Container(height=4),
                    
                    # Problemática
                    campos["dropdown_problematica"],
                    
                    ft.Container(height=4),
                    
                    # Observações
                    campos["txt_descricao"],
                ], spacing=14),
                bgcolor=CORES["card"],
                padding=24,
                border_radius=14,
                border=ft.border.all(1, CORES["borda"]),
            ),

            ft.Container(height=16),

            # Botões de ação
            ft.Row(
                [btn_cancelar, btn_salvar],
                alignment=ft.MainAxisAlignment.END,
                spacing=16,
            ),
        ], spacing=20),
        bgcolor=CORES["card"],
        padding=36,
        border_radius=16,
        border=ft.border.all(1, CORES["borda"]),
        width=1000,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=25,
            color=ft.Colors.with_opacity(0.15, CORES["primaria"]),
            offset=ft.Offset(0, 8)
        ),
    )