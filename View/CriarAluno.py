import flet as ft
from Models.AlunosModel import criarAluno
from Models.EscolasModel import listarEscolas  

def PaginaCriarAluno(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"
    
    def LimitarNumero(e):
     valor = ''.join(filter(str.isdigit, e.control.value))  
     if len(valor) > 10:  
        valor = valor[:10]  
     e.control.value = valor
     page.update()
    
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
    
    # === CAMPOS DO FORMULÁRIO ===
    txt_numero_processo = ft.TextField(
        label="Número de Processo",
        hint_text="Ex: 2024001",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.NUMBERS,
        text_size=15,
        color="#000000",
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
        color="#000000",
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
        color="#000000",
    )
    
    txt_turma = ft.TextField(
        label="Turma",
        hint_text="Ex: A, B, C...",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.MEETING_ROOM,
        text_size=15,
        max_length=3,
        color="#000000",
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
            ft.dropdown.Option(key=str(escola.get("IdEscola")), text=escola.get("NomeEscola", "")) 
            for escola in escolas
        ] if escolas else [ft.dropdown.Option("0", "Nenhuma escola disponível")],
        text_size=15,
        color="#000000",
    )
    
    # Mensagem de feedback
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
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                                ft.Text("Erros no formulário:", size=15, weight=ft.FontWeight.BOLD, color=cor_erro),
                            ],
                            spacing=10,
                        ),
                        ft.Column(
                            [ft.Text(f"• {erro}", size=13, color=cor_erro) for erro in erros],
                            spacing=5,
                        ),
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
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=cor_sucesso, size=24),
                            ft.Text("Aluno criado com sucesso!", size=15, weight=ft.FontWeight.BOLD, color=cor_sucesso),
                        ],
                        spacing=12,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.1, cor_sucesso),
                    border=ft.border.all(1, cor_sucesso),
                    border_radius=12,
                    padding=16,
                )
                mensagem_feedback.visible = True
                page.update()
                
                # Redirecionar após 1.5 segundos
                import time
                time.sleep(1.5),
                page.go("/pagina-principal"),
            else:
                raise Exception("Erro ao criar aluno")
                
        except Exception as ex:
            mensagem_feedback.content = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                        ft.Text(f"Erro ao criar aluno: {str(ex)}", size=14, color=cor_erro),
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
    
    # === BOTÕES ===
    btn_salvar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SAVE, size=20),
                ft.Text("Guardar Aluno", size=15, weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
        ),
        bgcolor=cor_primaria,
        color=ft.Colors.WHITE,
        on_click=salvar_aluno,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.symmetric(horizontal=28, vertical=18),
        ),
    )
    
    btn_cancelar = ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CANCEL, size=20, color=cor_texto_medio),
                ft.Text("Voltar", size=15, weight=ft.FontWeight.W_600, color=cor_texto_medio),
            ],
            spacing=8,
        ),
        on_click=lambda e: page.go("/pagina-principal"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.symmetric(horizontal=28, vertical=18),
            side=ft.BorderSide(1, cor_borda),
        ),
    )
    
    # === FORMULÁRIO ===
    formulario = ft.Container(
        content=ft.Column(
            [
                # Cabeçalho
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=cor_primaria,
                            icon_size=28,
                            on_click=lambda e: page.go("/pagina-principal"),
                            tooltip="Voltar",
                        ),
                        ft.Column(
                            [
                                ft.Text("Criar Novo Aluno", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                ft.Text("Preencha os dados do aluno", size=14, color=cor_texto_claro),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Divider(height=30, color=cor_borda),
                
                # Mensagem de feedback
                mensagem_feedback,
                
                # Campos do formulário
                ft.Container(
                    content=ft.Column(
                        [
                            txt_numero_processo,
                            txt_nome,
                            ft.Row(
                                [txt_ano, txt_turma],
                                spacing=15,
                            ),
                            dropdown_escola,
                        ],
                        spacing=20,
                    ),
                    padding=ft.padding.only(top=10, bottom=20),
                ),
                
                # Botões
                ft.Row(
                    [btn_cancelar, btn_salvar],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=15,
        ),
        bgcolor=cor_card,
        padding=40,
        border_radius=16,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)),
        width=700,
    )
    
    # === CONTEÚDO PRINCIPAL ===
    conteudo_principal = ft.Container(
        content=ft.Column(
            [formulario],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=cor_fundo,
        padding=40,
        alignment=ft.alignment.center,
        expand=True,
    )
    
    return ft.View(
        route="/CriarAluno",
        controls=[conteudo_principal],
        bgcolor=cor_fundo,
    )