from webscout.search.duckduckgo_main import DuckDuckGoSearch

class BuscaWeb:
    def __init__(self):
        self.busca = DuckDuckGoSearch()
    
    def buscar(self, pergunta: str, region: str = "pt-br", 
               safesearch: str = "moderate", 
               max_results: int = 5) -> str:
        resultados = self.busca.text(pergunta, region=region, 
                                     safesearch=safesearch, 
                                     max_results=max_results)
        resultados_formatados = "\n".join(
            [f"{res['body']}. " for i, res in enumerate(resultados)]
        )
        return resultados_formatados

