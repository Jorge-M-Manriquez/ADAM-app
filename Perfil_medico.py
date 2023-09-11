from flet import *
import flet as ft

def main(page: Page):
    page.add(Text("PERFIL MEDICOO!!!"))
    ruta= page.route
    page.add(ft.Text(f"Initial route: {ruta}"))

