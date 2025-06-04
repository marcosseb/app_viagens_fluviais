import flet as ft
from controllers import payment_controller

def View(page: ft.Page):
    page.title = "Busca"

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

    texto = ft.Text("Tela de pagamento")
    botao = ft.ElevatedButton(text="Pagar", on_click=payment_controller.open_navigation)

    return ft.View(
        "/",
        appbar=appbar,
        controls=[texto, botao],
        padding=20,
        scroll=ft.ScrollMode.AUTO,
    )
