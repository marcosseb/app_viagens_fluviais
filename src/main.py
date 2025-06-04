import flet as ft
from routes import home, login, search, signup, payment, navigation, dashboard
from urllib.parse import urlparse

def main(page: ft.Page): 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400 
    page.window.height = 600 
    page.window.left = -400 
    page.window.top = 10 
    page.window.always_on_top = True
    page.title = "Teste de Applicativo"


    def route_change(e): 
        page.views.clear() 
        if page.route == "/login": 
            page.views.append(login.View(page)) 
        elif page.route == '/home': 
            page.views.append(home.View(page))
        elif page.route == "/cadastro":
            page.views.append(signup.View(page))
        elif page.route == "/search":
            page.views.append(search.View(page))
        elif page.route == "/payment":
            page.views.append(payment.View(page))
        elif page.route == "/navigation":
            page.views.append(navigation.View(page))
        elif page.route == "/dashboard":
            page.views.append(dashboard.View(page))
        page.update()

    page.on_route_change = route_change
    page.go("/home") # Change this to the initial route you want
    # page.go("/login")

    page.add(ft. Text("Testando"))

ft.app(main)
