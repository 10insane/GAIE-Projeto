import flet as ft
from Models.TecnicoModel import criarTecnico

def CreateTecnico(page: ft.Page):
    # Campos de entrada com estilo idêntico ao login
    def limitar_numero_processo(e):
     valor = ''.join(filter(str.isdigit, e.control.value))  # mantém apenas dígitos
     if len(valor) > 10:  # agora o limite é 10
        valor = valor[:10]  # corta o excesso
     e.control.value = valor
     page.update()
    
    campoNovoNumero = ft.TextField(
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

    campoNovoNome = ft.TextField(
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

    # Função salvar técnico
    def salvarTecnico(e):
        nProc = campoNovoNumero.value.strip()
        nome = campoNovoNome.value.strip()

        if not nProc or not nome:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return

        if criarTecnico(nProc, nome):
            page.snack_bar = ft.SnackBar(ft.Text("✅ Técnico criado com sucesso!"))
            page.snack_bar.open = True
            page.go("/login")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Erro ao criar técnico!"))
            page.snack_bar.open = True
            page.update()

    # Botão Salvar
    botaoSalvar = ft.ElevatedButton(
        "Salvar",
        on_click=salvarTecnico,
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

    # Botão Cancelar
    botaoCancelar = ft.ElevatedButton(
        "Cancelar",
        on_click=lambda e: page.go("/login"),
        width=150,
        height=55,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
            bgcolor="#2563EB",
            color=ft.Colors.WHITE,
            text_style=ft.TextStyle(
                font_family="sans-serif",
                weight=ft.FontWeight.BOLD,
                size=16,
                letter_spacing=1.0,
            ),
        ),
    )

    # Linha de botões
    botoesAcao = ft.Row(
        [botaoSalvar, botaoCancelar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Caixa principal com mesmo estilo do login
    caixaCriarTecnico = ft.Container(
        width=380,
        height=420,
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
                ft.Text(
                    "Criar Novo Técnico",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1E40AF"
                ),
                campoNovoNumero,
                campoNovoNome,
                botoesAcao,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )

    # Fundo com gradiente idêntico ao login - ocupando tela inteira
    fundoComGradiente = ft.Container(
        width=page.width if page.width else 1920,
        height=page.height if page.height else 1080,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#3B82F6", "#60A5FA", "#93C5FD"],
        ),
        content=ft.Stack(
            [
                ft.Container(
                    content=caixaCriarTecnico,
                    alignment=ft.alignment.center,
                )
            ],
            expand=True,
        )
    )

    return ft.View(
        route="/criar-tecnico",
        controls=[fundoComGradiente],
    )