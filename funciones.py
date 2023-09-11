from flet import *
import flet as ft
from pydub import AudioSegment
from pydub.playback import play
import pygame
import wave
import pyaudio

def stop_recording(stream, p, ):
    stream.stop_stream()
    stream.close()
    p.terminate
    print('***DETENER GRABACION***')

def record(stream, CHUNK, frames,stop_event):
        while not stop_event.is_set():
            data = stream.read(CHUNK)
            frames.append(data)
            
def design_grabando(page, button_color):
    #Altura del snackbar
    alt_snackbar= (page.window_height)* 0.03
    button_color[0] = ft.colors.RED
    page.update()

    page.snack_bar = SnackBar(
        Text("Grabando...",size=alt_snackbar,weight="bold"),
        bgcolor="red"       
    )
    page.snack_bar.open = True
    page.update()

def play_response(mute_state):
    if mute_state[0]== False:
        pygame.mixer.init()
        pygame.mixer.music.load('response.mp3')
        print('***REPRODUCIENDO AUDIO***')
        pygame.mixer.music.play()
    else:
        print('***NO REPRODUCIENDO AUDIO***')

def design_recvoz(page):
    #Altura del snackbar
    alt_snackbar= (page.window_height)* 0.03
    page.snack_bar = SnackBar(
         Column([
              Text("Reconociendo tu voz...",size=alt_snackbar),
              ],alignment="center"),
              bgcolor="green"          
              )
    page.snack_bar.open = True

def save_record(CHANNELS, p, FORMAT, RATE, frames):
    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    print('***GUARDANDO GRABACION***')
    wf.close()

def color_boton(page, boton):
    if boton.bgcolor == ft.colors.GREEN:
        boton.bgcolor = ft.colors.RED
    elif boton.bgcolor == ft.colors.RED:
        boton.bgcolor = ft.colors.GREEN
    else:
        boton.bgcolor = ft.colors.GREEN
    page.update()

def inicializar_pyaudio(CHANNELS, CHUNK, FORMAT, RATE):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    return p, stream
