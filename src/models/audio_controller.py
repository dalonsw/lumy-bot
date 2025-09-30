import speech_recognition as sr
import pyttsx3

class EntradaAudio:
    def __init__(self):
        self.reader = sr.Recognizer()
        self.mic = sr.Microphone()

    def ouvir_microfone(self):
        with self.mic as source:
            print("Fale algo...")
            audio = self.reader.listen(source)

        try:
            texto = self.reader.recognize_google(audio, language="pt-BR")
            print("Você disse: " + texto)
            return texto.lower()
        except sr.UnknownValueError:
            print("Não consegui entender o áudio.")
        except sr.RequestError as e:
            print(f"Erro ao processar o áudio; {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

class SaidaAudio:
    def __init__(self):
        self.engine = pyttsx3.init()

    def falar(self, texto):
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Erro na síntese de voz: {e}")