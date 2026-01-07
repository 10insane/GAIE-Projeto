import flet as ft
from Models.AlunosModel import listarAlunos
from Models.EscolasModel import listarEscolas
from Models.TecnicoModel import listarTecnico
from Models.RegistoModel import listarRegistos

from View.PaginaPrincipalAdmin.estilosAdmin import cor_fundo
from View.PaginaPrincipalAdmin.cabecalhoAdmin import criar_cabecalho
from View.PaginaPrincipalAdmin.menu_lateralAdmin import criar_menu_lateral
from View.PaginaPrincipalAdmin.dashboard_viewAdmin import criar_dashboard_viewAdmin
from View.PaginaPrincipalAdmin.alunos_viewAdmin import criar_alunos_view
from View.PaginaPrincipalAdmin.escolas_viewAdmin import criar_escolas_view
from View.PaginaPrincipalAdmin.tecnicos_viewAdmin import criar_tecnicos_view
from View.PaginaPrincipalAdmin.registos_viewAdmin import criar_registos_view


def PaginaPrincipalAdmin(page: ft.Page):

    conteudo_principal = ft.Container(expand=True)

    def trocar_vista(vista):

        alunos = listarAlunos()
        escolas = listarEscolas()
        tecnicos = listarTecnico()
        registos = listarRegistos()

        if vista == "dashboardAdmin":
            conteudo_principal.content = criar_dashboard_viewAdmin(page, alunos, escolas, registos)
        elif vista == "alunos":
            conteudo_principal.content = criar_alunos_view(alunos, page)
        elif vista == "escolas":
            conteudo_principal.content = criar_escolas_view(escolas, page)
        elif vista == "tecnicos":
            conteudo_principal.content = criar_tecnicos_view(tecnicos, page)
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

    trocar_vista("dashboardAdmin")  # vista inicial

    return ft.View(
        route="/PaginaPrincipalAdmin",
        controls=[
            criar_cabecalho(page),
            ft.Container(content=layout, padding=20, bgcolor=cor_fundo, expand=True),
        ],
        bgcolor=cor_fundo,
    )
