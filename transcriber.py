import openai
    
class Transcriber:
    def __init__(self):
        pass
        
    def transcribe(self, file_path):
        # Open the file
        with open(file_path, 'rb') as audio_file:
            # Transcribir el audio con Whisper
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print("********TRANSCRIBIENDO********")
        return transcript.text

