import os
import pygame
import wave
import speech_recognition as sr
from piper import PiperVoice

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
                                       phrase_time_limit=10)
        try:
            texto = self.reader.recognize_google(audio, 
                                                 language="pt-BR")
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
                 voice='./src/assets/tts-models/pt_BR-dii.onnx',
                 aquivo_wav='./src/assets/sounds/output.wav'):
        self.voice = voice
        self.aquivo_wav = aquivo_wav
        self.piper = PiperVoice.load(self.voice)

    def falar(self, texto):
        try:
            if not os.path.exists(os.path.dirname(self.aquivo_wav)):
                os.makedirs(os.path.dirname(self.aquivo_wav))
                
            with wave.open(self.aquivo_wav, "wb") as wav_file:
                self.piper.synthesize_wav(texto, wav_file)
                
            pygame.mixer.init()
            pygame.mixer.music.load(self.aquivo_wav)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
        except Exception as e:
            print(f"Erro ao sintetizar voz: {e}")
            pygame.mixer.quit()

    def parar(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Erro ao parar a reprodução: {e}")
            pygame.mixer.quit()