import spotipy
import os
import dotenv
from spotipy.oauth2 import SpotifyOAuth
dotenv.load_dotenv()

class SpotifyPlayer:
    def __init__(self, id_cliente= os.getenv("SPOTIFY_CLIENT_ID"), 
                 client_secret= os.getenv("SPOTIFY_CLIENT_SECRET"), 
                 redirect_uri= os.getenv("SPOTIFY_REDIRECT_URI")):
        self.id_cliente = id_cliente
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.sp = None
        self.iniciar_sessao()

    def iniciar_sessao(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.id_cliente,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope="user-modify-playback-state,user-read-playback-state"
            ))
        except Exception as e:
            print(f"Ocorreu um erro ao iniciar a sessão no Spotify")
        
    def conectar_dispositivo(self, nome_dispositivo):
        dispositivos = self.sp.devices().get('devices', [])
        for dispositivo in dispositivos:
            if dispositivo['name'] == nome_dispositivo:
                self.sp.transfer_playback(dispositivo['id'], force_play=False)
                print(f"Conectado ao dispositivo: {nome_dispositivo}")
                return
    
    def dispositivo_conectado(self):
        dispositivos = self.sp.devices().get('devices', [])
        for dispositivo in dispositivos:
            if dispositivo['is_active']:
                return dispositivo['name']
        return None
    
    def musica_tocando(self):
        status = self.sp.current_playback()
        if status and status.get('is_playing'):
            return True
        return False

# ==================== Controles de Reprodução ====================

    def buscar(self, pesquisa, tipo):
        if self.sp:
            resultados = self.sp.search(q=pesquisa, type=tipo, limit=1)
            items = resultados.get(f"{tipo}s", {}).get("items", [])
            if items:
                return items[0]["uri"]
        return None

    def tocar(self, uri):
        if self.sp:
            if "track" in uri:
                self.sp.start_playback(uris=[uri])
            else:
                self.sp.start_playback(context_uri=uri)
                
    def pausar(self):
        if self.sp:
            self.sp.pause_playback()
            
    def retomar(self):
        if self.sp:
            self.sp.start_playback()
            
    def proxima(self):
        if self.sp:
            self.sp.next_track()
            
    def anterior(self):
        if self.sp:
            self.sp.previous_track()
            
    def adicionar_musica_fila(self, uri):
        if self.sp:
            self.sp.add_to_queue(uri)
            
    def aleatorio(self, estado):
        if self.sp:
            self.sp.shuffle(state=estado)
            
    def repetir(self, estado):
        if self.sp:
            self.sp.repeat(state=estado)
        
    def volume(self, arg):
        if self.sp:
            status = self.sp.current_playback()
            if status and 'device' in status:
                volume_atual = status['device']['volume_percent']
                if arg == 'aumentar':
                    novo_volume = min(volume_atual + 10, 100)
                elif arg == 'diminuir':
                    novo_volume = max(volume_atual - 10, 0)
                elif arg == 'mudo':
                    novo_volume = 0
                elif arg.isdigit():
                    novo_volume = max(0, min(int(arg), 100))
                else:
                    return
                self.sp.volume(novo_volume)
                
    def obter_volume_atual(self):
        try:
            if self.sp:
                status = self.sp.current_playback()
                if status and 'device' in status:
                    return status['device']['volume_percent']
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao obter o volume atual: {e}")
            
if __name__ == "__main__":
    player = SpotifyPlayer()
    print(f"Dispositivo conectado: {player.dispositivo_conectado()}")