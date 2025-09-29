import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro na síntese de voz: {e}")

if __name__ == "__main__":
    speak("Olá, este é um teste de síntese de voz.")