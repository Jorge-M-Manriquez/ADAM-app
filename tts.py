import os
from dotenv import load_dotenv
import requests

class TTS():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('ELEVENLABS_API_KEY')
    
    def process(self, text):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/SOYHLrjzK2X1ezoPC6cr"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.35
            }
        }

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "response.mp3"
        file_path = os.path.join(script_dir, file_name)
        #print('***UBICACION ARCHIVO: ', script_dir, ' ***')

        response = requests.post(url, json=data, headers=headers)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print('***GENERANDO AUDIO RESPUESTA***')
        return file_name
