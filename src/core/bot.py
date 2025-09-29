from src.services.puter_ai import perguntar_puter
from src.services.transcribe_audio import listen_mic
from src.services.audio_to_text import speak

def bot_main():
    try:
        bot_listen()
    
    except Exception as e:
        speak("Ocorreu um erro no assistente. Por favor, tente novamente.")

def bot_listen():
    pergunta = listen_mic()

    if pergunta:
        resposta = perguntar_puter(pergunta)
        
        if "buscaDataAtual" in resposta:
            from datetime import datetime
            data_atual = datetime.now().strftime("%d/%m/%Y")
            speak(f"A data atual é {data_atual}.")
        else:
            speak(resposta)

        if "buscaHoraAtual" in resposta:
            from datetime import datetime
            hora_atual = datetime.now().strftime("%H:%M")
            speak(f"A hora atual é {hora_atual}.")
        else:
            speak(resposta)
    else:
        speak("Desculpe, não entendi sua pergunta.")
