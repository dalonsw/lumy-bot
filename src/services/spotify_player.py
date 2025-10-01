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
        self.conectar_dispositivo(os.getenv("SPOTIFY_DEVICE_ID"))

    def iniciar_sessao(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.id_cliente,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-modify-playback-state,user-read-playback-state"
        ))
        
    def conectar_dispositivo(self, device_id):
        if self.sp:
            self.sp.transfer_playback(device_id=device_id, 
                                      force_play=True)

    def buscar(self, pesquisa, tipo):
        if self.sp:
            resultados = self.sp.search(q=pesquisa, type=tipo, limit=1)
            items = resultados.get(f"{tipo}s", {}).get("items", [])
            if items:
                return items[0]["uri"]
        return None

    def play(self, uri):
        print(f"Tocando URI: {uri}")
        if self.sp:
            if "track" in uri:
                self.sp.start_playback(uris=[uri])
            else:
                self.sp.start_playback(context_uri=uri)
                
    def parar(self):
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
        