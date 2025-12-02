import flet as ft
from Models.AlunosModel import listarAlunos
from Models.EscolasModel import listarEscolas
from Models.TecnicoModel import listarTecnico
from Models.RegistoModel import listarRegistos

from View.PaginaPrincipal.estilos import cor_fundo
from View.PaginaPrincipal.cabecalho import criar_cabecalho
from View.PaginaPrincipal.menu_lateral import criar_menu_lateral
from View.PaginaPrincipal.dashboard_view import criar_dashboard_view
from View.PaginaPrincipal.alunos_view import criar_alunos_view
from View.PaginaPrincipal.escolas_view import criar_escolas_view
from View.PaginaPrincipal.tecnicos_view import criar_tecnicos_view
from View.PaginaPrincipal.registos_view import criar_registos_view


def PaginaPrincipal(page: ft.Page):

    conteudo_principal = ft.Container(expand=True)

    def trocar_vista(vista):

        alunos = listarAlunos()
        escolas = listarEscolas()
        tecnicos = listarTecnico()
        registos = listarRegistos()

        if vista == "dashboard":
            conteudo_principal.content = criar_dashboard_view( alunos, escolas, registos)
        elif vista == "alunos":
            conteudo_principal.content = criar_alunos_view(alunos, page)
        elif vista == "escolas":
            conteudo_principal.content = criar_escolas_view(escolas, page)
        elif vista == "tecnicos":
            conteudo_principal.content = criar_tecnicos_view(tecnicos)
        elif vista == "registos":
            conteudo_principal.content = criar_registos_view(registos, page)

        page.update()

    # Layout final
    layout = ft.Row(
        [
            criar_menu_lateral(page, trocar_vista),
            conteudo_principal
        ],
        spacing=20,
        expand=True
    )

    trocar_vista("dashboard")  # vista inicial

    return ft.View(
        route="/pagina-principal",
        controls=[
            criar_cabecalho(page),
            ft.Container(content=layout, padding=20, bgcolor=cor_fundo, expand=True),
        ],
        bgcolor=cor_fundo,
    )
