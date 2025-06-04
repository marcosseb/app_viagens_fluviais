import flet as ft

def open_search(e, origem, destino, embarque):
    e.go("/search", query={
        "origem": origem,
        "destino": destino,
        "embarque": embarque
    })

