import flet as ft
from Models.EscolasModel import *

def CriarEscola(page: ft.Page):
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

    # ===== CAMPO NOME DA ESCOLA =====
    nome_input = ft.TextField(
        label="Nome da Escola",
        hint_text="Digite o nome completo da escola",
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        prefix_icon=ft.Icons.DOMAIN,
        text_size=15,
        color=cor_texto_claro,
        label_style=ft.TextStyle(color=cor_texto_medio),
        hint_style=ft.TextStyle(color=cor_texto_medio),
        bgcolor=cor_fundo,
        filled=True,
    )

    # ===== MENSAGEM DE FEEDBACK =====
    mensagem_feedback = ft.Container(visible=False)

    # ===== FUNÇÃO GUARDAR =====
    def guardar_escola(e):
        nome = nome_input.value.strip()

        if not nome:
            mensagem_feedback.content = ft.Container(
                content=ft.Text("✗ Nome da escola é obrigatório", color=cor_erro, size=14),
                bgcolor="#1A0000",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()
            return

        try:
            conn = bd_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Escolas (NomeEscola)
                    VALUES (%s)
                """, (nome,))
                conn.commit()

                mensagem_feedback.content = ft.Container(
                    content=ft.Text("✓ Escola criada com sucesso!", color=cor_sucesso, size=14),
                    bgcolor="#001A0A",
                    padding=15,
                    border_radius=8,
                    border=ft.border.all(1, cor_sucesso),
                )
                mensagem_feedback.visible = True
                page.update()

                # Limpar campo
                import time
                time.sleep(1.5)
                nome_input.value = ""
                mensagem_feedback.visible = False
                page.update()
                
                # Voltar à tela principal
                page.go("/TelaPrincipalAdmin")

            finally:
                cursor.close()
                conn.close()

        except Exception as err:
            mensagem_feedback.content = ft.Container(
                content=ft.Text(f"✗ Erro: {str(err)}", color=cor_erro, size=14),
                bgcolor="#1A0000",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, cor_erro),
            )
            mensagem_feedback.visible = True
            page.update()

    # ======================= BOTÕES ==========================

    btn_guardar = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SAVE, size=18),
                    ft.Text("Guardar Escola", size=15, weight=ft.FontWeight.BOLD),
                ],
                tight=True,
                spacing=8,
            ),
            bgcolor=cor_primaria,
            color=ft.Colors.WHITE,
            on_click=guardar_escola,
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
            on_click=lambda e: page.go("/TelaPrincipalAdmin"),
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
                            on_click=lambda e: page.go("/TelaPrincipalAdmin"),
                            tooltip="Voltar",
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Sistema SPO - Criar Nova Escola",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto_claro,
                                ),
                                ft.Text(
                                    "Adicione uma nova escola ao sistema",
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

                # Card de informação
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO, color=cor_primaria, size=18),
                        ft.Text(
                            "Preencha o nome da escola para adicioná-la ao sistema",
                            size=13,
                            color=cor_texto_medio,
                        ),
                    ], spacing=10),
                    bgcolor=cor_card,
                    padding=15,
                    border_radius=12,
                    border=ft.border.all(1, cor_borda),
                ),

                # Campo principal
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.Icon(ft.Icons.DOMAIN, color=cor_primaria, size=18),
                                ft.Text("Nome da Escola", size=14, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ], spacing=8),
                            ft.Container(height=5),
                            nome_input,
                        ],
                        spacing=10
                    ),
                    bgcolor=cor_card,
                    padding=15,
                    border_radius=12,
                    border=ft.border.all(1, cor_borda),
                ),

                # Botões
                ft.Container(
                    content=ft.Row(
                        [btn_cancelar, btn_guardar],
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
        route="/criar-escola",
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