import flet as ft
from controllers import payment_controller
from models.passagens_controller import PassagensController
from urllib.parse import urlparse, parse_qs

db = PassagensController()

def View(page: ft.Page):
    page.title = "Pagamento"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    parsed_url = urlparse(page.route)
    query_params = parse_qs(parsed_url.query)
    id = query_params.get("id", [""])[0]

    passagem = {
        "id_viagem": id,
        "id_assento": 2,
        "id_passageiro": 2
    }

    def voltar_home(e):
        page.go("/home")

    def finalizar_pagamento(e):
        # Simula processamento do pagamento
        progress_ring.visible = True
        confirmar_btn.disabled = True
        page.update()
        
        # Simula delay do processamento
        import time
        if db.cadastrar_passagem(passagem):
            time.sleep(2)
            print("Salvo")

        
        # Redireciona para navigation após "pagamento"
        payment_controller.open_navigation(e)

    # Componentes da UI
    titulo = ft.Text("Finalizar Pagamento", size=24, weight=ft.FontWeight.BOLD)
    
    resumo_compra = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.ListTile(
                    title=ft.Text("Resumo da Compra", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text("Passagem de Barco - Classe Econômica"),
                ),
                ft.Divider(),
                ft.Row(
                    [ft.Text("Valor Total:"), ft.Text("R$ 150,00", weight=ft.FontWeight.BOLD)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]),
            padding=20,
            width=400
        )
    )

    forma_pagamento = ft.Dropdown(
        label="Forma de Pagamento",
        options=[
            ft.dropdown.Option("Cartão de Crédito"),
            ft.dropdown.Option("Pix"),
            ft.dropdown.Option("Boleto Bancário"),
        ],
        value="Cartão de Crédito",
        width=400
    )

    progress_ring = ft.ProgressRing(visible=False)
    
    confirmar_btn = ft.ElevatedButton(
        "Confirmar Pagamento",
        icon=ft.Icons.PAYMENT,
        on_click=finalizar_pagamento,
        width=400,
        height=50
    )

    voltar_btn = ft.TextButton(
        "Voltar",
        icon=ft.Icons.ARROW_BACK,
        on_click=voltar_home
    )

    return ft.View(
        "/payment",
        appbar=ft.AppBar(
            title=ft.Text("Pagamento"),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=voltar_home,
                tooltip="Voltar"
            ),
        ),
        controls=[
            ft.Column(
                [
                    titulo,
                    ft.Divider(height=20),
                    resumo_compra,
                    ft.Divider(height=20),
                    forma_pagamento,
                    ft.Divider(height=20),
                    ft.Row([progress_ring, confirmar_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=10),
                    voltar_btn
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )