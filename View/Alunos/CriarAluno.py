import flet as ft
from Models.AlunosModel import criarAluno
from Models.EscolasModel import listarEscolas  

def PaginaCriarAluno(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    # === CORES (do estilos.py) ===
    cor_primaria = "#6EA8FE"        # azul suave
    cor_secundaria = "#9B8CFF"      # lilás leve
    cor_fundo = "#0E1628"           # dark azulado
    cor_card = "#16213E"            # card com tom azul
    cor_texto_claro = "#E6EBFF"
    cor_texto_medio = "#A5B4D6"
    cor_texto_escuro = "#8A94B8"
    cor_borda = "#23325C"
    cor_sucesso = "#10B981"
    cor_erro = "#DC2626"

    def LimitarNumero(e):
        valor = ''.join(filter(str.isdigit, e.control.value))  
        if len(valor) > 10:  
            valor = valor[:10]  
        e.control.value = valor
        page.update()
    
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

    # === CAMPOS DO FORMULÁRIO ===
    txt_numero_processo = ft.TextField(
        label="Número de Processo",
        hint_text="Ex: 2024001",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.NUMBERS,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
        autofocus=True,
        on_change=LimitarNumero,
    )
    
    txt_nome = ft.TextField(
        label="Nome Completo do Aluno",
        hint_text="Ex: João Silva",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.PERSON,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )
    
    txt_ano = ft.Dropdown(
        label="Ano Escolar",
        hint_text="Selecione o ano",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.SCHOOL,
        options=[
            ft.dropdown.Option(str(i)) for i in range(1, 13)
        ],
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )
    
    txt_turma = ft.TextField(
        label="Turma",
        hint_text="Ex: A, B, C...",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.MEETING_ROOM,
        text_size=15,
        max_length=3,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )
    
    # Carregar escolas
    escolas = []
    try:
        escolas = listarEscolas()  
    except:
        escolas = []
    
    dropdown_escola = ft.Dropdown(
        label="Escola",
        hint_text="Selecione a escola",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.LOCATION_CITY,
        options=[
            ft.dropdown.Option(key=str(escola.get("idEscola")), text=escola.get("NomeEscola", "")) 
            for escola in escolas
        ] if escolas else [ft.dropdown.Option("0", "Nenhuma escola disponível")],
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )
    
    if escolas:
        dropdown_escola.value = str(escolas[0]["idEscola"])
    
    mensagem_feedback = ft.Container(visible=False)
    
    # === FUNÇÃO PARA SALVAR ===
    def salvar_aluno(e):
        # Validação
        erros = []
        
        if not txt_numero_processo.value or txt_numero_processo.value.strip() == "":
            erros.append("Número de processo é obrigatório")
        
        if not txt_nome.value or txt_nome.value.strip() == "":
            erros.append("Nome do aluno é obrigatório")
        
        if not txt_ano.value:
            erros.append("Ano escolar é obrigatório")
        
        if not txt_turma.value or txt_turma.value.strip() == "":
            erros.append("Turma é obrigatória")
        
        if not dropdown_escola.value or dropdown_escola.value == "0":
            erros.append("Escola é obrigatória")
        
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
        
        # Tentar criar o aluno
        try:
            sucesso = criarAluno(
                nProcessoAluno=txt_numero_processo.value.strip(),
                nomeAluno=txt_nome.value.strip(),
                ano=txt_ano.value,
                turma=txt_turma.value.strip().upper(),
                IdEscola=int(dropdown_escola.value)
            )
            
            if sucesso:
                mensagem_feedback.content = ft.Container(
                    content=ft.Text("✓ Aluno criado com sucesso!", color=cor_sucesso, size=14),
                    bgcolor="#001A0A",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, cor_sucesso),
                )
                mensagem_feedback.visible = True
                page.update()
                
                # Guardar o ID do aluno criado na sessão
                page.session.set("aluno_detalhes_id", txt_numero_processo.value.strip())
                
                # Redirecionar após 1.5 segundos
                import time
                time.sleep(1.5)
                
                # Verificar se é admin ou técnico
                usuario_tipo = page.session.get("usuario_tipo")
                if usuario_tipo == "admin":
                    page.go("/TelaPrincipalAdmin")
                else:
                    page.go("/maisDetalhesAlunos")
            else:
                raise Exception("Erro ao criar aluno")
                
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
                    ft.Text("Guardar Aluno", size=15, weight=ft.FontWeight.BOLD),
                ],
                tight=True,
                spacing=8,
            ),
            bgcolor=cor_primaria,
            color=ft.Colors.WHITE,
            on_click=salvar_aluno,
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
            on_click=lambda e: (
                page.session.set("aluno_detalhes_id", None),
                page.go("/TelaPrincipalAdmin")
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
                side=ft.BorderSide(1, cor_borda),
                color=cor_texto_claro,
            ),
        ),
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
                            on_click=lambda e: (
                                page.session.set("aluno_detalhes_id", None),
                                page.go("/TelaPrincipalAdmin")
                            ),
                            tooltip="Voltar",
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Sistema SPO - Criar Novo Aluno",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Preencha os dados do aluno",
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

                # Linha 1: Número de Processo e Nome
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.NUMBERS, color=cor_primaria, size=18),
                                        ft.Text("Número de Processo", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_numero_processo,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.PERSON, color=cor_secundaria, size=18),
                                        ft.Text("Nome do Aluno", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_nome,
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

                # Linha 2: Ano, Turma e Escola
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.SCHOOL, color=cor_primaria, size=18),
                                        ft.Text("Ano Escolar", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_ano,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.MEETING_ROOM, color=cor_primaria, size=18),
                                        ft.Text("Turma", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    txt_turma,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Icon(ft.Icons.LOCATION_CITY, color=cor_secundaria, size=18),
                                        ft.Text("Escola", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ], spacing=8),
                                    ft.Container(height=5),
                                    dropdown_escola,
                                ],
                                spacing=10
                            ),
                            bgcolor=cor_card,
                            padding=15,
                            border_radius=12,
                            border=ft.border.all(1, cor_borda),
                            expand=2,
                        ),
                    ],
                    spacing=15,
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
        route="/CriarAluno",
        controls=[
            ft.Column(
                [
                    cabecalho,
                    ft.Container(
                        content=formulario,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                spacing=180,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            )
        ],
        bgcolor=cor_fundo,
        padding=20,
    )