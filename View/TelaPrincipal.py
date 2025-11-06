import flet as ft
 
# Dados de exemplo (posteriormente virão do banco de dados)
alunos = [
    {"nome": "João Silva", "tecnico": "Sidnei Costa", "problema": "Dificuldades de aprendizagem", "estado": "A aguardar"},
    {"nome": "Maria Santos", "tecnico": "Sidnei Costa", "problema": "Problemas de comportamento", "estado": "Em Avaliação"},
    {"nome": "Pedro Oliveira", "tecnico": "Carlos Mendes", "problema": "Necessidades educativas especiais", "estado": "Em intervenção"},
    {"nome": "Ana Rodrigues", "tecnico": "Sidnei Costa", "problema": "Apoio psicológico", "estado": "Pendente"},
    {"nome": "Carlos Ferreira", "tecnico": "Carlos Mendes", "problema": "Acompanhamento familiar", "estado": "Arquivado"},
    {"nome": "Sofia Martins", "tecnico": "Sidnei Costa", "problema": "Integração escolar", "estado": "Em vigilância"},
    {"nome": "Tiago Costa", "tecnico": "Carlos Mendes", "problema": "Dificuldades de concentração", "estado": "A aguardar"},
    {"nome": "Beatriz Alves", "tecnico": "Sidnei Costa", "problema": "Apoio social", "estado": "Pendente"},
    {"nome": "Ricardo Sousa", "tecnico": "Carlos Mendes", "problema": "Orientação vocacional", "estado": "Em Avaliação"},
    {"nome": "Inês Ribeiro", "tecnico": "Sidnei Costa", "problema": "Dificuldades emocionais", "estado": "Em intervenção"},
]
 
def PaginaPrincipal(page: ft.Page):
    # Obtém nome do técnico da sessão
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"
   
    # === CORES E ESTILO - INSPIRADO EM DESIGN MODERNO ===
    cor_primaria = "#1E40AF"  # Azul profissional
    cor_primaria_hover = "#1E3A8A"
    cor_secundaria = "#3B82F6"
    cor_acento = "#60A5FA"
    cor_fundo = "#F8FAFC"
    cor_fundo_secundario = "#F1F5F9"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
    cor_texto_medio = "#334155"
    cor_texto_claro = "#64748B"
    cor_borda = "#E2E8F0"
   
    # === CABEÇALHO PREMIUM ===
    cabecalho = ft.Container(
        bgcolor=cor_primaria,
        padding=ft.padding.symmetric(horizontal=30, vertical=18),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.WHITE, size=32),
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                            padding=10,
                            border_radius=12,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "GAIE",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "Gestão Integrada de Alunos e Educação",
                                    size=12,
                                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(expand=True),
                # Menu de perfil do utilizador
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        tecnico_nome,
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        "Técnico Responsável",
                                        size=11,
                                        color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                                    ),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            ft.PopupMenuButton(
                                icon=ft.Icons.ACCOUNT_CIRCLE,
                                icon_color=ft.Colors.WHITE,
                                icon_size=36,
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.PERSON_ROUNDED, size=20, color=cor_texto_medio),
                                                ft.Text("Meu Perfil", size=14, color=cor_texto_escuro),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/perfil"),
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.SETTINGS_ROUNDED, size=20, color=cor_texto_medio),
                                                ft.Text("Configurações", size=14, color=cor_texto_escuro),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/configuracoes"),
                                    ),
                                    ft.PopupMenuItem(),  # Divider
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#DC2626"),
                                                ft.Text("Terminar Sessão", size=14, color="#DC2626", weight=ft.FontWeight.W_600),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/login"),
                                    ),
                                ],
                            ),
                        ],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    border_radius=30,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )
   
    # === MENU LATERAL PREMIUM ===
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
                spacing=14,
            ),
            padding=16,
            border_radius=12,
            ink=True,
            on_click=lambda e: page.go(rota) if rota else None,
            bgcolor=cor_primaria if ativo else "transparent",
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
   
    menu_lateral = ft.Container(
        width=260,
        bgcolor=cor_card,
        padding=24,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
        ),
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE_ROUNDED, color=cor_primaria, size=48),
                                bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                                padding=14,
                                border_radius=16,
                            ),
                            ft.Text(
                                "Menu Principal",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=cor_texto_escuro,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=15),
                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD_ROUNDED, "/dashboard", ativo=True),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE_ROUNDED, "/alunos"),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT_ROUNDED, "/registos"),
                criar_botao_menu("Técnicos", ft.Icons.PERSON_ROUNDED, "/tecnicos"),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL_ROUNDED, "/escolas"),
                ft.Container(expand=True),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=10),
                criar_botao_menu("Configurações", ft.Icons.SETTINGS_ROUNDED, "/configuracoes"),
                ft.Container(
                    content=ft.Text(
                        "v1.0.0",
                        size=11,
                        color=cor_texto_claro,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=ft.padding.only(top=15),
                ),
            ],
            spacing=6,
        ),
    )
   
    # === FILTROS CORRIGIDOS ===
    filtro_nome = ft.Dropdown(
        label="Filtrar por Aluno",
        hint_text="Todos os alunos",
        options=[ft.dropdown.Option(key=a["nome"], text=a["nome"]) for a in alunos],
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        text_size=14,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
   
    filtro_tecnico = ft.Dropdown(
        label="Filtrar por Técnico",
        hint_text="Todos os técnicos",
        options=[ft.dropdown.Option(key=t, text=t) for t in sorted(list(set([a["tecnico"] for a in alunos])))],
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        text_size=14,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
   
    filtro_estado = ft.Dropdown(
        label="Filtrar por Estado",
        hint_text="Todos os estados",
        options=[
            ft.dropdown.Option(key="A aguardar", text="A aguardar"),
            ft.dropdown.Option(key="Em Avaliação", text="Em Avaliação"),
            ft.dropdown.Option(key="Em intervenção", text="Em intervenção"),
            ft.dropdown.Option(key="Pendente", text="Pendente"),
            ft.dropdown.Option(key="Arquivado", text="Arquivado"),
            ft.dropdown.Option(key="Em vigilância", text="Em vigilância"),
        ],
        border_radius=12,
        filled=True,
        bgcolor=cor_card,
        text_size=14,
        border_color=cor_borda,
        focused_border_color=cor_primaria,
        color=cor_texto_escuro,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
    )
   
    # === TABELA DE DADOS PREMIUM ===
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Aluno", weight=ft.FontWeight.BOLD, size=14, color=cor_texto_escuro)),
            ft.DataColumn(ft.Text("Técnico", weight=ft.FontWeight.BOLD, size=14, color=cor_texto_escuro)),
            ft.DataColumn(ft.Text("Problema", weight=ft.FontWeight.BOLD, size=14, color=cor_texto_escuro)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, size=14, color=cor_texto_escuro)),
            ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD, size=14, color=cor_texto_escuro)),
        ],
        border=ft.border.all(1, cor_borda),
        border_radius=12,
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.with_opacity(0.5, cor_borda)),
        heading_row_color=cor_fundo_secundario,
        heading_row_height=52,
        data_row_min_height=60,
        data_row_max_height=60,
    )
   
    def obter_cor_estado(estado):
        cores = {
            "A aguardar": "#F59E0B",
            "Em Avaliação": "#3B82F6",
            "Em intervenção": "#8B5CF6",
            "Pendente": "#EAB308",
            "Arquivado": "#6B7280",
            "Em vigilância": "#10B981",
        }
        return cores.get(estado, "#6B7280")
   
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
                border_radius=16,
            )
           
            # Botões de ação
            botoes_acao = ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY_ROUNDED,
                        icon_color=cor_primaria,
                        tooltip="Ver detalhes",
                        icon_size=20,
                        style=ft.ButtonStyle(
                            overlay_color=ft.Colors.with_opacity(0.1, cor_primaria),
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_color="#0EA5E9",
                        tooltip="Editar",
                        icon_size=20,
                        style=ft.ButtonStyle(
                            overlay_color=ft.Colors.with_opacity(0.1, "#0EA5E9"),
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED,
                        icon_color="#DC2626",
                        tooltip="Eliminar",
                        icon_size=20,
                        style=ft.ButtonStyle(
                            overlay_color=ft.Colors.with_opacity(0.1, "#DC2626"),
                        ),
                    ),
                ],
                spacing=0,
            )
           
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(a["nome"], size=14, weight=ft.FontWeight.W_600, color=cor_texto_escuro)),
                        ft.DataCell(ft.Text(a["tecnico"], size=14, weight=ft.FontWeight.W_500, color=cor_texto_medio)),
                        ft.DataCell(ft.Text(a["problema"], size=13, color=cor_texto_medio)),
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
   
    # === CARTÕES DE ESTATÍSTICAS COMPACTOS ===
    def criar_card_pequeno(titulo, valor, icone, cor):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=cor, size=18),
                        bgcolor=ft.Colors.with_opacity(0.1, cor),
                        border_radius=8,
                        padding=8,
                    ),
                    ft.Column(
                        [
                            ft.Text(str(valor), size=18, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Text(titulo, size=11, color=cor_texto_claro, weight=ft.FontWeight.W_500),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            bgcolor=cor_card,
            padding=12,
            border_radius=10,
            border=ft.border.all(1, cor_borda),
            expand=True,
        )
   
    # Contar alunos por estado
    def contar_por_estado(estado):
        return len([a for a in alunos if a["estado"] == estado])
   
    # Card grande - Total de Alunos
    card_total = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PEOPLE_ALT_ROUNDED, color=cor_primaria, size=40),
                    bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                    border_radius=16,
                    padding=14,
                ),
                ft.Text(str(len(alunos)), size=42, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                ft.Text("Total de Alunos", size=14, weight=ft.FontWeight.W_600, color=cor_texto_medio),
                ft.Text("Todos os registos", size=11, color=cor_texto_claro),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor=cor_card,
        padding=20,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
        ),
        border=ft.border.all(1, cor_borda),
        width=240,
    )
   
    # Grid de estados compacto (2 colunas x 3 linhas)
    grid_estados = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        criar_card_pequeno("A aguardar", contar_por_estado("A aguardar"), ft.Icons.PENDING_ACTIONS, "#F59E0B"),
                        criar_card_pequeno("Em Avaliação", contar_por_estado("Em Avaliação"), ft.Icons.ASSESSMENT, "#3B82F6"),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        criar_card_pequeno("Em intervenção", contar_por_estado("Em intervenção"), ft.Icons.PSYCHOLOGY, "#8B5CF6"),
                        criar_card_pequeno("Pendente", contar_por_estado("Pendente"), ft.Icons.SCHEDULE, "#EAB308"),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        criar_card_pequeno("Arquivado", contar_por_estado("Arquivado"), ft.Icons.ARCHIVE, "#6B7280"),
                        criar_card_pequeno("Em vigilância", contar_por_estado("Em vigilância"), ft.Icons.VISIBILITY, "#10B981"),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
        expand=True,
    )
   
    # Container com estatísticas
    secao_estatisticas = ft.Container(
        content=ft.Row(
            [
                card_total,
                grid_estados,
            ],
            spacing=16,
        ),
        height=200,
    )
   
    # === ÁREA DE CONTEÚDO PRINCIPAL ===
    conteudo_principal = ft.Container(
        expand=True,
        bgcolor=cor_fundo,
        padding=24,
        content=ft.Column(
            [
                # Estatísticas compactas
                secao_estatisticas,
               
                # Seção de filtros
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Lista de Registos",
                                                size=22,
                                                weight=ft.FontWeight.BOLD,
                                                color=cor_texto_escuro,
                                            ),
                                            ft.Text(
                                                f"{len(alunos)} registos no sistema",
                                                size=13,
                                                color=cor_texto_claro,
                                            ),
                                        ],
                                        spacing=2,
                                    ),
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Novo Registo",
                                        icon=ft.Icons.ADD_CIRCLE_ROUNDED,
                                        bgcolor=cor_primaria,
                                        color=ft.Colors.WHITE,
                                        height=46,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            elevation=2,
                                            overlay_color=cor_primaria_hover,
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(height=16),
                            ft.Row(
                                [filtro_nome, filtro_tecnico, filtro_estado],
                                spacing=12,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=cor_card,
                    padding=24,
                    border_radius=16,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=20,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                    ),
                    border=ft.border.all(1, cor_borda),
                ),
               
                # Tabela - MAIS VISÍVEL E MAIOR
                ft.Container(
                    content=ft.Column(
                        [tabela],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    bgcolor=cor_card,
                    padding=24,
                    border_radius=16,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=20,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                    ),
                    border=ft.border.all(1, cor_borda),
                    expand=True,
                ),
            ],
            spacing=16,
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
 