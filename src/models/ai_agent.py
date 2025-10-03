import dotenv
from ai4free import YouChat
dotenv.load_dotenv()

class AIAgent:
    def __init__(self, nome: str, 
                 policy_file: str = "src/config/prompt_policy.txt", 
                 max_tokens: int = 100, dados_adicionais_file: str = "src/cache/dados_adicionais.json"):
        self.__nome = nome
        self.__cliente = YouChat(is_conversation=True, max_tokens=max_tokens,
                                timeout=30, intro=None, filepath=None,
                                update_file=True, proxies={}, history_offset=10250,
                                act=None,
                            )
        self.__prompt_policy = open(policy_file, "r", encoding="utf-8").read()
        
    def get_nome(self):
        return self.__nome
    
    def get_datetime(self):
        from datetime import datetime
        return f"datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
    def salvar_dados_adicionais(self, dados_novos: str):
        pass


    def perguntar(self, pergunta: str,):
        request = self.get_datetime() + self.__prompt_policy + pergunta
        response = self.__cliente.ask(request)
        return response['text']