import flet as ft

# Dados de exemplo (posteriormente virão do banco de dados)
alunos = [
    {"nome": "João Silva", "tecnico": "Sidnei Costa", "problema": "Internet lenta", "estado": "Pendente"},
    {"nome": "Maria Santos", "tecnico": "Sidnei Costa", "problema": "Computador travando", "estado": "Concluído"},
    {"nome": "Pedro Oliveira", "tecnico": "Carlos Mendes", "problema": "Tela azul", "estado": "Em andamento"},
    {"nome": "Ana Rodrigues", "tecnico": "Sidnei Costa", "problema": "Erro de sistema", "estado": "Pendente"},
]

def PaginaPrincipal(page: ft.Page):
    # Obtém nome do técnico da sessão
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"
    
    # === CORES E ESTILO ===
    cor_primaria = "#6A1B9A"  # Roxo mais profissional
    cor_secundaria = "#8E24AA"
    cor_acento = "#AB47BC"
    cor_fundo = "#F5F5F5"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#1A1A1A"
    cor_texto_medio = "#424242"
    cor_texto_claro = "#616161"
    
    # === CABEÇALHO ===
    cabecalho = ft.Container(
        bgcolor=cor_primaria,
        padding=20,
        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.WHITE, size=32),
                        ft.Column(
                            [
                                ft.Text(
                                    "GAIE - Gestão de Alunos",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    f"Bem-vindo, {tecnico_nome}",
                                    size=14,
                                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(expand=True),
                # Menu de perfil do utilizador
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                tecnico_nome,
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.WHITE,
                            ),
                            ft.PopupMenuButton(
                                icon=ft.Icons.ACCOUNT_CIRCLE,
                                icon_color=ft.Colors.WHITE,
                                icon_size=32,
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.PERSON, size=20),
                                                ft.Text("Meu Perfil", size=14),
                                            ],
                                            spacing=10,
                                        ),
                                        on_click=lambda e: page.go("/perfil"),
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.SETTINGS, size=20),
                                                ft.Text("Configurações", size=14),
                                            ],
                                            spacing=10,
                                        ),
                                        on_click=lambda e: page.go("/configuracoes"),
                                    ),
                                    ft.PopupMenuItem(),  # Divider
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOGOUT, size=20, color="#E53935"),
                                                ft.Text("Sair", size=14, color="#E53935", weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=10,
                                        ),
                                        on_click=lambda e: page.go("/login"),
                                    ),
                                ],
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.padding.only(left=15, right=5),
                    border_radius=25,
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )
    
    # === MENU LATERAL ===
    def criar_botao_menu(texto, icone, rota=None, ativo=False):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        icone, 
                        color=ft.Colors.WHITE if ativo else cor_primaria, 
                        size=22
                    ),
                    ft.Text(
                        texto, 
                        size=15, 
                        weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.W_500, 
                        color=ft.Colors.WHITE if ativo else cor_texto_escuro
                    ),
                ],
                spacing=12,
            ),
            padding=15,
            border_radius=10,
            ink=True,
            on_click=lambda e: page.go(rota) if rota else None,
            bgcolor=cor_primaria if ativo else ft.Colors.with_opacity(0.08, cor_primaria),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
    
    menu_lateral = ft.Container(
        width=250,
        bgcolor=cor_card,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.SCHOOL, color=cor_primaria, size=40),
                            ft.Text(
                                "GAIE",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=cor_texto_escuro,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=ft.padding.only(bottom=15),
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, cor_texto_claro)),
                ft.Container(height=15),
                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD, "/dashboard", ativo=True),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE, "/alunos"),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT, "/registos"),
                criar_botao_menu("Técnicos", ft.Icons.PERSON, "/tecnicos"),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL, "/escolas"),
                ft.Container(expand=True),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, cor_texto_claro)),
                ft.Container(height=10),
                criar_botao_menu("Configurações", ft.Icons.SETTINGS, "/configuracoes"),
            ],
            spacing=8,
        ),
    )
    
    # === FILTROS ===
    filtro_nome = ft.Dropdown(
        label="Filtrar por Aluno",
        hint_text="Todos os alunos",
        options=[ft.dropdown.Option(a["nome"]) for a in alunos],
        border_radius=8,
        filled=True,
        bgcolor=cor_card,
    )
    
    filtro_tecnico = ft.Dropdown(
        label="Filtrar por Técnico",
        hint_text="Todos os técnicos",
        options=[ft.dropdown.Option(a["tecnico"]) for a in alunos],
        border_radius=8,
        filled=True,
        bgcolor=cor_card,
    )
    
    filtro_estado = ft.Dropdown(
        label="Filtrar por Estado",
        hint_text="Todos os estados",
        options=[ft.dropdown.Option(a["estado"]) for a in alunos],
        border_radius=8,
        filled=True,
        bgcolor=cor_card,
    )
    
    # === TABELA DE DADOS ===
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Aluno", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Técnico", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Problema", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
        ],
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, cor_texto_claro)),
        border_radius=10,
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.with_opacity(0.05, cor_texto_claro)),
        heading_row_color=ft.Colors.with_opacity(0.05, cor_primaria),
    )
    
    def obter_cor_estado(estado):
        cores = {
            "Pendente": "#FFA726",
            "Em andamento": "#42A5F5",
            "Concluído": "#66BB6A",
        }
        return cores.get(estado, "#757575")
    
    def atualizar_tabela():
        tabela.rows.clear()
        for a in alunos:
            # Aplicar filtros
            if filtro_nome.value and a["nome"] != filtro_nome.value:
                continue
            if filtro_tecnico.value and a["tecnico"] != filtro_tecnico.value:
                continue
            if filtro_estado.value and a["estado"] != filtro_estado.value:
                continue
            
            # Badge de estado
            badge_estado = ft.Container(
                content=ft.Text(
                    a["estado"],
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor=obter_cor_estado(a["estado"]),
                border_radius=15,
            )
            
            # Botões de ação
            botoes_acao = ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY,
                        icon_color=cor_primaria,
                        tooltip="Ver detalhes",
                        icon_size=20,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#1976D2",
                        tooltip="Editar",
                        icon_size=20,
                    ),
                ],
                spacing=5,
            )
            
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(a["nome"], size=14)),
                        ft.DataCell(ft.Text(a["tecnico"], size=14)),
                        ft.DataCell(ft.Text(a["problema"], size=14)),
                        ft.DataCell(badge_estado),
                        ft.DataCell(botoes_acao),
                    ]
                )
            )
        page.update()
    
    # Conectar eventos de filtro
    filtro_nome.on_change = lambda e: atualizar_tabela()
    filtro_tecnico.on_change = lambda e: atualizar_tabela()
    filtro_estado.on_change = lambda e: atualizar_tabela()
    
    # Preencher tabela inicial
    atualizar_tabela()
    
    # === CARTÕES DE ESTATÍSTICAS ===
    def criar_card_estatistica(titulo, valor, icone, cor):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icone, color=cor, size=28),
                            ft.Container(expand=True),
                            ft.Text(str(valor), size=32, weight=ft.FontWeight.BOLD, color=cor),
                        ],
                    ),
                    ft.Text(titulo, size=14, color=cor_texto_claro),
                ],
                spacing=10,
            ),
            bgcolor=cor_card,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
            expand=True,
        )
    
    cards_estatisticas = ft.Row(
        [
            criar_card_estatistica("Total de Alunos", len(alunos), ft.Icons.PEOPLE, "#6A1B9A"),
            criar_card_estatistica("Pendentes", 2, ft.Icons.PENDING, "#FFA726"),
            criar_card_estatistica("Em Andamento", 1, ft.Icons.AUTORENEW, "#42A5F5"),
            criar_card_estatistica("Concluídos", 1, ft.Icons.CHECK_CIRCLE, "#66BB6A"),
        ],
        spacing=15,
    )
    
    # === ÁREA DE CONTEÚDO PRINCIPAL ===
    conteudo_principal = ft.Container(
        expand=True,
        bgcolor=cor_fundo,
        padding=20,
        content=ft.Column(
            [
                # Estatísticas
                cards_estatisticas,
                
                # Seção de filtros
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "Lista de Registos",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_texto_escuro,
                                    ),
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Novo Registo",
                                        icon=ft.Icons.ADD,
                                        bgcolor=cor_primaria,
                                        color=ft.Colors.WHITE,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                            ),
                            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                            ft.Row(
                                [filtro_nome, filtro_tecnico, filtro_estado],
                                spacing=15,
                            ),
                        ],
                        spacing=15,
                    ),
                    bgcolor=cor_card,
                    padding=20,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                ),
                
                # Tabela
                ft.Container(
                    content=ft.Column(
                        [tabela],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    bgcolor=cor_card,
                    padding=20,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                    expand=True,
                ),
            ],
            spacing=20,
            expand=True,
        ),
    )
    
    # === LAYOUT PRINCIPAL ===
    layout = ft.Row(
        [
            menu_lateral,
            conteudo_principal,
        ],
        spacing=20,
        expand=True,
    )
    
    return ft.View(
        route="/pagina-principal",
        controls=[
            cabecalho,
            ft.Container(
                content=layout,
                padding=20,
                bgcolor=cor_fundo,
                expand=True,
            ),
        ],
        bgcolor=cor_fundo,
    )