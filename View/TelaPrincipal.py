import flet as ft

alunos = [
    {"nome": "João", "tecnico": "Sidnei", "problema": "Internet lenta", "estado": "Pendente"},
    {"nome": "Maria", "tecnico": "Sidnei", "problema": "Computador travando", "estado": "Concluído"},
    {"nome": "Pedro", "tecnico": "Carlos", "problema": "Tela azul", "estado": "Em andamento"},
]

def PaginaPrincipal(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"


    cabecalho = ft.Container(
        bgcolor="#8A2BE2",
        padding=15,
        content=ft.Row(
            [
                ft.Text(f"GAIE - Bem-vindo {tecnico_nome}", size=22, color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.ElevatedButton("Sair", on_click=lambda e: page.go("/login"), bgcolor="#FF4D4D"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    filtro_nome = ft.Dropdown(label="Aluno", options=[ft.dropdown.Option(a["nome"]) for a in alunos])
    filtro_tecnico = ft.Dropdown(label="Técnico", options=[ft.dropdown.Option(a["tecnico"]) for a in alunos])
    filtro_estado = ft.Dropdown(label="Estado", options=[ft.dropdown.Option(a["estado"]) for a in alunos])

    tabela = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Aluno")),
        ft.DataColumn(ft.Text("Técnico")),
        ft.DataColumn(ft.Text("Problema")),
        ft.DataColumn(ft.Text("Estado")),
    ])

    def atualizar_tabela():
        tabela.rows.clear()
        for a in alunos:
            if filtro_nome.value and a["nome"] != filtro_nome.value:
                continue
            if filtro_tecnico.value and a["tecnico"] != filtro_tecnico.value:
                continue
            if filtro_estado.value and a["estado"] != filtro_estado.value:
                continue
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(a["nome"])),
                ft.DataCell(ft.Text(a["tecnico"])),
                ft.DataCell(ft.Text(a["problema"])),
                ft.DataCell(ft.Text(a["estado"])),
            ]))
        page.update()

    atualizar_tabela()

    conteudo = ft.Column(
        [filtro_nome, filtro_tecnico, filtro_estado, tabela],
        spacing=15,
        expand=True,
    )

    return ft.View(
        route="/pagina-principal", 
        controls=[cabecalho, ft.Container(padding=20, content=conteudo)],
    )
