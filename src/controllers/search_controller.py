import flet as ft

def open_payment(e: ft.ControlEvent):
    e.page.go("/payment")