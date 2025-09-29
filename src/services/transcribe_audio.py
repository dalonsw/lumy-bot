import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

def listen_mic():
    with mic as source:
        print("Fale algo...")
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("Você disse: " + texto)
        return texto
    except sr.UnknownValueError:
        print("Não consegui entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao processar o áudio; {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    listen_mic()