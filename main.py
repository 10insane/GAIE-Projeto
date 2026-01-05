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
from View.Config.Config import PainelAdmin
from View.TelaPrincipalAdmin import PaginaPrincipalAdmin
from View.PaginaPrincipal.maisDetalhesRegisto import MaisDetalhesRegistos
from View.PaginaPrincipal.maisDetalhesAlunos import DetalhesAluno
from View.PaginaPrincipal.TecnicoPerfil import PerfilTecnico

def main(page: ft.Page):
    page.title = "GAIE - Psicologia"
    page.theme_mode = ft.ThemeMode.DARK
    page.session.clear()

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        
        route = page.route

        if route == "/login":
            view = LoginView(page)
        elif route == "/pagina-principal":
            view = PaginaPrincipal(page)
        elif route == "/criar-tecnico":
            view = CreateTecnico(page)
        elif route == "/CriarAluno": 
            view = PaginaCriarAluno(page) 
        elif route == "/criar-escola": 
            view = CriarEscola(page)  
        elif route=="/criar-registo":
            view= PaginaCriarRegisto(page)
        elif route=="/EditarAluno":
            view= PaginaEditarAluno(page)
        elif route=="/EditarEscola":
            view= PaginaEditarEscola(page)
        elif route=="/EditarRegisto":
            view= PaginaEditarRegisto(page)
        elif route=="/Config":
            view= PainelAdmin(page)
        elif route=="/TelaPrincipalAdmin":
            view= PaginaPrincipalAdmin(page)
        elif route=="/maisDetalhesRegisto":
            view= MaisDetalhesRegistos(page)
        elif route =="/maisDetalhesAlunos":
            view= DetalhesAluno(page)
        elif route == "/TecnicoPerfil":
          tecnico = page.session.get("tecnico")

          view = ft.View(
         "/TecnicoPerfil",
         controls=[
            ft.Container(
                content=PerfilTecnico(tecnico),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]
    )

        else:
            view = LoginView(page)  

        page.views.append(view)
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/login")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/login")


ft.app(target=main, view=ft.WEB_BROWSER)
