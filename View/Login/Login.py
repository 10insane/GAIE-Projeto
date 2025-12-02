import flet as ft
import flet_lottie as fl
from Models.TecnicoModel import listarTecnico
from Models.AdminModel import listarAdmin
from datetime import datetime

def LoginView(page: ft.Page):
    page.title = "GAIE - Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # === CORES - TEMA PRETO E ROXO ===
    cor_primaria = "#8B5CF6"  # Roxo vibrante
    cor_secundaria = "#A78BFA"  # Roxo claro
    cor_roxo_escuro = "#6D28D9"  # Roxo escuro
    cor_fundo_escuro = "#0F0F0F"  # Preto profundo
    cor_card = "#1A1A1A"  # Cinza muito escuro
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#9CA3AF"
    cor_borda = "#2D2D2D"
    cor_erro = "#EF4444"
    cor_hover = "#7C3AED"
    
    # Limita nº de processo a 10 dígitos
    def limitar_numero_processo(e):
        valor = ''.join(filter(str.isdigit, e.control.value))
        if len(valor) > 10:
            valor = valor[:10]
        e.control.value = valor
        page.update()
    
    # Autenticação
    def autenticar(e):
        nProc = campoNumeroProcesso.value.strip()
        password = campoSenha.value.strip()

        if not nProc or not password:
            mensagemErro.visible = True
            mensagemErro.content.controls[1].value = "Preencha ambos os campos!"
            page.update()
            return

        # Tentar autenticar como Admin
        admins = listarAdmin()
        admin_valido = next(
            (a for a in admins if str(a.get("nProcAdmin", "")).strip() == nProc and a.get("password", "") == password),
            None
        )
        if admin_valido:
            page.session.set("usuario_tipo", "admin")
            page.session.set("usuario_nome", admin_valido.get("NomeAdmin"))
            page.go("/TelaPrincipalAdmin")
            return

        # Se não for admin, tenta autenticar como Técnico
        tecnicos = listarTecnico()
        tecnico_valido = next(
            (t for t in tecnicos if str(t.get("nProcTecnico", "")).strip() == nProc and t.get("password", "") == password),
            None
        )
        if tecnico_valido:
            page.session.set("usuario_tipo", "tecnico")
            page.session.set("usuario_nome", tecnico_valido.get("NomeTecnico"))
            page.go("/pagina-principal")
            return

        # Se não encontrou ninguém
        mensagemErro.visible = True
        mensagemErro.content.controls[1].value = "Número de processo ou senha incorretos!"
        page.update()

    # === ANIMAÇÃO LOTTIE ===
    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        animate=True,
        width=150,
        height=150,
    )

    # === CAMPOS DE INPUT MODERNOS ===
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
        text_style=ft.TextStyle(
            color=cor_texto_claro,
            weight=ft.FontWeight.W_500,
            size=15,
        ),
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
        text_style=ft.TextStyle(
            color=cor_texto_claro,
            weight=ft.FontWeight.W_500,
            size=15,
        ),
        label_style=ft.TextStyle(color=cor_texto_medio),
        border_radius=12,
        height=60,
        bgcolor=cor_card,
        filled=True,
        cursor_color=cor_primaria,
    )

    # === MENSAGEM DE ERRO ESTILIZADA ===
    mensagemErro = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ERROR_ROUNDED, color=cor_erro, size=20),
                ft.Text(
                    "",
                    size=13,
                    color=cor_erro,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=10,
        ),
        padding=12,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.1, cor_erro),
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, cor_erro)),
        visible=False,
    )

    # === BOTÃO ENTRAR MODERNO ===
    botaoEntrar = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGIN_ROUNDED, color=ft.Colors.WHITE, size=22),
                ft.Text(
                    "Entrar no Sistema",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
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
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.4, cor_primaria),
            offset=ft.Offset(0, 4),
        ),
    )

    # === CHECKBOX LEMBRAR ===
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
            ft.TextButton(
                "Esqueceu a senha?",
                style=ft.ButtonStyle(
                    color=cor_primaria,
                ),
            ),
        ],
        width=380,
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
                        ft.Text(
                            "Bem-vindo de volta",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=cor_texto_claro,
                        ),
                        ft.Text(
                            "Entre com suas credenciais para continuar",
                            size=14,
                            color=cor_texto_medio,
                        ),
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

    # === IMAGEM LATERAL ===
    imagemPsico = ft.Container(
        content=fl.Lottie(
            src="https://lottie.host/3ca3724a-1dd4-41d0-8783-b409dabecb3d/TMc5F1aZeS.json",
            animate=True,
            width=760,
            height=760,
        ),
        padding=60,
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

    # === FUNDO COM GRADIENTE ROXO E PRETO ===
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

    # === LAYOUT COMPLETO ===
    layout_completo = ft.Column([fundoComGradiente], spacing=0, expand=True)

    return ft.View(
        route="/login",
        controls=[layout_completo],
        bgcolor=cor_fundo_escuro
    )
