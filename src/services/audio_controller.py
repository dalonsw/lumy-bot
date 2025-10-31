import pygame
import speech_recognition as sr
from src.models.speechma import Speechma

class EntradaAudio:
    def __init__(self, debug=False):
        self.reader = sr.Recognizer()
        self.mic = sr.Microphone()
        self.debug = debug

    def ouvir_microfone(self):
        with self.mic as source:
            if self.debug:
                print("[MODO DEBUG] Ouvindo...")
            audio = self.reader.listen(source, timeout=0, 
                                       phrase_time_limit=1000)
        try:
            texto = self.reader.recognize_google(audio, 
                                                 language="pt-BR, en-US")
            if self.debug:
                print(f"[MODO DEBUG] Você disse: {texto}")
            return texto.lower()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Erro ao se comunicar com o serviço de voz: {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

class SaidaAudio:
    def __init__(self, 
                 voice='voice-221',
                 path='./src/assets/sounds/'):
        self.path = path
        self.voice = voice
        self.speech_man = Speechma(voice_id=self.voice, 
                                    directory=self.path)

    def falar(self, texto):
        try:
            self.speech_man.gerar_audio(texto)

            pygame.mixer.init()
            pygame.mixer.music.load(self.path + "output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
        except Exception as e:
            print(f"Erro ao sintetizar voz: {e}")

    def parar(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Erro ao parar a reprodução: {e}")
            pygame.mixer.quit()
