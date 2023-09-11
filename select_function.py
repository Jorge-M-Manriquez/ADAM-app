import json
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

class Select_function:
    def __init__(self):
        pass

    def select_function(self, text):  
        llm = LLM()
        function_name, args, message = llm.process_functions(text)
        if function_name is not None:
            print('***OBTENIENDO RESPUESTA DESDE GPT***')
            if function_name == "get_weather":
                function_response = Weather().get(args["ubicacion"])
                function_response = json.dumps(function_response)
                
                final_response = llm.process_response(text, message, function_name, function_response)
                tts_file = TTS().process(final_response)
                return {"result": "ok", "text": final_response, "file": tts_file}
            
            elif function_name == "abrir_chrome":
                PcCommand().open_chrome(args["website"])
                function_response = "Informa si la tarea fue completada"

                final_response = llm.process_response(text, message, function_name, function_response)
                tts_file = TTS().process(final_response)
                return {"result": "ok", "text": final_response, "file": tts_file}
            
            elif function_name == "hola":
                function_response = "responder el saludo, presentarse indicando tu nombre"
                
                final_response = llm.process_response(text, message, function_name, function_response)
                tts_file = TTS().process(final_response)
                return {"result": "ok", "text": final_response, "file": tts_file}
            
            elif function_name == "explicar_algo":
                function_response = "explicar lo solicitado"
                
                final_response = llm.process_response(text, message, function_name, function_response)
                tts_file = TTS().process(final_response)
                return {"result": "ok", "text": final_response, "file": tts_file}
        else:
            print('***OBTENIENDO RESPUESTA DESDE GPT***')
            function_name= "responder"
            function_response = text
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
