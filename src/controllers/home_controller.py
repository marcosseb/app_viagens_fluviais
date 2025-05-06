import flet as ft

def open_search(e: ft.ControlEvent):
    e.page.go("/search")