import os
import datetime
import dotenv
from threading import Timer
from src.services.alarmes import Alarmes
from src.services.spotify import SpotifyPlayer
from src.services.busca_web import BuscaWeb
dotenv.load_dotenv()

class Controlador:
    def __init__(self):
        self.alarmes = Alarmes()
        self.busca_web = BuscaWeb()
        self.spotify = SpotifyPlayer()
        self.servicos_registrados = {
            'tocar_musica': self.tocar_musica,
            'controlar_musica': self.controlar_musica,
            'definir_alarme': self.definir_alarme,
            'listar_alarmes': self.listar_alarmes,
            'apagar_alarme': self.remover_alarme,
            'alertar_alarme': self.modificar_alarme,
            'alterar_alarme': self.alterar_alarme,
            'buscar_web': self.buscar_web,
        }
        
    # ==================== Serviços de Spotify ====================
    
    def tocar_musica(self, busca, tipo):
        dispositivo_principal = os.getenv("SPOTIFY_DEVICE_NAME")
        if self.spotify.dispositivo_conectado() != dispositivo_principal:
            self.spotify.conectar_dispositivo(dispositivo_principal)
            
        uri = self.spotify.buscar(busca, tipo)
        if uri:
            self.spotify.pausar()
            Timer(1, self.spotify.tocar, args=[uri]).start()

    def controlar_volume_fala(self, nivel):
        if self.spotify.musica_tocando():
            self.spotify.volume(nivel)
            
    def volume_atual(self):
        return self.spotify.obter_volume_atual()

    def controlar_musica(self, acao, args=None):
        acoes = {
            'play': self.spotify.retomar,
            'pause': self.spotify.pausar,
            'next': self.spotify.proxima,
            'previous': self.spotify.anterior,
            'aleatorio': self.spotify.aleatorio,
            'repetir': self.spotify.repetir,
            'volume': self.spotify.volume
        }
        try:
            if args is not None:
                acoes[acao](args)
            else:
                acoes[acao]()
        except TypeError as e:
            print(f"Erro ao executar a ação '{acao}': {e}")

    # ==================== Serviços de Busca ====================

    def buscar_web(self, busca: str) -> str:
        return self.busca_web.buscar(busca)

    # ==================== Serviços de Alarmes ====================

    def modificar_alarme(self, atividade, nova_data_hora):
        nova_data_hora = datetime.datetime.strptime(nova_data_hora, 
                                                    "%Y-%m-%d %H:%M:%S")
        self.alarmes.modificar_alarme(atividade, nova_data_hora)

    def definir_alarme(self, atividade, data_hora):
        data_hora = datetime.datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
        self.alarmes.adicionar_alarme(atividade, data_hora)

    def alterar_alarme(self, atividade, nova_data_hora):
        nova_data_hora = datetime.datetime.strptime(nova_data_hora, 
                                                    "%Y-%m-%d %H:%M:%S")
        self.alarmes.alterar_alarme(atividade, nova_data_hora)

    def listar_alarmes(self):
        alarmes = self.alarmes.listar_alarmes()
        if not alarmes:
            return "Nenhum alarme definido."
        mensagens = [
            f"{alarme['atividade']} em {alarme['data_hora']}" 
            for alarme in alarmes
        ]

    def remover_alarme(self, atividade):
        self.alarmes.remover_alarme(atividade)
        
    # ==================== Execução de Serviços ====================

    def executar_servico(self, funcao_nome, *args, **kwargs) -> None:
        try:
            if funcao_nome in self.servicos_registrados:
                return self.servicos_registrados[funcao_nome](*args, **kwargs)
            else:
                raise ValueError(
                    f"Função '{funcao_nome}' não está registrada nos serviços."
                )
        except Exception as e:
            print(f"Ocorreu um erro ao tentar executar os serviços: {e}")