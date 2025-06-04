import flet as ft
import datetime
from models.db_connection import DbConnection
from controllers import home_controller
from urllib.parse import urlparse
#import sqlite3

# conn = sqlite3.connect("./storage/data/passagens_barco.db", check_same_thread=False)

# def listar_cidades():
#     c = conn.cursor()
#     try:
#         c.execute('SELECT DISTINCT cidade FROM portos')
#         cities = c.fetchall()
#         return [row[0] for row in cities]
#     finally:
#         c.close()  # Ensure cursor is closed after operation

db = DbConnection()

for cidade in db.listar_cidades():
    print("Cidade:" + cidade)

print(db.listar_cidades())
print(db.listar_passagens())

def View(page: ft.Page):
    page.title = "Home"

    #def handle_change(e):
    #    return_value = e.control.value.strftime('%Y-%m-%d') if e.control.value else "No date selected"
    #    return return_value

    #def handle_dismissal(e):
    #    page.add(ft.Text(f"DatePicker dismissed"))

    # Fetch cities from the database
    cidades = db.listar_cidades()

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

    print(page)

    date = None

    def on_date_change(e):
        nonlocal date
        date = e.control.value.strftime('%Y-%m-%d') if e.control.value else None
        #print(f"Selected date: {date}")
    

    calendar = ft.DatePicker(
                first_date=datetime.datetime(year=2000, month=10, day=1),
                last_date=datetime.datetime(year=2025, month=12, day=30),
                on_change= on_date_change,  
            )
    
    
    
    
    embarque = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(calendar),
    )
    
    test_query = 'banana'

    pesquisar = ft.ElevatedButton(
        text="Pesquisar",
        icon=ft.icons.SEARCH,
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.WHITE,
        on_click=lambda e: page.go(
            f"/search?origem={origem.value}&destino={destino.value}&embarque={date}"
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
            pesquisar,
        ],
    )