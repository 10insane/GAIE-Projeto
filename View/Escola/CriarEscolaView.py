import flet as ft
from Models.EscolasModel import *
 
def CriarEscola(page: ft.Page):
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
 
    nome_input = ft.TextField(label="Nome da Escola", width=300)
    mensagem = ft.Text("", size=14, color="#16A34A", weight=ft.FontWeight.W_600)
 
    def guardar_escola(e):
        nome = nome_input.value.strip()
 
        if not nome:
            mensagem.value = "⚠️ Preenche o Nome da escola."
            mensagem.color = "#DC2626"
            page.update()
            return
 
        try:
            conn = bd_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Escolas (NomeEscola)
                    VALUES (%s)
                """, (nome,))  # <-- Corrigido: tuple com 1 elemento
                conn.commit()
 
                mensagem.value = "✅ Escola criada com sucesso!"
                mensagem.color = "#16A34A"
                page.update()
 
                # Opcional: voltar à tela principal depois de criar
                page.go("/TelaPrincipalAdmin")
            finally:
                cursor.close()
                conn.close()
 
        except Exception as err:
            mensagem.value = f"❌ Erro ao criar escola: {err}"
            mensagem.color = "#DC2626"
            page.update()
 
    conteudo = ft.Container(
        content=ft.Column([
            ft.Text("Criar Nova Escola", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
            ft.Container(height=20),
            nome_input,
            ft.Container(height=10),
            mensagem,
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton("Guardar", bgcolor=cor_primaria, color="white", on_click=guardar_escola),
                ft.OutlinedButton("Cancelar", on_click=lambda e: page.go("/TelaPrincipalAdmin")),
            ], spacing=15),
        ], spacing=10),
        bgcolor=cor_card,
        padding=30,
        border_radius=16,
        expand=False,
    )
 
    return ft.View(
        route="/criar-escola",
        controls=[conteudo],
        bgcolor=cor_fundo,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
 