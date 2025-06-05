import flet as ft

def open_search(e: ft.ControlEvent, origem: str, destino: str, embarque: str):
    # Validar parâmetros antes de navegar
    if not origem or not destino:
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Selecione origem e destino!"), open=True))
        return
    
    # Construir URL corretamente
    params = {
        "origem": origem,
        "destino": destino,
        "embarque": embarque if embarque else ""
    }
    
    e.page.go(f"/search?origem={params['origem']}&destino={params['destino']}&embarque={params['embarque']}")

