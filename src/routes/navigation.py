import flet as ft
import datetime

def View(page: ft.Page):
    page.title = "Acompanhar Viagem"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    def voltar_home(e):
        page.go("/home")

    # Dados simulados de passagens
    passagens = [
        {
            "id": "BARC-2023-001",
            "origem": "Porto de Santos",
            "destino": "Ilha Bela",
            "data": datetime.datetime(2023, 12, 15, 14, 30),
            "status": "Embarque em 2h",
            "assento": "A12"
        },
        {
            "id": "BARC-2023-002",
            "origem": "Porto de Angra",
            "destino": "Ilha Grande",
            "data": datetime.datetime(2023, 12, 20, 9, 0),
            "status": "Confirmada",
            "assento": "B05"
        }
    ]

    # Cria cards de passagens
    passagens_widgets = []
    for p in passagens:
        passagens_widgets.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.CONFIRMATION_NUMBER),
                            title=ft.Text(f"Passagem #{p['id']}"),
                            subtitle=ft.Text(f"{p['origem']} → {p['destino']}"),
                        ),
                        ft.Divider(height=1),
                        ft.Row([
                            ft.Text(f"🗓 {p['data'].strftime('%d/%m/%Y %H:%M')}"),
                            ft.Text(f"🧭 {p['status']}", color=ft.Colors.GREEN if "Confirmada" in p['status'] else ft.Colors.BLUE),
                            ft.Text(f"💺 Assento {p['assento']}")
                        ], spacing=20)
                    ]),
                    padding=10,
                    width=400
                ),
                elevation=5
            )
        )

    # Mapa simulado (imagem de placeholder)
    mapa = ft.Container(
        content=ft.Column([
            ft.Text("Rota em Tempo Real", size=18, weight=ft.FontWeight.BOLD),
            ft.Image(
                src="../assets/map.png",
                width=400,
                height=250,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(10)
            )
        ]),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=ft.border_radius.all(10)
    )

    return ft.View(
        "/navigation",
        appbar=ft.AppBar(
            title=ft.Text("Minhas Viagens"),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=voltar_home,
                tooltip="Voltar"
            ),
            actions=[
                ft.IconButton(ft.icons.REFRESH, tooltip="Atualizar"),
                ft.IconButton(ft.icons.DOWNLOAD, tooltip="Baixar Comprovante"),
            ],
        ),
        controls=[
            ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=40),
                                ft.Text("Pagamento Confirmado!", size=20, weight=ft.FontWeight.BOLD)
                            ], spacing=10),
                            padding=20
                        ),
                        color=ft.Colors.GREEN_50
                    ),
                    ft.Divider(height=20),
                    ft.Text("Suas Passagens:", size=18, weight=ft.FontWeight.BOLD),
                    ft.Column(passagens_widgets, spacing=15),
                    ft.Divider(height=30),
                    mapa,
                    ft.ElevatedButton(
                        "Acompanhar Minha Viagem",
                        icon=ft.icons.DIRECTIONS_BOAT,
                        on_click=lambda e: print("Acompanhando viagem..."),
                        width=400
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )