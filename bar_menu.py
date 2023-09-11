import flet as ft
import time

# Declara 'exp_menu' como una variable global
exp_menu = None

def abrirventana(page, exp_menu):
    if page.window_width <= 800:
        page.overlay.append(exp_menu)
        exp_menu.offset = ft.transform.Offset(0,0)
    else:
        cerrarventana(page, exp_menu)
    page.update()

def cerrarventana(page, exp_menu):
    page.overlay.remove(exp_menu)
    page.update()

def check(page, bar, responsiv, boton_r, col1, col2):
    # Usa la palabra clave 'global' para indicar que quieres usar la variable global 'exp_menu'
    global exp_menu

    while True:
        if page.window_width <= 800:
            for x in bar.actions[1].controls:
                x.visible = False
            responsiv.visible = True
            bar.update()
            time.sleep(1)
            
            # Redimensiona exp_menu
            alt_expmenu = (page.window_height) * 0.9
            anc_expmenu = (page.window_width) * 0.9
            alt_espacio = (page.window_height) - alt_expmenu
            anc_espacio = (page.window_width) - anc_expmenu
            exp_menu.margin = ft.margin.only(left=anc_espacio, bottom=alt_espacio)
            exp_menu.width = anc_expmenu
            exp_menu.height = alt_expmenu
            
            class ResizeSinMenu(Exception):
                pass

            if anc_expmenu >= (800*0.9):
                exp_menu.visible = False
                if exp_menu in page.overlay:
                    page.overlay.remove(exp_menu)
            else:
                exp_menu.visible = True

            #redimensionar tamaño boton grabar
            area_boton= ((page.window_height + page.window_height)/2)* 0.2
            boton_r.width= area_boton
            boton_r.height= area_boton

            #altura del espacio para la respuesta
            alt_col1 = (page.window_height)* 0.5
            col1.height= alt_col1

            #altura del espacio para la respuesta
            alt_col2 = (page.window_height)* 0.2
            col2.height= alt_col2

            page.update()
            time.sleep(0.05)
        else:
            for x in bar.actions[1].controls:
                x.visible = True
            responsiv.visible = False
            bar.update()
            time.sleep(1)
        page.update()
        

def create_appbar(page):
    # Usa la palabra clave 'global' para indicar que quieres usar la variable global 'exp_menu'
    global exp_menu

    menu = ["Perfil_medico", "Historial conversaciones", "Instrucciones", "AjustesADAM"]

    responsiv = ft.Container(
        visible=False,
        content=ft.IconButton(icon="menu", icon_color="white"),
        on_click=lambda e: abrirventana(page, exp_menu)
    )

    alt_bar= (page.window_height)* 0.05

    bar = ft.AppBar(
        title=ft.Text("ADAM", size=alt_bar, color="white"),
        center_title= True,
        bgcolor=ft.colors.GREEN,
        actions=[
            responsiv,
            ft.Row()
        ]
    )

    #Altura del exp_menu
    alt_expmenu= (page.window_height)* 0.9
    #Ancho del exp_menu
    anc_expmenu= (page.window_width)* 0.9
    #Altura del exp_menu
    alt_espacio= (page.window_height)- alt_expmenu
    #Ancho del exp_menu
    anc_espacio= (page.window_width)- anc_expmenu

    exp_menu = ft.Container(
        bgcolor="white",
        padding=10,
        margin=ft.margin.only(left=anc_espacio, bottom=alt_espacio),
        width=anc_expmenu,
        height=alt_expmenu,
        offset=ft.transform.Offset(-3,0),
        animate_offset=ft.animation.Animation(300, "easeIn "),
        content=ft.Column([
            ft.IconButton(icon ="close", icon_color="black", on_click=lambda e: cerrarventana(page, exp_menu))
        ])
    )

    for x in menu:
        bar.actions[1].controls.append(
            ft.TextButton(x,
                visible=True,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: "white"
                    }
                ),
                on_click=lambda e: page.go(x.lower()) # Agregado para la navegación.
            )
        )

        exp_menu.content.controls.append(
            ft.TextButton(x,
                visible=True,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: "black"
                    }
                ), 
                on_click=lambda e: page.go(x.lower()) # Agregado para la navegación.
            )
        )

    return bar, responsiv  # Devuelve una tupla con la AppBar y el contenedor responsiv


