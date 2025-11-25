import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import listarTecnico
from datetime import datetime

def LoginView(page: ft.Page):
    page.title = "Login Técnico"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def limitar_numero_processo(e):
     valor = ''.join(filter(str.isdigit, e.control.value)) 
     if len(valor) > 10:  
        valor = valor[:10]  
     e.control.value = valor
     page.update()
    
    def autenticar(e):
        nProc = campoNumeroProcesso.value.strip()
        nome = campoNomeTecnico.value.strip()

        if not nProc or not nome:
            mensagemErro.value = "Preencha ambos os campos!"
            page.update()
            return

        try:
            tecnicos = listarTecnico()
        except Exception as ex:
            mensagemErro.value = f"Erro ao listar técnicos: {ex}"
            page.update()
            return

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
            page.update()

    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        animate=True,
        width=150,
        height=150,
    )

    campoNumeroProcesso = ft.TextField(
        label="Nº Processo Técnico",
        prefix_icon=ft.Icons.BADGE,
        width=350,
        autofocus=True,
        border_color="#000200",
        focused_border_color="#1E40AF",
        hint_text="Digite o número do processo",
        text_style=ft.TextStyle(
            font_family="sans-serif",
            weight=ft.FontWeight.BOLD,
            size=14,
            letter_spacing=0.5,
            color="#000000",
        ),
        border_radius=25,
        on_change=limitar_numero_processo,
    )

    campoNomeTecnico = ft.TextField(
        label="Nome do Técnico",
        prefix_icon=ft.Icons.PERSON,
        width=350,
        border_color="#000200",
        focused_border_color="#1E40AF",
        hint_text="Digite o nome do técnico",
        text_style=ft.TextStyle(
            font_family="sans-serif",
            weight=ft.FontWeight.BOLD,
            size=14,
            letter_spacing=0.5,
            color="#000000",
        ),
        border_radius=25,
    )

    mensagemErro = ft.Text(color=ft.Colors.RED, size=16)

    botaoEntrar = ft.ElevatedButton(
        "Entrar",
        on_click=autenticar, 
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
            bgcolor="#1E40AF",
            color="#FFFFFF",
            text_style=ft.TextStyle(
                font_family="sans-serif",
                weight=ft.FontWeight.BOLD,
                size=16,
                letter_spacing=1.0,
            ),
            elevation=8,
            overlay_color="#2563EB",
        ),
        width=150,
        height=55,
    )

    botoesLogin = ft.Row(
        [botaoEntrar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    caixaLogin = ft.Container(
        width=380,
        height=550,
        padding=40,
        bgcolor="#FFFFFF",
        border_radius=25,
        border=ft.border.all(2, "#1E40AF"),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.with_opacity(0.25, "#1E40AF"),
            spread_radius=1,
        ),
        content=ft.Column(
            [
                animacaoLottie,
                ft.Text("Login", size=28, weight=ft.FontWeight.BOLD, color="#1E40AF"),
                campoNumeroProcesso,
                campoNomeTecnico,
                botoesLogin,
                mensagemErro,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    imagemPsico = fl.Lottie(
        src="https://lottie.host/3ca3724a-1dd4-41d0-8783-b409dabecb3d/TMc5F1aZeS.json",
        animate=True,
        width=750,
        height=600,
    )

    layoutPrincipal = ft.Row(
        [
            ft.Container(content=caixaLogin, expand=1, alignment=ft.alignment.center),
            ft.Container(content=imagemPsico, expand=1, alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=40,
    )

    fundoComGradiente = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#3B82F6", "#60A5FA", "#93C5FD"],
        ),
        content=layoutPrincipal,
    )

    def criar_rodape():
        anoAtual = datetime.now().year
        return ft.Container(
            padding=ft.padding.symmetric(vertical=10, horizontal=40),
            bgcolor=ft.Colors.BLACK,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Text("Sobre", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                    ft.Text("Contato", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                    ft.Text("Privacidade", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                    ft.Text("Termos de Uso", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=20
                            ),
                           ft.Container(expand=1),
                            ft.Text("Suporte: suporte@TGPSISolutions.com", color=ft.Colors.WHITE)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=ft.Colors.GREY, thickness=0.5, height=5),
                    ft.Row(
                        [
                            ft.Text(f"© {anoAtual} TGPSI Solutions", color=ft.Colors.WHITE),
                            ft.Container(expand=1),
                            ft.Text("Versão 1.0.0", color=ft.Colors.WHITE, size=12),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                ],
                spacing=5
            )
        )

    rodape = criar_rodape()

    layout_completo = ft.Column(
        [
            fundoComGradiente,
            rodape
        ],
        spacing=0,
        expand=True
    )

    return ft.View(route="/login", controls=[layout_completo])
