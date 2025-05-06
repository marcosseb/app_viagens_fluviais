import flet as ft

def View(page: ft.Page):
    page.title = "Cadastro"

    nome = ft.TextField(label="Nome", width=400)
    email = ft.TextField(label="Email", width=400)
    cad_pf = ft.TextField(label="CPF", width=400)
    password = ft.TextField(label="Senha", password=True, width=400)
    password2 = ft.TextField(label="Repetir Senha", password=True, width=400)
    cad_button = ft.ElevatedButton("Cadastrar")
    

    return ft.View(
        controls=[
            nome,
            email,
            cad_pf,
            password,
            password2,
            cad_button
        ],
        padding=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )