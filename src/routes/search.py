import flet as ft

passagem1 = {
    "origem": "Óbidos",
    "destino": "Belém",
    "data": "2023-10-01",
    "horario": "10:00",
    "preco": 100.0,
}

passagem2 = {
    "origem": "Alenquer",
    "destino": "Óbidos",
    "data": "2023-10-02",
    "horario": "12:00",
    "preco": 120.0,
}

def create_passage_card(passage):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.DIRECTIONS_BUS),
                        title=ft.Text(f"{passage['origem']} → {passage['destino']}"),
                        subtitle=ft.Text(f"Data: {passage['data']} • Horário: {passage['horario']}"),
                    ),
                    ft.Row(
                        [
                            ft.Text(f"R$ {passage['preco']:.2f}", 
                                   size=20, weight=ft.FontWeight.BOLD),
                            ft.FilledButton("Comprar"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=5,
            ),
            width=400,
            padding=10,
        )
    )

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

    passage_cards = ft.Column(
        [
            create_passage_card(passagem1),
            create_passage_card(passagem2),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        "/",
        appbar=appbar,
        controls=[passage_cards],
        padding=20,
        scroll=ft.ScrollMode.AUTO,
    )
