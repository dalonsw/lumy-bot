import os
import datetime
import dotenv
from src.services.lembretes import Lembretes
from src.services.spotify_player import SpotifyPlayer
dotenv.load_dotenv()

class Controlador:
    def __init__(self):
        self.lembretes = Lembretes()
        self.spotify = SpotifyPlayer()
        self.servicos_registrados = {
            'tocar_musica': self.tocar_musica,
            'controlar_musica': self.controlar_musica,
            'definir_lembrete': self.definir_lembrete,
            'listar_lembretes': self.listar_lembretes,
            'apagar_lembrete': self.remover_lembrete,
            'alertar_lembrete': self.alertar_lembrete,
            'alterar_lembrete': self.alterar_lembrete,
        }
        
    # ==================== Serviços de Spotify ====================
    
    def tocar_musica(self, busca, tipo):
        self.spotify.conectar_dispositivo(os.getenv("SPOTIFY_DEVICE_ID"))
        uri = self.spotify.buscar(busca, tipo)
        if uri:
            self.spotify.play(uri)
        return f"Tocando {busca} no Spotify."

    def controlar_musica(self, acao, args=None):
        acoes = {
            'play': self.spotify.retomar,
            'pause': self.spotify.parar,
            'next': self.spotify.proxima,
            'previous': self.spotify.anterior,
            'aleatorio': self.spotify.aleatorio,
            'repetir': self.spotify.repetir,
            'volume': self.spotify.volume
        }
        try:
            if args:
                acoes[acao](args)
            else:
                acoes[acao]()
        except TypeError as e:
            print(f"Erro ao executar a ação '{acao}': {e}")
    
    # ==================== Serviços de Lembretes ====================
            
    def alertar_lembrete(self):
        return self.lembretes.alertar_lembrete()

    def definir_lembrete(self, atividade, data_hora):
        data_hora = datetime.datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
        self.lembretes.adicionar_lembrete(atividade, data_hora)
        return f"Lembrete definido para {atividade} em {data_hora}."

    def alterar_lembrete(self, atividade, nova_data_hora):
        nova_data_hora = datetime.datetime.strptime(nova_data_hora, "%Y-%m-%d %H:%M:%S")
        self.lembretes.alterar_lembrete(atividade, nova_data_hora)
        return f"Lembrete alterado para {atividade} em {nova_data_hora}."

    def listar_lembretes(self):
        lembretes = self.lembretes.listar_lembretes()
        if not lembretes:
            return "Nenhum lembrete definido."
        mensagens = [
            f"{lembrete['atividade']} em {lembrete['data_hora']}" 
            for lembrete in lembretes
        ]
        return "Lembretes:\n" + "\n".join(mensagens)
    
    def remover_lembrete(self, atividade):
        self.lembretes.remover_lembrete(atividade)
        return f"Lembrete removido para {atividade}"

    def executar_servico(self, funcao_nome, *args, **kwargs) -> None:
        if funcao_nome in self.servicos_registrados:
            return self.servicos_registrados[funcao_nome](*args, **kwargs)
        else:
            raise ValueError(
                f"Função '{funcao_nome}' não está registrada nos serviços."
            )