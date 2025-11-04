import flet as ft
import flet_lottie as fl
import threading
import time
import math
from Models.TecnicoModel import listarTecnico


def LoginView(page: ft.Page):
    animacaoLottie = fl.Lottie(
        src="https://lottie.host/5859fa72-f001-4fa0-9c23-f5df61e4bfe5/MpooU95fLc.json",
        animate=True,
        width=150,
        height=150,
    )

    campoNumeroProcesso = ft.TextField(label="Nº Processo Técnico", prefix_icon=ft.Icons.BADGE, width=300)
    campoNomeTecnico = ft.TextField(label="Nome do Técnico", prefix_icon=ft.Icons.PERSON, width=300)
    mensagemErro = ft.Text(color=ft.Colors.RED)
    botaoCriar = ft.ElevatedButton("Criar Técnico", visible=False, on_click=lambda e: page.go("/criar-tecnico"))

    # ======= Função de autenticação =======
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

    botaoEntrar = ft.ElevatedButton("Entrar", on_click=autenticar, bgcolor="#8A2BE2", color=ft.Colors.WHITE)
    botoesLogin = ft.Row([botaoEntrar, botaoCriar], alignment=ft.MainAxisAlignment.CENTER)

    # ======= Fundo com gradiente animado =======
    fundoComGradiente = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#47C3FD", "#45FFCA", "#950ECE"],
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    animacaoLottie,
                                    ft.Text(
                                        "Login do Técnico",
                                        style=ft.TextThemeStyle.HEADLINE_SMALL,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    campoNumeroProcesso,
                                    campoNomeTecnico,
                                    botoesLogin,
                                    mensagemErro,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                            ),
                            padding=40,
                            width=400,
                            border_radius=20,
                            bgcolor="rgba(0, 0, 0, 0.8)",
                            border=ft.border.all(2, ft.Colors.WHITE70),
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=8,
                                color="rgba(0,0,0,0.5)",
                                offset=ft.Offset(2, 2),
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
    )

    # ======= Animação do gradiente com thread =======
    def animar_gradiente():
        t = 0
        while True:
            t += 0.03
            r1 = int(128 + 127 * math.sin(t))
            g1 = int(128 + 127 * math.sin(t + 2))
            b1 = int(128 + 127 * math.sin(t + 4))

            r2 = int(128 + 127 * math.sin(t + 1))
            g2 = int(128 + 127 * math.sin(t + 3))
            b2 = int(128 + 127 * math.sin(t + 5))

            color1 = f"#{r1:02x}{g1:02x}{b1:02x}"
            color2 = f"#{r2:02x}{g2:02x}{b2:02x}"

            fundoComGradiente.gradient = ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[color1, color2],
            )
            fundoComGradiente.update()
            time.sleep(0.05)

    # Inicia thread de animação
    threading.Thread(target=animar_gradiente, daemon=True).start()

    return ft.View(
        route="/login",
        controls=[fundoComGradiente],
    )
