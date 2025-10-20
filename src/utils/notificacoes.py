import pygame

class Notificacoes:
    def __init__(self):
        self.som_ativar = 'src/assets/sounds/ativar_speech.wav'
        self.som_alarme = 'src/assets/sounds/alarme.mp3'

    def tocar_som_ativar(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.som_ativar)
        pygame.mixer.music.play()
        pygame.mixer.stop()

    def tocar_som_alarme(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.som_alarme)
        pygame.mixer.music.play(-1)
        
    def parar_som_alarme(self):
        pygame.mixer.stop()
        pygame.mixer.quit()
        
if __name__ == "__main__":
    import asyncio
    from threading import Timer
    notificacoes = Notificacoes()

    async def tocar_som_alarme():
        Timer(3, notificacoes.tocar_som_alarme).start()
            

    async def desligar_som_alarme():
        input("Pressione Enter para parar o som do alarme...\n")
        notificacoes.parar_som_alarme()
        
    asyncio.run(tocar_som_alarme())
    asyncio.run(desligar_som_alarme())
