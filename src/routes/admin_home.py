import flet as ft

def View(page: ft.Page):
    content_area = ft.Column([], expand=True, scroll=ft.ScrollMode.AUTO)
    
    def handle_navigation(e):
        if e.control.selected_index == 0:  # Home
            show_home()
        elif e.control.selected_index == 1:  # Passageiros
            page.go("/passageiros")
        elif e.control.selected_index == 2:  # Viagens
            page.go("/viagens")
        page.update()
    
    def navigate_to(route):
        page.go(route)
    
    def create_card(title, icon, route, color):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(icon, color=color),
                            title=ft.Text(title, weight=ft.FontWeight.BOLD),
                        ),
                        ft.Row(
                            [ft.Text("Acessar", style="labelMedium"),
                             ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=20)],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=0,
                ),
                width=200,
                height=150,
                padding=10,
                on_click=lambda e: navigate_to(route),
                ink=True,
            ),
            elevation=5,
            color=ft.Colors.GREY,
        )
    
    def show_home():
        cards = ft.Row(
            wrap=True,
            spacing=20,
            run_spacing=20,
            controls=[
                create_card("Portos", ft.Icons.LOCATION_ON, "/portos", ft.Colors.BLUE),
                create_card("Embarcações", ft.Icons.DIRECTIONS_BOAT, "/embarcacoes", ft.Colors.GREEN),
                create_card("Passageiros", ft.Icons.PEOPLE, "/passageiros", ft.Colors.ORANGE),
                create_card("Assentos", ft.Icons.EVENT_SEAT, "/assentos", ft.Colors.PURPLE),
                create_card("Viagens", ft.Icons.DIRECTIONS_BOAT_FILLED, "/viagens", ft.Colors.INDIGO),
                create_card("Passagens", ft.Icons.CONFIRMATION_NUMBER, "/passagens", ft.Colors.TEAL),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        
        welcome = ft.Column(
            controls=[
                ft.Text("Bem-vindo ao Painel Administrativo", 
                       size=24, 
                       weight=ft.FontWeight.BOLD),
                ft.Text("Selecione um módulo para gerenciar:", 
                       size=16, 
                       color=ft.Colors.GREY),
                ft.Divider(height=20),
            ]
        )
        
        content_area.controls = [
            welcome,
            cards,
            ft.Divider(height=30),
            ft.Text("Estatísticas Rápidas", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("12", size=36, weight=ft.FontWeight.BOLD),
                                ft.Text("Viagens hoje", style="labelMedium")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=20,
                        width=150,
                        height=100,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("85%", size=36, weight=ft.FontWeight.BOLD),
                                ft.Text("Ocupação", style="labelMedium")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=20,
                        width=150,
                        height=100,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("24", size=36, weight=ft.FontWeight.BOLD),
                                ft.Text("Novos passageiros", style="labelMedium")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=20,
                        width=150,
                        height=100,
                        bgcolor=ft.Colors.ORANGE_50,
                        border_radius=10,
                    ),
                ],
                spacing=20
            )
        ]
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        leading=ft.FloatingActionButton(
            icon=ft.Icons.ADD, 
            text="Novo",
            tooltip="Criar novo item",
            on_click=lambda e: print("Novo item")
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINE,
                selected_icon=ft.Icons.PEOPLE,
                label="Passageiros",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.DIRECTIONS_BOAT_OUTLINED,
                selected_icon=ft.Icons.DIRECTIONS_BOAT,
                label="Viagens",
            ),
        ],
        on_change=handle_navigation,
    )

    # Mostrar a página inicial por padrão
    show_home()

    return ft.View(
        "/admin_home",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=content_area,
                        padding=20,
                        expand=True,
                    ),
                ],
                expand=True,
            )
        ],
        padding=0
    )