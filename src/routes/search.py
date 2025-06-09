import flet as ft
from controllers import search_controller
from models.db_connection import DbConnection
from urllib.parse import urlparse, parse_qs

db = DbConnection()


def View(page: ft.Page):
    
    # Parse URL parameters
    parsed_url = urlparse(page.route)
    query_params = parse_qs(parsed_url.query)
    origem = query_params.get("origem", [""])[0]
    destino = query_params.get("destino", [""])[0]
    embarque = query_params.get("embarque", [""])[0]

    print(f"Parâmetros recebidos: {query_params}")
    
    page.title = "Busca"
    print(f"Origem: {origem}, Destino: {destino}, Embarque: {embarque}")
    
    appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),
        title=ft.Text("Busca"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.SEARCH, tooltip="Search"),
            ft.IconButton(ft.Icons.NOTIFICATIONS, tooltip="Notifications"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS),
                    ft.PopupMenuItem(text="Logout", icon=ft.Icons.LOGOUT),
                ],
            ),
        ],
    )

    # Validate parameters
    if not all([origem, destino, embarque]):
        return ft.View(
            appbar=appbar,
            controls=[
                ft.Text("Erro: Parâmetros de busca incompletos", 
                       size=18, color=ft.Colors.ERROR),
                ft.ElevatedButton("Voltar", 
                                on_click=lambda e: page.go("/home"))
            ],
            padding=20,
        )
    
    # Search for travels
    try:
        viagens_encontradas = db.search_travels(origem, destino, embarque)
    except Exception as e:
        print(f"Erro ao buscar viagens: {e}")
        viagens_encontradas = []
    
    # Page header
    header = ft.Column([
        ft.Text("Resultados da Busca", size=24, weight=ft.FontWeight.BOLD),
        ft.Text(f"De {origem} para {destino} em {embarque}", 
               size=16, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Divider()
    ])
    

    # Results section
    if viagens_encontradas:
        # Create cards for each travel option
        viagem_cards = []
        for i, viagem in enumerate(viagens_encontradas):
            # Desempacotar os valores corretamente
            (
                id_viagem, 
                porto_origem, 
                porto_destino, 
                cidade_origem, 
                cidade_destino, 
                data_partida, 
                embarcacao, 
                capacidade
            ) = viagem
            
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.DIRECTIONS_BOAT, size=40),
                            title=ft.Text(f"{porto_origem} → {porto_destino}"),
                            subtitle=ft.Text(f"Partida: {data_partida}"),
                        ),
                        ft.Row([
                            ft.Text("R$ 50,00", size=18, weight=ft.FontWeight.BOLD, 
                                   color=ft.Colors.PRIMARY),
                            #ft.Spacer(),
                            ft.ElevatedButton(
                                "Selecionar",
                                on_click=lambda e, idx=i: search_controller.open_payment(
                                    e,
                                    id_viagem
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    padding=16
                ),
                margin=ft.margin.only(bottom=10)
            )
            viagem_cards.append(card)
        
        results_content = ft.Column([
            ft.Text(f"{len(viagens_encontradas)} viagem(ns) encontrada(s)", 
                   size=16, weight=ft.FontWeight.W_500),
            *viagem_cards
        ])
# ... (restante do código) ...
    else:
        # No results found
        results_content = ft.Column([
            ft.Icon(ft.Icons.SEARCH_OFF, size=64, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text("Nenhuma viagem encontrada", 
                   size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Tente alterar os critérios de busca", 
                   size=16, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.ElevatedButton(
                "Nova Busca",
                icon=ft.Icons.SEARCH,
                on_click=lambda e: page.go("/home")
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    # Back button
    back_button = ft.OutlinedButton(
        "Voltar",
        ft.Icons.ARROW_BACK,
        on_click=lambda e: page.go("/home")
    )

    return ft.View(
        appbar=appbar,
        controls=[
            header,
            results_content,
            ft.Divider(),
            back_button
        ],
        padding=20,
        scroll=ft.ScrollMode.AUTO,
    )