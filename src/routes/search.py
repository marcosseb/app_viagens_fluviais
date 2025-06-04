import flet as ft
from controllers import search_controller
from models.db_connection import DbConnection
from urllib.parse import urlparse, parse_qs

db = DbConnection()

def View(page: ft.Page):
    
    parsed_url = urlparse(page.route)
    query_params = parse_qs(parsed_url.query)
    origem = query_params.get("origem", [""])[0]
    destino = query_params.get("destino", [""])[0]
    embarque = query_params.get("embarque", [""])[0]
    page.title = "Busca"
    print(f"Origem: {origem}, Destino: {destino}, Embarque: {embarque}")
    
    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MENU),
        title=ft.Text("Busca"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.SEARCH, tooltip="Search"),
            ft.IconButton(ft.icons.NOTIFICATIONS, tooltip="Notifications"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Settings", icon=ft.icons.SETTINGS),
                    ft.PopupMenuItem(text="Logout", icon=ft.icons.LOGOUT),
                ],
            ),
        ],
    )

    label = ft.Text("Resultados da Busca", size=24, weight=ft.FontWeight.BOLD)
    text = ft.Text(
        f"Origem: {origem}, Destino: {destino}, Embarque: {embarque}",
        size=18,
        weight=ft.FontWeight.NORMAL
    )

    return ft.View(
        appbar=appbar,
        controls=[
            label,
            text,
        ]
    )
    

    