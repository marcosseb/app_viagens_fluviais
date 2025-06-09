import flet as ft




def View(page: ft.Page):

    admin_button = ft.ElevatedButton("Fluvial Admin", on_click=lambda e: page.go("/admin_home"))
    cliente_button = ft.ElevatedButton("Fluvial Cliente", on_click=lambda e: page.go("/home"))


    return ft.View(
        padding=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            admin_button,
            cliente_button
        ],
    )