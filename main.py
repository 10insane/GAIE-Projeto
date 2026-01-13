import flet as ft
from View.Login.Login import LoginView
from View.TelaPrincipal import PaginaPrincipal
from View.Tecnico.CriarTecnicoView import CreateTecnico
from View.Alunos.CriarAluno import PaginaCriarAluno
from View.Escola.CriarEscolaView import CriarEscola
from View.Registo.CriarRegisto import PaginaCriarRegisto
from View.Alunos.EditarAluno import PaginaEditarAluno
from View.Escola.EditarEscola import PaginaEditarEscola
from View.Registo.EditarRegisto import PaginaEditarRegisto
from View.RegistosAdminPage import RegistosAdminPage
from View.Config.Config import PainelAdmin
from View.TelaPrincipalAdmin import PaginaPrincipalAdmin
from View.PaginaPrincipal.maisDetalhesRegisto import MaisDetalhesRegistos
from View.PaginaPrincipal.maisDetalhesAlunos import DetalhesAluno
from View.PaginaPrincipal.TecnicoPerfil import PerfilTecnico
from View.PaginaPrincipal.maisDetalhesEscolas import DetalhesEscola

def main(page: ft.Page):
    page.title = "GAIE - Psicologia"
    page.theme_mode = ft.ThemeMode.DARK
    page.session.clear()

    protected_routes = [
        "/pagina-principal", "/criar-tecnico", "/CriarAluno", "/criar-escola", "/criar-registo",
        "/EditarAluno", "/EditarEscola", "/EditarRegisto", "/registos", "/Config", "/TelaPrincipalAdmin",
        "/maisDetalhesRegisto", "/maisDetalhesAlunos", "/TecnicoPerfil", "/DetalhesEscola"
    ]

    def get_view(route, page):
        if route == "/login":
            return LoginView(page)
        elif route == "/pagina-principal":
            return PaginaPrincipal(page)
        elif route == "/criar-tecnico":
            return CreateTecnico(page)
        elif route == "/CriarAluno": 
            return PaginaCriarAluno(page) 
        elif route == "/criar-escola": 
            return CriarEscola(page)  
        elif route=="/criar-registo":
            return PaginaCriarRegisto(page)
        elif route=="/EditarAluno":
            return PaginaEditarAluno(page)
        elif route=="/EditarEscola":
            return PaginaEditarEscola(page)
        elif route=="/EditarRegisto":
            return PaginaEditarRegisto(page)
        elif route=="/registos":
            return RegistosAdminPage(page)
        elif route=="/Config":
            return PainelAdmin(page)
        elif route=="/TelaPrincipalAdmin":
            return PaginaPrincipalAdmin(page)
        elif route=="/maisDetalhesRegisto":
            return MaisDetalhesRegistos(page)
        elif route =="/maisDetalhesAlunos":
            return DetalhesAluno(page)
        elif route =="/maisDetalhesEscolas":
            return DetalhesEscola(page)
        elif route == "/TecnicoPerfil":
            tecnico = page.session.get("tecnico")
            return ft.View(
                "/TecnicoPerfil",
                controls=[
                    ft.Container(
                        content=PerfilTecnico(tecnico, page),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ]
            )
        else:
            return LoginView(page)

    def navigate(route):
        if route in protected_routes and not page.session.get("usuario_tipo"):
            route = "/login"
        view = get_view(route, page)
        page.views.clear()
        page.views.append(view)
        page.update()

    # Override page.go to use navigate
    page.go = navigate

    # Disable route change and view pop to prevent URL changes
    page.on_route_change = None
    page.on_view_pop = None

    # Start with login
    navigate("/login")


ft.app(target=main, view=ft.WEB_BROWSER, route_url_strategy="hash")