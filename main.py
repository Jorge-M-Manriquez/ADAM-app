from flet import *
import flet as ft
import pyaudio
import wave
import threading
import speech_recognition as sr
from transcriber import Transcriber
from dotenv import load_dotenv
import os
import openai
from select_function import Select_function
import pygame
from bar_menu import create_appbar, check
from funciones import record, stop_recording, design_grabando, play_response, design_recvoz, save_record, color_boton, inicializar_pyaudio

#
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

def main(page: ft.Page):
    page.window_width= 350
    page.window_height= 700
    page.scroll= "auto"
    
    #llamar al appbar
    bar, responsiv = create_appbar(page)
    page.appbar = bar
    # Variable de estado para rastrear el color actual del botón
    button_color = [ft.colors.GREEN]
    #Definir parametro para la respuesta final en texto
    response = Text() 
    #Definir parametro para silenciar a adam
    mute_state=[False]
    #elementos necesarios para la grabacion
    recording_state = [False]
    frames = []
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 22050
    audio_element = None
    # Definir un diccionario para almacenar stream y p
    context = {'stream': None, 'p': None}
    #Definir parametro para detener el proceso
    obtener_resp= [True]
    #tamaño botones
    area_boton1= (page.window_height)* 0.2 
    area_boton2= (page.window_height)* 0.1 
    # Crear un objeto Event para señalizar cuándo detener la grabación
    stop_event = threading.Event()
    boton_s_visible = [False]

    def recordnow(e):
        nonlocal recording_state, frames, audio_element, button_color
        global transcript, result
        obtener_resp[0]= True
        color_boton(page, boton_r)
        context['p'] = pyaudio.PyAudio()
        context['stream'] = context['p'].open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
        if not recording_state[0]:
            recording_state[0] = True
            threading._start_new_thread(record, (context['stream'],  CHUNK, frames, stop_event))
            print('***INICIANDO GRABACION***')
            boton_s.visible=True
            boton_s_visible[0]= True
            design_grabando(page, button_color)
            page.update()

        else:
            recording_state[0] = False
            button_color[0] = ft.colors.GREEN
            page.update()
            
            stop_recording(context['stream'], context['p'])  
            
            save_record(CHANNELS, context['p'], FORMAT, RATE, frames)
            #
            try:
                boton_s.visible = False
            except Exception as e:
                print(f"Error al intentar cambiar la visibilidad de boton_s: {e}")

            if obtener_resp[0] == True:
                boton_s.visible=False
                r = sr.Recognizer()
                with sr.AudioFile("recording.wav") as source:
                    audio_data = r.record(source)
                    design_recvoz(page)
                    page.update()
            
                    if obtener_resp[0] == True:
                        transcript = Transcriber().transcribe("recording.wav")
                        # Eliminar el archivo recording.wav después de reproducirlo
                        #os.remove('recording.wav')
                        #page.update()
                    else:
                        print("***RESPUESTA CANCELADA***")

                    if obtener_resp[0] == True:
                        result = Select_function().select_function(transcript)
                        final_response = result["text"]
                        response.value = final_response
                        print('***MOSTRANDO RESPUESTA TXT***')
                        page.update()
                    else:
                        print("***RESPUESTA CANCELADA***")
                        response.value = ""
                        
                    if obtener_resp[0] == True:               
                        frames = []
                        print('***RESTABLECIENDO FRAMES***')
                        play_response(mute_state)
                        page.update()
                    else:
                        print("***RESPUESTA CANCELADA***")
                        try:
                            pygame.mixer.music.stop()
                        except:
                            print("***NO SE ESTABA REPRODUCIENDO NINGUN AUDIO***")
                            response.value = ""
                        obtener_resp[0] == True
            else:
                print("***RESPUESTA CANCELADA***")
                # Eliminar el archivo response.mp3 después de reproducirlo
                #os.remove('response.mp3')
                #page.update()

    def stop_proceso(e):
        obtener_resp[0]= False
        #stop_recording(context['stream'], context['p'], boton_s) 
        # Restablecer el color del botón de grabar
        if recording_state[0]==True:
            color_boton(page, boton_r)
        # Detener la reproducción del sonido si está activa
        try:
            pygame.mixer.music.stop()
        except:
            print("***NO SE ESTABA REPRODUCIENDO NINGUN AUDIO***")
        # Cerrar el snackbar si está abierto
        if page.snack_bar is not None:
            page.snack_bar.open = False
        # Limpiar la respuesta en texto
        response.value = ""
        # Detener la grabación si está activa
        if recording_state[0]==True:
            #stop_event.set()
            #stop_recording(context['stream'], context['p'], boton_s)
            frames.clear() 
            recording_state[0] = False
        try:
            boton_s.visible = False
        except Exception as e:
            print(f"Error al intentar cambiar la visibilidad de boton_s: {e}")        
        page.update() 

    def fmute_state(e):
        if mute_state[0] == False:
            boton_m.content= ft.Image(src="not_ear.png", scale= 2)
            mute_state[0] = True
            boton_m.bgcolor=ft.colors.RED
            try:
                pygame.mixer.music.stop()
            except:
                print("***NO SE ESTABA REPRODUCIENDO NINGUN AUDIO***")
        else:
            boton_m.content= ft.Image(src="ear.png", scale= 2)
            mute_state[0] = False
            boton_m.bgcolor=ft.colors.GREEN

    #botones mutear grabar y detener
    boton_s = ft.ElevatedButton(
        width=area_boton2,
        height=area_boton2,
        on_click=stop_proceso,
        bgcolor=ft.colors.RED,
        content=ft.Image(
            src="stop.png", 
            scale= 2),
        visible=False) 
    
    boton_m = ft.ElevatedButton( 
        width=area_boton2,
        height=area_boton2,
        on_click=fmute_state,
        content=ft.Image(src="ear.png", scale= 2),
        bgcolor=ft.colors.GREEN,        
    )
    boton_r = ft.ElevatedButton(
        width=area_boton1, 
        height=area_boton1,
        on_click=recordnow,
        content=ft.Image(src="microphone.png"),
        bgcolor=ft.colors.GREEN,        
    )
    boton_i = ft.ElevatedButton(
        width=area_boton2, 
        height=area_boton2,
        bgcolor=page.bgcolor,        
    )

    alt_resp1 = (page.window_height)* 0.5 #altura responsiva
    alt_resp2 = (page.window_height)* 0.4
    anc_resp1 = (page.window_width)* 0.5

    col1 =ft.Column(
                    [response],
                    scroll=ft.ScrollMode.ALWAYS,
                    height=alt_resp1,  
                )
    col2= ft.Row(
                [ft.Column(
                    [boton_m],
                    height=alt_resp2,
                    horizontal_alignment= CrossAxisAlignment.START, 
                    alignment=ft.MainAxisAlignment.END),
                ft.Column(
                    [boton_r],
                    height=alt_resp2,
                    horizontal_alignment= CrossAxisAlignment.CENTER, 
                    alignment=ft.MainAxisAlignment.END),
                ft.Column([
                    ft.Column(
                        [boton_s],
                        height=alt_resp2,
                        horizontal_alignment= CrossAxisAlignment.END, 
                        alignment=ft.MainAxisAlignment.START),
                    ft.Column(
                        [boton_i],
                        horizontal_alignment= CrossAxisAlignment.END, 
                        alignment=ft.MainAxisAlignment.END)],)],

                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment= CrossAxisAlignment.CENTER)

    page.add(
        ft.Column(
            [
                col1,
                ft.Divider(),
                col2,
                                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    check(page, bar, responsiv, boton_r, col1, col2)

   
ft.app(target=main)



