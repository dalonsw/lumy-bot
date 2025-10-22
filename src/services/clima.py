from webscout.search.duckduckgo_main import DuckDuckGoSearch

class Clima:
    def __init__(self):
        self.busca = DuckDuckGoSearch()

    def buscar_clima(self, localizacao: str, region: str = "pt-br",
                safesearch: str = "moderate") -> str:
        resultado = self.busca.weather(localizacao)
        if resultado:
            return f'Clima em {localizacao}: {resultado["current"]}'
        return "Não foi possível obter informações sobre o clima."