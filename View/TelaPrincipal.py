import flet as ft
from Models.AlunosModel import listarAlunos
from Models.EscolasModel import listarEscolas, deletarEscola
from Models.TecnicoModel import listarTecnico
from Models.RegistoModel import listarRegistos

def PaginaPrincipal(page: ft.Page):
    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"
    alunos = listarAlunos()
    escolas = listarEscolas()
    tecnicos = listarTecnico()
    registos = listarRegistos()
    print("REGISTOS:", registos)
    

    # === CORES ===
    cor_primaria = "#1E40AF"
    cor_fundo = "#F8FAFC"
    cor_card = "#FFFFFF"
    cor_texto_escuro = "#0F172A"
    cor_texto_medio = "#334155"
    cor_texto_claro = "#64748B"
    cor_borda = "#E2E8F0"

    # === CABEÇALHO ===
    cabecalho = ft.Container(
        padding=ft.padding.symmetric(horizontal=30, vertical=18),
        bgcolor=cor_primaria,
        shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
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
                                ft.Text("GAIE", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
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
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(tecnico_nome, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
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
                                                ft.Icon(ft.Icons.PERSON_ROUNDED, size=20, color=ft.Colors.WHITE),
                                                ft.Text("Meu Perfil", size=14, color=ft.Colors.WHITE),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/perfil"),
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.SETTINGS_ROUNDED, size=20, color=ft.Colors.WHITE),
                                                ft.Text("Configurações", size=14,color=ft.Colors.WHITE),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/configuracoes"),
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#DC2626"),
                                                ft.Text(
                                                    "Terminar Sessão",
                                                    size=14,
                                                    color="#DC2626",
                                                    weight=ft.FontWeight.W_600,
                                                ),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/login"),
                                    ),
                                ],
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    border_radius=30,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                ),
            ]
        ),
    )

    # === MENU LATERAL ===
    def criar_botao_menu(texto, icone, rota, ativo=False, acao=None):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icone, color=ft.Colors.WHITE if ativo else cor_primaria, size=22),
                    ft.Text(
                        texto,
                        size=15,
                        weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.W_500,
                        color=ft.Colors.WHITE if ativo else cor_texto_escuro,
                    ),
                ],
                spacing=14,
            ),
            padding=16,
            border_radius=12,
            ink=True,
            on_click=acao,
            bgcolor=cor_primaria if ativo else "transparent",
        )

    menu_lateral = ft.Container(
        width=260,
        bgcolor=cor_card,
        padding=24,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.09, ft.Colors.BLACK)
        ),
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE_ROUNDED, color=cor_primaria, size=48),
                                bgcolor=ft.Colors.with_opacity(0.09, cor_primaria),
                                padding=14,
                                border_radius=16,
                            ),
                            ft.Text("Menu Principal", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=15),
                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD_ROUNDED, "/pagina-principal", acao=lambda e: trocar_vista("dashboard")),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE_ROUNDED, "/alunos", acao=lambda e: trocar_vista("alunos")),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL_ROUNDED, "/escolas", acao=lambda e: trocar_vista("escolas")),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT_ROUNDED, "/registos", acao=lambda e: trocar_vista("registos")),
                criar_botao_menu("Técnicos", ft.Icons.PERSON_ROUNDED, "/tecnicos", acao=lambda e: trocar_vista("tecnicos")),
                ft.Container(expand=True),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=10),
                criar_botao_menu("Configurações", ft.Icons.SETTINGS_ROUNDED, "/configuracoes", acao=lambda e: page.go("/Config")),
                ft.Container(
                    content=ft.Text("v1.0.0", size=11, color=cor_texto_claro, text_align=ft.TextAlign.CENTER),
                    padding=ft.padding.only(top=15),
                ),
            ],
            spacing=6,
        ),
    )

    # === FUNÇÃO DE TROCA DE VISTA ===
    conteudo_principal = ft.Container(expand=True, bgcolor=cor_fundo, padding=30, content=None)

    # === DASHBOARD VIEW ===
    def criar_card_grande(titulo, valor, icone, cor, subtitulo):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=cor, size=48),
                        bgcolor=ft.Colors.with_opacity(0.1, cor),
                        border_radius=20,
                        padding=20,
                    ),
                    ft.Text(str(valor), size=64, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                    ft.Text(titulo, size=20, weight=ft.FontWeight.W_600, color=cor_texto_medio),
                    ft.Text(subtitulo, size=14, color=cor_texto_claro),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=cor_card,
            padding=40,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=25, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
            ),
            border=ft.border.all(1, cor_borda),
            expand=True,
        )

    def criar_card_estado(titulo, valor, icone, cor):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=cor, size=32),
                        bgcolor=ft.Colors.with_opacity(0.1, cor),
                        border_radius=14,
                        padding=16,
                    ),
                    ft.Text(str(valor), size=40, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                    ft.Text(
                        titulo,
                        size=15,
                        color=cor_texto_medio,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=cor_card,
            padding=28,
            border_radius=16,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=15, color=ft.Colors.with_opacity(0.07, ft.Colors.BLACK)
            ),
            expand=True,
        )

    dashboard_view = ft.Column(
        [
            ft.Row(
                [
                    criar_card_grande("Total de Alunos", len(alunos), ft.Icons.PEOPLE_ALT_ROUNDED, cor_primaria, "Registados no sistema"),
                    criar_card_grande("Total de Processos", len(registos), ft.Icons.ASSIGNMENT_ROUNDED, "#8B5CF6", "Todos os registos"),
                    criar_card_grande("Total de Escolas", len(escolas), ft.Icons.SCHOOL_ROUNDED, "#10B981", "Escolas registadas"),
                ],
                spacing=28,
            ),
            ft.Container(height=30),
            ft.Text("Estados dos Processos", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
            ft.Text("Distribuição dos processos por estado atual", size=14, color=cor_texto_claro),
            ft.Container(height=18),
            ft.Column(
                [
                ft.Row(
    [
        criar_card_estado("A Aguardar", 
                          len([r for r in registos if r.get("idEstado") == 1]), 
                          ft.Icons.PENDING_ACTIONS, "#F59E0B"),

        criar_card_estado("Em Avaliação", 
                          len([r for r in registos if r.get("idEstado") == 2]), 
                          ft.Icons.ASSESSMENT, "#3B82F6"),
    ],
    spacing=20,
),

ft.Row(
    [
        criar_card_estado("Em Intervenção", 
                          len([r for r in registos if r.get("idEstado") == 3]), 
                          ft.Icons.PSYCHOLOGY, "#8B5CF6"),

        criar_card_estado("Pendente", 
                          len([r for r in registos if r.get("idEstado") == 4]), 
                          ft.Icons.SCHEDULE, "#EAB308"),
    ],
    spacing=20,
),

ft.Row(
    [
        criar_card_estado("Arquivado", 
                          len([r for r in registos if r.get("idEstado") == 5]), 
                          ft.Icons.ARCHIVE, "#6B7280"),

        criar_card_estado("Em Vigilância", 
                          len([r for r in registos if r.get("idEstado") == 6]), 
                          ft.Icons.VISIBILITY, "#10B981"),
    ],
    spacing=20,
),

                ],
                spacing=20,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # === ALUNOS VIEW ===
    def criar_card_aluno(aluno):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=32),
                        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(aluno.get("NomeAluno", ""), size=16, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.SCHOOL, size=14, color=cor_texto_claro),
                                    ft.Text(f"{aluno.get('NomeEscola', 'N/A')}", size=13, color=cor_texto_medio),
                                    ft.Container(width=10),
                                    ft.Icon(ft.Icons.MEETING_ROOM, size=14, color=cor_texto_claro),
                                    ft.Text(
                                        f"{aluno.get('Ano', 'N/A')}º - Turma {aluno.get('Turma', 'N/A')}",
                                        size=13,
                                        color=cor_texto_medio,
                                    ),
                                ],
                                spacing=5,
                            ),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#F59E0B",
                                tooltip="Editar aluno",
                                on_click=lambda e, a=aluno: (
                                 page.session.set("aluno_editar_id", a["nProcessoAluno"]),
                                 page.go("/EditarAluno")
                               )
                               ,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#DC2626",
                                tooltip="Excluir aluno",
                                on_click=lambda e, a=aluno: excluir_aluno_modal(a),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
        )

    def excluir_aluno_modal(aluno):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o aluno {aluno.get('NomeAluno')}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.close()),
                ft.ElevatedButton("Excluir", bgcolor="#DC2626", color=ft.Colors.WHITE, on_click=lambda e: page.dialog.close()),
            ],
        )
        page.dialog.open = True
        page.update()

    search_alunos = ft.TextField(
        label="Pesquisar alunos (nome, escola, ano, turma)",
        prefix_icon=ft.Icons.SEARCH,
        width=400,
        on_change=lambda e: update_alunos_view(e.control.value),
    )

    def get_alunos_view(filtered_alunos):
        if filtered_alunos:
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Lista de Alunos", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                    ft.Text(f"Total: {len(filtered_alunos)} alunos encontrados", size=14, color=cor_texto_claro),
                                ],
                                spacing=5,
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.ADD, size=20),
                                        ft.Text("Novo Aluno", size=15, weight=ft.FontWeight.W_600),
                                    ],
                                    spacing=8,
                                ),
                                bgcolor=cor_primaria,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: page.go("/CriarAluno"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=10),
                    search_alunos,
                    ft.Container(height=20),
                    ft.Column([criar_card_aluno(a) for a in filtered_alunos], spacing=15, scroll=ft.ScrollMode.AUTO),
                ],
                spacing=10,
                expand=True,
            )
        else:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PEOPLE_OUTLINED, size=120, color=cor_texto_claro),
                        ft.Text("Nenhum aluno encontrado", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                        ft.Text("Tente ajustar os termos de pesquisa", size=15, color=cor_texto_claro),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )

    def update_alunos_view(query):
        if query.strip():
            filtered = [a for a in alunos if any(query.lower() in str(a.get(key, "")).lower() for key in ["NomeAluno", "NomeEscola", "Ano", "Turma"])]
        else:
            filtered = alunos
        conteudo_principal.content = get_alunos_view(filtered)
        page.update()

    alunos_view = get_alunos_view(alunos)

    # === ESCOLAS VIEW ===
    def criar_card_escola(escola):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.SCHOOL, color=cor_primaria, size=32),
                        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(escola.get("NomeEscola", ""), size=16, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Text(f"ID: {escola.get('IdEscola', 'N/A')}", size=13, color=cor_texto_medio),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#F59E0B",
                                tooltip="Editar",
                                on_click=lambda e, a=escola: (
                                 page.session.set("escola_editar_id", a["idEscola"]),
                                 page.go("/EditarEscola")
                               )
                               ,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#DC2626",
                                tooltip="Excluir",
                                on_click=lambda e, esc=escola: excluir_escola(esc),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
        )

    def excluir_escola(escola):
        sucesso = deletarEscola(escola.get("IdEscola"))
        if sucesso:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Escola {escola.get('NomeEscola')} removida com sucesso!"),
                bgcolor="#16A34A",
                duration=3000,
            )
            trocar_vista("escolas")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro ao tentar remover a escola."),
                bgcolor="#DC2626",
                duration=3000,
            )
        page.snack_bar.open = True
        page.update()

    if escolas:
        escolas_view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Lista de Escolas", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                ft.Text(f"Total: {len(escolas)} escolas registadas", size=14, color=cor_texto_claro),
                            ],
                            spacing=5,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ADD, size=20),
                                    ft.Text("Adicionar Escola", size=15, weight=ft.FontWeight.W_600),
                                ],
                                spacing=8,
                            ),
                            bgcolor=cor_primaria,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: page.go("/criar-escola"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                ft.Column([criar_card_escola(e) for e in escolas], spacing=15, scroll=ft.ScrollMode.AUTO),
            ],
            spacing=10,
            expand=True,
        )
    else:
        escolas_view = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.SCHOOL_OUTLINED, size=120, color=cor_texto_claro),
                            ft.Text("Nenhuma escola registada", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Text("A lista de escolas está vazia", size=15, color=cor_texto_claro),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.ADD_CIRCLE, size=24),
                                        ft.Text("Adicionar Primeira Escola", size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10,
                                ),
                                bgcolor=cor_primaria,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: page.go("/criar-escola"),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=10,
            expand=True,
        )

    # === TECNICOS VIEW ===
    def criar_card_tecnico(tecnico):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=32),
                        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(tecnico.get("NomeTecnico", ""), size=16, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Text(tecnico.get("Funcao", ""), size=13, color=cor_texto_medio),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Row([], spacing=5),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
        )

    if tecnicos:
        tecnicos_view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Lista de Técnicos", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                ft.Text(f"Total: {len(tecnicos)} técnicos registados", size=14, color=cor_texto_claro),
                            ],
                            spacing=5,
                        ),
                        ft.Container(expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                ft.Column([criar_card_tecnico(t) for t in tecnicos], spacing=15, scroll=ft.ScrollMode.AUTO),
            ],
            spacing=10,
            expand=True,
        )
    else:
        tecnicos_view = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ENGINEERING_OUTLINED, size=120, color=cor_texto_claro),
                    ft.Text("Nenhum técnico registado", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                    ft.Text("A lista de técnicos está vazia no momento", size=15, color=cor_texto_claro),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    # === REGISTOS VIEW ===
    def criar_card_registo(registo):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT, color=cor_primaria, size=32),
                        bgcolor=ft.Colors.with_opacity(0.1, cor_primaria),
                        padding=12,
                        border_radius=12,
                    ),
                    ft.Column(
                        [
                            ft.Text(f"Registo #{registo.get('nPIA', 'N/A')}", size=16, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PERSON, size=14, color=cor_texto_claro),
                                    ft.Text(f"Aluno: {registo.get('NomeAluno', 'N/A')}", size=13, color=cor_texto_medio),
                                    ft.Container(width=10),
                                    ft.Icon(ft.Icons.FLAG, size=14, color=cor_texto_claro),
                                    ft.Text(f"Estado: {registo.get('Estado', 'N/A')}", size=13, color=cor_texto_medio),

                                ],
                                spacing=5,
                            ),
                            ft.Text(f"Data: {registo.get('DataEntradaSPO', 'N/A')} | Técnico: {registo.get('NomeTecnico', 'N/A')}", size=12, color=cor_texto_claro),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.VISIBILITY,
                                icon_color=cor_primaria,
                                tooltip="Ver detalhes",
                                on_click=lambda e, r=registo: page.go(f"/registo/{r.get('idRegisto')}"),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#F59E0B",
                                tooltip="Editar",
                                on_click=lambda e, a=registo: (                                          
                                 page.session.set("registo_editar_id", a["nPIA"]),
                                 page.go("/EditarRegisto")
                               )
                               ,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
        )

    if registos:
        registos_view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Lista de Registos", size=28, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                                ft.Text(f"Total: {len(registos)} registos", size=14, color=cor_texto_claro),
                            ],
                            spacing=5,
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ADD, size=20),
                                    ft.Text("Novo Registo", size=15, weight=ft.FontWeight.W_600),
                                ],
                                spacing=8,
                            ),
                            bgcolor=cor_primaria,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: page.go("/criar-registo"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                ft.Column([criar_card_registo(r) for r in registos], spacing=15, scroll=ft.ScrollMode.AUTO),
            ],
            spacing=10,
            expand=True,
        )
    else:
        registos_view = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, size=120, color=cor_texto_claro),
                    ft.Text("Nenhum registo criado", size=24, weight=ft.FontWeight.BOLD, color=cor_texto_escuro),
                    ft.Text("Comece por adicionar o primeiro registo ao sistema", size=15, color=cor_texto_claro),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.ADD_CIRCLE, size=24),
                                ft.Text("Criar Primeiro Registo", size=16, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10,
                        ),
                        bgcolor=cor_primaria,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: page.go("/criar-registo"),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    # === TROCA DE VISTAS ===
    def trocar_vista(vista):
        if vista == "dashboard":
            conteudo_principal.content = dashboard_view
        elif vista == "alunos":
            conteudo_principal.content = alunos_view
        elif vista == "escolas":
            conteudo_principal.content = escolas_view
        elif vista == "registos":
            conteudo_principal.content = registos_view
        elif vista == "tecnicos":
            conteudo_principal.content = tecnicos_view
        page.update()

    # === LAYOUT PRINCIPAL ===
    layout = ft.Row([menu_lateral, conteudo_principal], spacing=20, expand=True)
    conteudo_principal.content = dashboard_view

    return ft.View(
        route="/pagina-principal",
        controls=[cabecalho, ft.Container(content=layout, padding=20, bgcolor=cor_fundo, expand=True)],
        bgcolor=cor_fundo,
    )
