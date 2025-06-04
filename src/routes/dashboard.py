import flet as ft
from models.db_connection import DbConnection

db = DbConnection()

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

    cidades = db.listar_cidades()
    passagens = db.listar_passagens()
    viagens = db.listar_viagens()

    texto = ft.Text("Bem-vindo ao Dashboard!", size=24, weight=ft.FontWeight.BOLD)

    tabela_cidades = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cidades")),
        ],
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(cidade))]) for cidade in cidades],
    )
    tabela_passagens = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Origem")),
            ft.DataColumn(ft.Text("Destino")),
            ft.DataColumn(ft.Text("Data Partida")),
            ft.DataColumn(ft.Text("Assento")),
            ft.DataColumn(ft.Text("Passageiro")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(origem)),
                ft.DataCell(ft.Text(destino)),
                ft.DataCell(ft.Text(data_partida)),
                ft.DataCell(ft.Text(numero_assento)),
                ft.DataCell(ft.Text(passageiro))
            ]) for origem, destino, data_partida, numero_assento, passageiro in passagens
        ],
    )
    tabela_viagens = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Viagem")),
            ft.DataColumn(ft.Text("Origem")),
            ft.DataColumn(ft.Text("Destino")),
            ft.DataColumn(ft.Text("Data Partida")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(id_viagem))),
                ft.DataCell(ft.Text(origem)),
                ft.DataCell(ft.Text(destino)),
                ft.DataCell(ft.Text(data_partida))
            ]) for id_viagem, origem, destino, data_partida in viagens
        ],
    )



    return ft.View(
        "/",
        appbar=appbar,
        controls=[
            texto,
            ft.Column(
                [
                    ft.Text("Cidades", size=20, weight=ft.FontWeight.BOLD),
                    tabela_cidades,
                    ft.Text("Passagens", size=20, weight=ft.FontWeight.BOLD),
                    tabela_passagens,
                    ft.Text("Viagens", size=20, weight=ft.FontWeight.BOLD),
                    tabela_viagens,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            )
        ]
    )
