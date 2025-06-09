import flet as ft
from routes import home, login, search, signup, payment, navigation, selection, admin_home, passagens, \
            portos, embarcacoes, assentos, passageiros, viagens
from urllib.parse import urlparse

def main(page: ft.Page): 
    # Configurações da janela
    page.title = "Sistema de Passagens de Barco"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200  # Largura maior para o painel administrativo
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    page.padding = 0
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Roboto")
    

    def route_change(e): 
        
        page.views.clear() 
        
        # Mapeamento de rotas
        routes = {
            "/login": login.View(page),
            "/home": home.View(page),
            "/cadastro": signup.View(page),
            "/search": search.View(page),
            "/payment": payment.View(page),
            "/navigation": navigation.View(page),
            "/selection": selection.View(page),
            "/admin_home": admin_home.View(page),
            "/passagens": passagens.View(page),
            "/portos": portos.View(page),
            "/embarcacoes": embarcacoes.View(page),
            "/assentos": assentos.View(page),
            "/passageiros": passageiros.View(page),
            "/viagens": viagens.View(page)
        }
        
        # Verifica se a rota começa com algum padrão conhecido
        for route_pattern, view in routes.items():
            if page.route.startswith(route_pattern):
                page.views.append(view)
                break
        else:
            # Rota não encontrada - mostra página 404
            page.views.append(
                ft.View(
                    "/404",
                    [
                        ft.AppBar(title=ft.Text("Página não encontrada")),
                        ft.Text("404 - Página não encontrada", size=30),
                        ft.ElevatedButton(
                            "Voltar para o início",
                            on_click=lambda _: page.go("/home")
                        )
                    ]
                )
            )
        
        page.update()

    def view_pop(e):
        """Lida com o botão voltar do navegador"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Configura handlers de navegação
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inicia o aplicativo na rota de login
    page.go("/home")

ft.app(target=main)  # Pode alterar para ft.AppView.WEB_BROWSER se quiser abrir no navegador