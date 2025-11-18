import flet as ft
from Models.AlunosModel import *
from Models.EscolasModel import listarEscolas  

def PaginaEditarAluno(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"
    
    # === OBTER ALUNO PARA EDITAR ===
    nProcessoAluno = page.session.get("aluno_editar_id")
    if not nProcessoAluno:
        page.go("/pagina-principal")
        return
    
    aluno = buscarAlunoPorProcesso(nProcessoAluno)
    if not aluno:
        page.go("/pagina-principal")
        return
    
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
        value=aluno["nProcessoAluno"],
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.NUMBERS,
        text_size=15,
        read_only=True,
        color="#000000",
    )
    
    txt_nome = ft.TextField(
        label="Nome Completo do Aluno",
        value=aluno["NomeAluno"],
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.PERSON,
        text_size=15,
        color="#000000",
    )
    
    txt_ano = ft.Dropdown(
        label="Ano Escolar",
        value=str(aluno["Ano"]),
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.SCHOOL,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],
        text_size=15,
        color="#000000",
    )
    
    txt_turma = ft.TextField(
        label="Turma",
        value=aluno["Turma"],
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.MEETING_ROOM,
        text_size=15,
        max_length=3,
        color="#000000",
    )
    
    # Carregar Escolas
    try:
        escolas = listarEscolas()
    except:
        escolas = []
    
    dropdown_escola = ft.Dropdown(
        label="Escola",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.LOCATION_CITY,
        options=[
            ft.dropdown.Option(key=str(e["idEscola"]), text=e["NomeEscola"])
            for e in escolas
        ] if escolas else [ft.dropdown.Option("0", "Nenhuma escola disponível")],
        text_size=15,
        color="#000000",
    )
    
    dropdown_escola.value = str(aluno["idEscola"])
    
    mensagem_feedback = ft.Container(visible=False)
    
    # === FUNÇÃO PARA ATUALIZAR ===
    def atualizar_aluno(e):
        erros = []
        
        if not txt_nome.value.strip():
            erros.append("Nome do aluno é obrigatório")
        if not txt_ano.value:
            erros.append("Ano escolar é obrigatório")
        if not txt_turma.value.strip():
            erros.append("Turma é obrigatória")
        if not dropdown_escola.value or dropdown_escola.value == "0":
            erros.append("Escola é obrigatória")

        if erros:
            mensagem_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                        ft.Text("Erros no formulário:", size=15, weight=ft.FontWeight.BOLD, color=cor_erro),
                    ]),
                    ft.Column([ft.Text(f"• {erro}", size=13, color=cor_erro) for erro in erros])
                ]),
                bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
                border=ft.border.all(1, cor_erro),
                border_radius=12,
                padding=16,
            )
            mensagem_feedback.visible = True
            page.update()
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
                mensagem_feedback.content = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=cor_sucesso, size=24),
                        ft.Text("Aluno atualizado com sucesso!", size=15, weight=ft.FontWeight.BOLD, color=cor_sucesso),
                    ]),
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
                return
            
            else:
                raise Exception("Nenhuma alteração foi realizada.")
        
        except Exception as ex:
            mensagem_feedback.content = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color=cor_erro, size=20),
                    ft.Text(f"Erro ao atualizar aluno: {str(ex)}", size=14, color=cor_erro),
                ]),
                bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
                border=ft.border.all(1, cor_erro),
                border_radius=12,
                padding=16,
            )
            mensagem_feedback.visible = True
            page.update()
    
    # === BOTÕES ===
    btn_salvar = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.SAVE, size=20),
            ft.Text("Atualizar Aluno", size=15, weight=ft.FontWeight.BOLD),
        ]),
        bgcolor=cor_primaria,
        color=ft.Colors.WHITE,
        on_click=atualizar_aluno,
    )
    
    btn_cancelar = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.CANCEL, size=20, color=cor_texto_medio),
            ft.Text("Voltar", size=15, weight=ft.FontWeight.W_600, color=cor_texto_medio),
        ]),
        on_click=lambda e: page.go("/pagina-principal"),
    )
    
    formulario = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=cor_primaria,
                    on_click=lambda e: page.go("/pagina-principal"),
                ),
                ft.Column([
                    ft.Text("Editar Aluno", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Editando: {aluno['NomeAluno']}", size=14, color=cor_texto_claro)
                ], expand=True),
            ]),
            ft.Divider(height=30, color=cor_borda),
            mensagem_feedback,
            txt_numero_processo,
            txt_nome,
            ft.Row([txt_ano, txt_turma], spacing=15),
            dropdown_escola,
            ft.Row([btn_cancelar, btn_salvar], alignment=ft.MainAxisAlignment.END),
        ]),
        bgcolor=cor_card,
        padding=40,
        width=700,
        border_radius=16,
    )
    
    return ft.View(
        route="/editar-aluno",
        controls=[ft.Container(
            content=ft.Column([formulario], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=cor_fundo,
            padding=40,
            expand=True,
        )],
        bgcolor=cor_fundo,
    )
