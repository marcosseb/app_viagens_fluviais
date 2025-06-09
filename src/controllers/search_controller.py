import flet as ft

def open_payment(e: ft.ControlEvent, id):
    e.page.go(f"/payment?id={id}")