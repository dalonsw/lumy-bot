from src.services.calendario import definir_lembrete
from src.services.spotify_player import SpotifyPlayer

def tocar_musica(busca, tipo):
    spotify = SpotifyPlayer()
    uri = spotify.buscar(busca, tipo)
    if uri:
        spotify.play(uri)
    return f"Tocando {busca} no Spotify."

def controlar_musica(acao, ativo=None):
    spotify = SpotifyPlayer()
    acoes = {
        'play': spotify.retomar,
        'pause': spotify.parar,
        'next': spotify.proxima,
        'previous': spotify.anterior,
        'shuffle': spotify.aleatorio
    }
    if acao in acoes:
        acoes[acao]() if acao != 'shuffle' else acoes[acao](ativo)

servicos_registrados = {
    'definir_lembrete': definir_lembrete,
    'tocar_musica': tocar_musica,
    'controlar_musica': controlar_musica
}

def bot_servicos(funcao_nome, *args, **kwargs) -> None:
    if funcao_nome in servicos_registrados:
        return servicos_registrados[funcao_nome](*args, **kwargs)
    else:
        raise ValueError(
            f"Função '{funcao_nome}' não está registrada nos serviços."
        )