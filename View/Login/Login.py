import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import listarTecnico
from Models.AdminModel import listarAdmin
import json
import os

TOKEN_FILE = "token.json"

def LoginView(page: ft.Page):
    page.title = "GAIE - Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # === CORES ===
    cor_primaria = "#8B5CF6"
    cor_card = "#1A1A1A"
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#9CA3AF"
    cor_borda = "#2D2D2D"
    cor_erro = "#EF4444"
    cor_fundo_escuro = "#0F0F0F"

    # Limita nº de processo a 10 dígitos
    def limitar_numero_processo(e):
        valor = ''.join(filter(str.isdigit, e.control.value))
        if len(valor) > 10:
            valor = valor[:10]
        e.control.value = valor
        page.update()

    # Função fictícia para gerar OAuth token
    def gerar_oauth_token(nProc, password):
        # Aqui você implementa a chamada ao backend para obter o token real
        return f"token_{nProc}"

    # === CAMPOS DE INPUT ===
    campoNumeroProcesso = ft.TextField(
        label="Nº Processo Técnico",
        prefix_icon=ft.Icons.BADGE_ROUNDED,
        width=380,
        autofocus=True,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        focused_border_width=2,
        hint_text="Digite o número do processo",
        hint_style=ft.TextStyle(color=cor_texto_medio, size=13),
        text_style=ft.TextStyle(color=cor_texto_claro, weight=ft.FontWeight.W_500, size=15),
        label_style=ft.TextStyle(color=cor_texto_medio),
        border_radius=12,
        height=60,
        bgcolor=cor_card,
        filled=True,
        cursor_color=cor_primaria,
        on_change=limitar_numero_processo,
    )

    campoSenha = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.KEY,
        width=380,
        password=True,
        can_reveal_password=True,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        focused_border_width=2,
        hint_text="Digite a sua password",
        hint_style=ft.TextStyle(color=cor_texto_medio, size=13),
        text_style=ft.TextStyle(color=cor_texto_claro, weight=ft.FontWeight.W_500, size=15),
        label_style=ft.TextStyle(color=cor_texto_medio),
        border_radius=12,
        height=60,
        bgcolor=cor_card,
        filled=True,
        cursor_color=cor_primaria,
    )

    # === MENSAGEM DE ERRO ===
    mensagemErro = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ERROR_ROUNDED, color=cor_erro, size=20),
                ft.Text("", size=13, color=cor_erro, weight=ft.FontWeight.W_500),
            ],
            spacing=10,
        ),
        padding=12,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, cor_erro)),
        visible=False,
    )

    # === CHECKBOX LEMBRAR-ME ===
    checkboxLembrar = ft.Row(
        [
            ft.Checkbox(
                label="Lembrar-me",
                value=False,
                fill_color=cor_primaria,
                check_color=ft.Colors.WHITE,
                label_style=ft.TextStyle(color=cor_texto_medio, size=13),
            ),
            ft.Container(expand=True),
            ft.TextButton("Esqueceu a senha?", style=ft.ButtonStyle(color=cor_primaria)),
        ],
        width=380,
    )

    # Autenticação
    def autenticar(e=None):
        nProc = campoNumeroProcesso.value.strip()
        password = campoSenha.value.strip()
        lembrar = checkboxLembrar.controls[0].value  # Valor do checkbox

        if not nProc or not password:
            mensagemErro.visible = True
            mensagemErro.content.controls[1].value = "Preencha ambos os campos!"
            page.update()
            return

        # Autenticar Admin
        admins = listarAdmin()
        admin_valido = next(
            (a for a in admins if str(a.get("nProcAdmin", "")).strip() == nProc and a.get("password", "") == password),
            None
        )
        if admin_valido:
            token = gerar_oauth_token(nProc, password) if lembrar else None
            page.session.set("usuario_tipo", "admin")
            page.session.set("usuario_nome", admin_valido.get("NomeAdmin"))
            if token:
                page.session.set("oauth_token", token)
                salvar_token(token, "admin")
            page.go("/TelaPrincipalAdmin")
            return

        # Autenticar Técnico
        tecnicos = listarTecnico()
        tecnico_valido = next(
            (t for t in tecnicos if str(t.get("nProcTecnico", "")).strip() == nProc and t.get("password", "") == password),
            None
        )
        if tecnico_valido:
            token = gerar_oauth_token(nProc, password) if lembrar else None
            page.session.set("usuario_tipo", "tecnico")
            page.session.set("tecnico_nome", tecnico_valido.get("NomeTecnico"))
            page.session.set("nProcTecnico", tecnico_valido.get("nProcTecnico"))
            if token:
                page.session.set("oauth_token", token)
                salvar_token(token, "tecnico")
            page.go("/pagina-principal")
            return

        # Nenhum usuário encontrado
        mensagemErro.visible = True
        mensagemErro.content.controls[1].value = "Número de processo ou senha incorretos!"
        page.update()

    # Salva token em arquivo local para persistência
    def salvar_token(token, usuario_tipo):
        with open(TOKEN_FILE, "w") as f:
            json.dump({"oauth_token": token, "usuario_tipo": usuario_tipo}, f)

    # Verifica token existente ao iniciar a página
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                token = data.get("oauth_token")
                usuario_tipo = data.get("usuario_tipo")
                if token and usuario_tipo:
                    page.session.set("oauth_token", token)
                    page.session.set("usuario_tipo", usuario_tipo)
                    if usuario_tipo == "admin":
                        page.go("/TelaPrincipalAdmin")
                    else:
                        page.go("/pagina-principal")
        except:
            pass

    # === BOTÃO ENTRAR ===
    botaoEntrar = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGIN_ROUNDED, color=ft.Colors.WHITE, size=22),
                ft.Text("Entrar no Sistema", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=380,
        height=56,
        bgcolor=cor_primaria,
        border_radius=12,
        ink=True,
        on_click=autenticar,
    )

    # === ANIMAÇÕES LOTTIE ===
    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        animate=True,
        width=150,
        height=150,
    )

    imagemPsico = ft.Container(
        content=fl.Lottie(
            src="https://lottie.host/3ca3724a-1dd4-41d0-8783-b409dabecb3d/TMc5F1aZeS.json",
            animate=True,
            width=760,
            height=760,
        ),
        padding=60,
    )

    # === CARD DE LOGIN ===
    caixaLogin = ft.Container(
        width=480,
        height=780,
        padding=50,
        bgcolor=cor_card,
        border_radius=30,
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            blur_radius=40,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            spread_radius=5,
        ),
        content=ft.Column(
            [
                ft.Container(content=animacaoLottie, padding=ft.padding.only(bottom=10)),
                ft.Column(
                    [
                        ft.Text("Bem-vindo de volta", size=32, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                        ft.Text("Entre com suas credenciais para continuar", size=14, color=cor_texto_medio),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                campoNumeroProcesso,
                campoSenha,
                ft.Container(height=5),
                checkboxLembrar,
                ft.Container(height=10),
                mensagemErro,
                botaoEntrar,
                ft.Container(height=15),
                ft.Row(
                    [
                        ft.Container(height=1, bgcolor=cor_borda, expand=True),
                        ft.Text("GAIE v1.0", size=12, color=cor_texto_medio),
                        ft.Container(height=1, bgcolor=cor_borda, expand=True),
                    ],
                    spacing=10,
                    width=380,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # === LAYOUT PRINCIPAL ===
    layoutPrincipal = ft.Row(
        [
            ft.Container(content=caixaLogin, expand=1, alignment=ft.alignment.center),
            ft.Container(content=imagemPsico, expand=1, alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=60,
    )

    # === FUNDO COM GRADIENTE ===
    fundoComGradiente = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                "#0F0F0F",
                "#1a0a2e",
                "#2d1b4e",
                "#1a0a2e",
                "#0F0F0F",
            ],
        ),
        content=layoutPrincipal,
    )

    layout_completo = ft.Column([fundoComGradiente], spacing=0, expand=True)

    return ft.View(
        route="/login",
        controls=[layout_completo],
        bgcolor=cor_fundo_escuro
    )
