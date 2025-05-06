import flet as ft
import datetime
from controllers import home_controller

def View(page: ft.Page):
    page.title = "Home"

    def handle_change(e):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))


    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MENU),
        title=ft.Text("Home"),
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

    title = ft.Text("Peça uma viagem", size=30)
    origem = ft.Dropdown(
        label="Origem",
        options=[
            ft.dropdown.Option("Óbidos"),
            ft.dropdown.Option("Belém"),
            ft.dropdown.Option("Santarem"),
            ft.dropdown.Option("Alenquer"),
            ft.dropdown.Option("Oriximiná"),
        ],
        width=300,
    )
    destino = ft.Dropdown(
        label="Destino",
        options=[
            ft.dropdown.Option("Óbidos"),
            ft.dropdown.Option("Belém"),
            ft.dropdown.Option("Santarem"),
            ft.dropdown.Option("Alenquer"),
            ft.dropdown.Option("Oriximiná"),
        ],
        width=300,
    )

    embarque = ft.ElevatedButton(
        "Pick date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2000, month=10, day=1),
                last_date=datetime.datetime(year=2025, month=10, day=1),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
    )

    pesquisar = ft.ElevatedButton(
        text="Pesquisar",
        icon=ft.icons.SEARCH,
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.WHITE,
        on_click=home_controller.open_search,
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
            pesquisar,
        ],
    )