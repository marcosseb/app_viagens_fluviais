import flet as ft
import datetime
from models.db_connection import DbConnection
from controllers import home_controller

db = DbConnection()

print(db.listar_viagens())

def View(page: ft.Page):
    page.title = "Home"
    
    # Variável para armazenar a data selecionada
    selected_date = None
    # Componente para exibir a data selecionada
    date_display = ft.Text("Nenhuma data selecionada")

    # Função para lidar com mudança de data
    def handle_date_change(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value.strftime('%Y-%m-%d')
            date_display.value = selected_date
            date_display.update()

    # Função para abrir o DatePicker
    def open_date_picker(e):
        # Criar nova instância do DatePicker cada vez que o botão é clicado
        date_picker = ft.DatePicker(
            first_date=datetime.datetime.now(),
            last_date=datetime.datetime.now() + datetime.timedelta(days=365),
            on_change=handle_date_change,
        )
        page.open(date_picker)

    cidades = db.listar_cidades()

    appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),
        title=ft.Text("Home"),
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

    title = ft.Text("Peça uma viagem", size=30)
    
    # Origin dropdown with dynamic options
    origem = ft.Dropdown(
        label="Origem",
        options=[ft.dropdown.Option(cidade) for cidade in cidades],
        width=300,
    )
    
    # Destination dropdown with dynamic options
    destino = ft.Dropdown(
        label="Destino",
        options=[ft.dropdown.Option(cidade) for cidade in cidades],
        width=300,
    )
    
    # Botão para selecionar data
    embarque = ft.ElevatedButton(
        "Selecionar data",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=open_date_picker,
    )
    
    pesquisar = ft.ElevatedButton(
        text="Pesquisar",
        icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.WHITE,
        on_click=lambda e: home_controller.open_search(
            e, 
            origem.value, 
            destino.value, 
            selected_date if selected_date else ""
        )
    )

    
    
    return ft.View(
        appbar=appbar,
        padding=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            title,
            origem,
            destino,
            embarque,
            date_display,
            pesquisar,
        ],
    )