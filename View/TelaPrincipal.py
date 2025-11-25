import flet as ft

from Models.AlunosModel import listarAlunos
from Models.EscolasModel import listarEscolas
from Models.TecnicoModel import listarTecnico
from Models.RegistoModel import listarRegistos


def PaginaPrincipal(page: ft.Page):

    tecnico_nome = page.session.get("tecnico_nome") or "Técnico"

    alunos = listarAlunos()
    escolas = listarEscolas()
    tecnicos = listarTecnico()
    registos = listarRegistos()

    # === CORES (tema escuro/roxo parecido com o Login) ===
    cor_primaria = "#8B5CF6"      # Roxo vibrante
    cor_secundaria = "#A78BFA"    # Roxo claro
    cor_roxo_escuro = "#6D28D9"
    cor_fundo = "#0F0F0F"         # Fundo escuro
    cor_card = "#121212"          # Card escuro
    cor_texto_claro = "#E5E7EB"
    cor_texto_medio = "#9CA3AF"
    cor_texto_escuro = "#D1D5DB"
    cor_borda = "#242424"

    # =======================================
    # CABEÇALHO
    # =======================================
    cabecalho = ft.Container(
        padding=ft.padding.symmetric(horizontal=28, vertical=16),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[cor_roxo_escuro, cor_primaria],
        ),
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
        ),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, color=ft.Colors.WHITE, size=30),
                            bgcolor=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
                            padding=10,
                            border_radius=10,
                        ),
                        ft.Column(
                            [
                                ft.Text("GAIE", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text(
                                    "Gestão Integrada de Alunos e Educação",
                                    size=12,
                                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
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
                                        color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
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
                                                ft.Text("Configurações", size=14, color=ft.Colors.WHITE),
                                            ],
                                            spacing=12,
                                        ),
                                        on_click=lambda e: page.go("/configuracoes"),
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#FF6B6B"),
                                                ft.Text("Terminar Sessão", size=14, color="#FF6B6B", weight=ft.FontWeight.W_600),
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
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                ),
            ]
        ),
    )

    # =======================================
    # MENU LATERAL
    # =======================================
    def criar_botao_menu(texto, icone, ativo=False, acao=None):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icone, color=ft.Colors.WHITE if ativo else cor_primaria, size=20),
                    ft.Text(
                        texto,
                        size=14,
                        weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.W_500,
                        color=ft.Colors.WHITE if ativo else cor_texto_claro,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
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
        border=ft.border.all(1, cor_borda),
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK)
        ),
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE_ROUNDED, color=cor_primaria, size=40),
                                bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                                padding=12,
                                border_radius=12,
                            ),
                            ft.Text("Menu Principal", size=18, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=ft.padding.only(bottom=18),
                ),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=12),

                criar_botao_menu("Dashboard", ft.Icons.DASHBOARD_ROUNDED, acao=lambda e: trocar_vista("dashboard")),
                criar_botao_menu("Alunos", ft.Icons.PEOPLE_ROUNDED, acao=lambda e: trocar_vista("alunos")),
                criar_botao_menu("Escolas", ft.Icons.SCHOOL_ROUNDED, acao=lambda e: trocar_vista("escolas")),
                criar_botao_menu("Registos", ft.Icons.ASSIGNMENT_ROUNDED, acao=lambda e: trocar_vista("registos")),
                criar_botao_menu("Técnicos", ft.Icons.PERSON_ROUNDED, acao=lambda e: trocar_vista("tecnicos")),

                ft.Container(expand=True),
                ft.Divider(height=1, color=cor_borda),
                ft.Container(height=10),

                criar_botao_menu("Configurações", ft.Icons.SETTINGS_ROUNDED, acao=lambda e: page.go("/Config")),

                ft.Container(
                    content=ft.Text("v1.0.0", size=11, color=cor_texto_medio, text_align=ft.TextAlign.CENTER),
                    padding=ft.padding.only(top=12),
                ),
            ],
            spacing=8,
        ),
    )

    # =======================================
    # ÁREA PRINCIPAL
    # =======================================
    conteudo_principal = ft.Container(expand=True, bgcolor=cor_fundo, padding=28, content=None)

    # =======================================
    # FUNÇÕES / VIEWS
    # =======================================

    def estilo_botao_acao(texto, icone, onclick):
        return ft.ElevatedButton(
            width=240,
            content=ft.Row(
                [
                    ft.Icon(icone, size=20, color=ft.Colors.WHITE),
                    ft.Text(texto, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=60),
                padding=ft.padding.symmetric(horizontal=22, vertical=12),
                bgcolor=cor_primaria,
                elevation=3,
            ),
            on_click=onclick,
        )

    # ==================================================
    # CARDS DO DASHBOARD
    # ==================================================
    def criar_card_grande(titulo, valor, icone, cor, subtitulo):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=cor, size=40),
                        bgcolor=ft.Colors.with_opacity(0.08, cor),
                        border_radius=14,
                        padding=14,
                    ),
                    ft.Text(str(valor), size=44, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ft.Text(titulo, size=16, weight=ft.FontWeight.W_600, color=cor_texto_medio),
                    ft.Text(subtitulo, size=12, color=cor_texto_medio),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=cor_card,
            padding=24,
            border_radius=14,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=18, color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK)
            ),
            border=ft.border.all(1, cor_borda),
            expand=True,
        )

    def criar_card_estado(titulo, valor, icone, cor):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icone, color=cor, size=28),
                        bgcolor=ft.Colors.with_opacity(0.08, cor),
                        border_radius=12,
                        padding=12,
                    ),
                    ft.Text(str(valor), size=28, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ft.Text(titulo, size=13, color=cor_texto_medio, weight=ft.FontWeight.W_500),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=cor_card,
            padding=18,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=12, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
            expand=True,
        )

    # ==================================================
    # DASHBOARD VIEW
    # ==================================================
    dashboard_view = ft.Column(
        [
            ft.Row(
                [
                    criar_card_grande("Total de Alunos", len(alunos), ft.Icons.PEOPLE_ALT_ROUNDED, cor_primaria, "Registados no sistema"),
                    criar_card_grande("Total de Registos", len(registos), ft.Icons.ASSIGNMENT_ROUNDED, cor_secundaria, "Todos os registos"),
                    criar_card_grande("Total de Escolas", len(escolas), ft.Icons.SCHOOL_ROUNDED, "#10B981", "Escolas registadas"),
                ],
                spacing=20,
            ),

            ft.Container(height=18),

            ft.Text("Estados dos Processos", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
            ft.Text("Distribuição dos processos por estado atual", size=12, color=cor_texto_medio),
            ft.Container(height=14),

            ft.Column(
                [
                    ft.Row(
                        [
                            criar_card_estado("A Aguardar", len([r for r in registos if r.get("idEstado") == 1]), ft.Icons.PENDING_ACTIONS, "#F59E0B"),
                            criar_card_estado("Em Avaliação", len([r for r in registos if r.get("idEstado") == 2]), ft.Icons.ASSESSMENT, "#3B82F6"),
                        ],
                        spacing=16,
                    ),

                    ft.Row(
                        [
                            criar_card_estado("Em Intervenção", len([r for r in registos if r.get("idEstado") == 3]), ft.Icons.PSYCHOLOGY, cor_primaria),
                            criar_card_estado("Pendente", len([r for r in registos if r.get("idEstado") == 4]), ft.Icons.SCHEDULE, "#EAB308"),
                        ],
                        spacing=16,
                    ),

                    ft.Row(
                        [
                            criar_card_estado("Arquivado", len([r for r in registos if r.get("idEstado") == 5]), ft.Icons.ARCHIVE, "#6B7280"),
                            criar_card_estado("Em Vigilância", len([r for r in registos if r.get("idEstado") == 6]), ft.Icons.VISIBILITY, "#10B981"),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=12,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
    )

    # ==================================================
    # ALUNOS VIEW
    # ==================================================
    def criar_card_aluno(aluno):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=28),
                        bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Column(
                        [
                            ft.Text(aluno.get("NomeAluno", ""), size=15, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.SCHOOL, size=14, color=cor_texto_medio),
                                    ft.Text(f"{aluno.get('NomeEscola', 'N/A')}", size=12, color=cor_texto_medio),
                                    ft.Container(width=10),
                                    ft.Icon(ft.Icons.MEETING_ROOM, size=14, color=cor_texto_medio),
                                    ft.Text(f"{aluno.get('Ano', 'N/A')}º - Turma {aluno.get('Turma', 'N/A')}", size=12, color=cor_texto_medio),
                                ],
                                spacing=6,
                            ),
                        ],
                        spacing=6,
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
                                ),
                            ),
                        ],
                        spacing=6,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=16,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK)
            ),
        )

    def get_alunos_view(filtered_alunos):
        if filtered_alunos:
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Lista de Alunos", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ft.Text(f"Total: {len(filtered_alunos)} alunos encontrados", size=12, color=cor_texto_medio),
                                ],
                                spacing=4,
                            ),
                            ft.Container(expand=True),
                            # Botão padronizado igual aos outros
                            estilo_botao_acao("Adicionar Aluno", ft.Icons.ADD_CIRCLE, lambda e: page.go("/CriarAluno")),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=16),
                    ft.Column(
                        [criar_card_aluno(a) for a in filtered_alunos],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=10,
                expand=True,
            )

        # NENHUM ALUNO
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, size=100, color=cor_texto_medio),
                    ft.Text("Nenhum aluno encontrado", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ft.Text("Comece por adicionar o primeiro registo ao sistema", size=13, color=cor_texto_medio),
                    ft.Container(height=12),
                    estilo_botao_acao("Adicionar Primeiro Aluno", ft.Icons.ADD_CIRCLE, lambda e: page.go("/CriarAluno")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    # ==================================================
    # ESCOLAS VIEW
    # ==================================================
    def criar_card_escola(escola):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.SCHOOL, color=cor_primaria, size=28),
                        bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Column(
                        [
                            ft.Text(escola.get("NomeEscola", ""), size=15, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ft.Text(f"ID: {escola.get('idEscola', 'N/A')}", size=12, color=cor_texto_medio),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#F59E0B",
                        tooltip="Editar",
                        on_click=lambda e, a=escola: (
                            page.session.set("escola_editar_id", a.get("idEscola")),
                            page.go("/EditarEscola")
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=14,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
            ),
        )

    def build_escolas_view():
        if escolas:
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Lista de Escolas", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                    ft.Text(f"Total: {len(escolas)} escolas registadas", size=12, color=cor_texto_medio),
                                ],
                                spacing=4,
                            ),
                            ft.Container(expand=True),
                            estilo_botao_acao("Adicionar Escola", ft.Icons.ADD_CIRCLE, lambda e: page.go("/criar-escola")),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=16),
                    ft.Column(
                        [criar_card_escola(e) for e in escolas],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=10,
                expand=True,
            )

        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.SCHOOL_OUTLINED, size=100, color=cor_texto_medio),
                            ft.Text("Nenhuma escola registada", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ft.Text("A lista de escolas está vazia", size=13, color=cor_texto_medio),
                            ft.Container(height=12),
                            estilo_botao_acao("Adicionar Primeira Escola", ft.Icons.ADD_CIRCLE, lambda e: page.go("/criar-escola")),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=10,
            expand=True,
        )

    # ==================================================
    # TECNICOS VIEW
    # ==================================================
    def criar_card_tecnico(tecnico):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=cor_primaria, size=28),
                        bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Column(
                        [
                            # chave ajustada para manter compatibilidade
                            ft.Text(tecnico.get("NomeTecnico", tecnico.get("nomeTecnico", "")), size=15, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ft.Text(tecnico.get("Funcao", ""), size=12, color=cor_texto_medio),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Row([], spacing=5),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=14,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
            ),
        )

    tecnicos_view = (
        ft.Column(
            [criar_card_tecnico(t) for t in tecnicos],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )
        if tecnicos
        else ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ENGINEERING_OUTLINED, size=100, color=cor_texto_medio),
                    ft.Text("Nenhum técnico registado", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ft.Text("A lista de técnicos está vazia", size=13, color=cor_texto_medio),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )

    # ==================================================
    # REGISTOS VIEW
    # ==================================================
    def criar_card_registo(registo):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.ASSIGNMENT, color=cor_primaria, size=28),
                        bgcolor=ft.Colors.with_opacity(0.08, cor_primaria),
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Column(
                        [
                            ft.Text(f"Registo #{registo.get('nPIA', 'N/A')}", size=15, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PERSON, size=14, color=cor_texto_medio),
                                    ft.Text(f"Aluno: {registo.get('NomeAluno', 'N/A')}", size=12, color=cor_texto_medio),
                                    ft.Container(width=10),
                                    ft.Icon(ft.Icons.FLAG, size=14, color=cor_texto_medio),
                                    ft.Text(f"Estado: {registo.get('Estado', 'N/A')}", size=12, color=cor_texto_medio),
                                ],
                                spacing=6,
                            ),
                            ft.Text(
                                f"Data: {registo.get('DataEntradaSPO', 'N/A')} | Técnico: {registo.get('NomeTecnico', 'N/A')}",
                                size=11,
                                color=cor_texto_medio,
                            ),
                        ],
                        spacing=6,
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
                                    page.go("/EditarRegisto"),
                                ),
                            ),
                        ],
                        spacing=6,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=cor_card,
            padding=14,
            border_radius=12,
            border=ft.border.all(1, cor_borda),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
            ),
        )

    registos_view = (
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Lista de Registo", size=22, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                                ft.Text(f"Total: {len(registos)} Registo encontrados", size=12, color=cor_texto_medio),
                            ],
                            spacing=4,
                        ),
                        ft.Container(expand=True),
                        estilo_botao_acao("Adicionar Registo", ft.Icons.ADD_CIRCLE, lambda e: page.go("/criar-registo")),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=16),
                ft.Column(
                    [criar_card_registo(r) for r in registos],
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=10,
            expand=True,
        )
        if registos
        else ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, size=100, color=cor_texto_medio),
                    ft.Text("Nenhum registo criado", size=20, weight=ft.FontWeight.BOLD, color=cor_texto_claro),
                    ft.Text("Comece por adicionar o primeiro registo", size=13, color=cor_texto_medio),
                    ft.Container(height=12),
                    estilo_botao_acao("Adicionar Primeiro Registo", ft.Icons.ADD, lambda e: page.go("/criar-registo")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )

    # ==================================================
    # FUNÇÃO DE TROCA DE VISTA
    # ==================================================
    def trocar_vista(vista):
        nonlocal alunos, escolas, tecnicos, registos

        try:
            alunos = listarAlunos()
            escolas = listarEscolas()
            tecnicos = listarTecnico()
            registos = listarRegistos()
        except Exception as err:
            print("Erro ao recarregar dados:", err)

        if vista == "dashboard":
            conteudo_principal.content = dashboard_view
        elif vista == "alunos":
            conteudo_principal.content = get_alunos_view(alunos)
        elif vista == "escolas":
            conteudo_principal.content = build_escolas_view()
        elif vista == "registos":
            conteudo_principal.content = registos_view
        elif vista == "tecnicos":
            conteudo_principal.content = tecnicos_view

        page.update()

    # =======================================
    # LAYOUT FINAL
    # =======================================
    layout = ft.Row([menu_lateral, conteudo_principal], spacing=20, expand=True)
    conteudo_principal.content = dashboard_view

    return ft.View(
        route="/pagina-principal",
        controls=[
            cabecalho,
            ft.Container(content=layout, padding=20, bgcolor=cor_fundo, expand=True),
        ],
        bgcolor=cor_fundo,
    )