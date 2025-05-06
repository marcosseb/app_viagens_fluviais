import flet as ft
from controllers import login_controller, signup_controller

def View(page: ft.Page):
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    '''def on_login_click(e):
        if username.value == "admin" and password.value == "1234":
            page.snack_bar = ft.SnackBar(ft.Text("Login successful!"), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid credentials!"), open=True)'''

    img_logo = ft.Image(src='../assets/icon.png', width=200, height=200)
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    login_button = ft.ElevatedButton("Login", on_click=login_controller.open_home, width=300)
    signup_button = ft.TextButton("Cadastre-Se", on_click=signup_controller.open_signup, width=300)

    return ft.View(
        controls=[
            img_logo,
            username,
            password,
            login_button,
            signup_button,
        ],
        padding=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )