import flet as ft
from View.Login import LoginView
from View.TelaPrincipal import PaginaPrincipal
from View.CriarTecnicoView import CreateTecnico
from View.CriarAluno import PaginaCriarAluno
from View.CriarEscolaView import CriarEscola
from View.CriarRegisto import PaginaCriarRegisto
from View.EditarAluno import PaginaEditarAluno
from View.EditarEscola import PaginaEditarEscola
from View.EditarRegisto import PaginaEditarRegisto



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
