from src.services.puter_ai import perguntar_puter
from src.services.transcribe_audio import listen_mic
from src.services.audio_to_text import speak

def main():
    texto = input("Digite sua pergunta (ou fale algo): ")
    if texto:
        resposta = perguntar_puter(texto)
        print("Puter AI respondeu:", resposta)
        
        # Corrigido: usando elif para evitar conflitos
        if "buscaDataAtual" in resposta:
            from datetime import datetime
            data_atual = datetime.now().strftime("%d/%m/%Y")
            speak(f"A data atual é {data_atual}.")
        if "buscaHoraAtual" in resposta:
            from datetime import datetime
            hora_atual = datetime.now().strftime("%H:%M")
            speak(f"A hora atual é {hora_atual}.")
        else:
            # Fala a resposta normal se não for data nem hora
            speak(resposta)
    else:
        speak("Desculpe, não entendi sua pergunta.")

if __name__ == "__main__":
    while True:
        main()