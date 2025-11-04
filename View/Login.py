import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import listarTecnico

def LoginView(page: ft.Page):
    # Animação Lottie de Login
    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        animate=True,
        width=150,
        height=150,
    )

    # Campos de entrada para número do processo e nome do técnico
    campoNumeroProcesso = ft.TextField(
        label="Nº Processo Técnico", 
        prefix_icon=ft.Icons.BADGE, 
        width=350, 
        autofocus=True,
        border_color="#4CAF50",  # Verde para o campo
        focused_border_color="#1E40AF",  # Azul no foco
        hint_text="Digite o número do processo"
    )
    campoNomeTecnico = ft.TextField(
        label="Nome do Técnico", 
        prefix_icon=ft.Icons.PERSON, 
        width=350, 
        border_color="#4CAF50", 
        focused_border_color="#1E40AF",  # Azul no foco
        hint_text="Digite o nome do técnico"
    )

    # Mensagem de erro
    mensagemErro = ft.Text(color=ft.Colors.RED, size=16)

    # Botão para criar técnico (inicialmente invisível)
    botaoCriar = ft.ElevatedButton(
        "Criar Técnico", 
        visible=False, 
        on_click=lambda e: page.go("/criar-tecnico"),
        bgcolor="#4CAF50",  # Verde claro
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))  # Bordas arredondadas
    )

    # Função de autenticação
    def autenticar(e):
        nProc = campoNumeroProcesso.value.strip()
        nome = campoNomeTecnico.value.strip()

        if not nProc or not nome:
            mensagemErro.value = "Preencha ambos os campos!"
            page.update()
            return

        tecnicos = listarTecnico()
        tecnicoExiste = any(
            str(t.get("nProcTecnico", "")).strip() == str(nProc).strip()
            and t.get("NomeTecnico", "").strip().lower() == nome.strip().lower()
            for t in tecnicos
        )

        if tecnicoExiste:
            page.session.set("tecnico_nome", nome)
            page.go("/pagina-principal")
        else:
            mensagemErro.value = "Técnico não encontrado! Deseja criar um novo?"
            botaoCriar.visible = True
            page.update()

    # Botão de login
    botaoEntrar = ft.ElevatedButton(
        "Entrar", 
        on_click=autenticar, 
        bgcolor="#1E40AF",  # Azul escuro
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))  # Bordas arredondadas
    )

    # Organizar os botões de login
    botoesLogin = ft.Row(
        [botaoEntrar, botaoCriar], 
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=20
    )

    caixaLogin = ft.Container(
        width=450,
        height=500,
        padding=50,
        bgcolor=ft.Colors.WHITE  # Usando a constante de cor branca do Flet
,  # Fundo branco sólido
        border_radius=25,  # Bordas arredondadas
        content=ft.Column(
            [
                animacaoLottie,
                ft.Text("Login", size=26, weight=ft.FontWeight.BOLD, color="#000103"),
                campoNumeroProcesso,
                campoNomeTecnico,
                botoesLogin,
                mensagemErro,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        ),
    )

    # Imagem do lado direito (a animação está em uma posição mais visível)
    imagemPsico = fl.Lottie(
        src="https://lottie.host/3ca3724a-1dd4-41d0-8783-b409dabecb3d/TMc5F1aZeS.json",
        animate=True,
        width=600,  # Aumentando a largura da animação
        height=450,
    )

    # Layout principal com duas colunas (caixa de login e animação do lado direito)
    layoutPrincipal = ft.Row(
        [
            ft.Container(content=caixaLogin, expand=1, alignment=ft.alignment.center),
            ft.Container(content=imagemPsico, expand=1, alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,  # Diminuí o espaçamento para dar mais espaço para a imagem
    )

    # Fundo com gradiente moderno (fundo azul suave)
    fundoComGradiente = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#3B82F6", "#60A5FA", "#93C5FD"],  # Gradiente de azuis
        ),
        content=layoutPrincipal,
    )

    # Retorna a view com fundo gradiente e os controles
    return ft.View(route="/login", controls=[fundoComGradiente])
