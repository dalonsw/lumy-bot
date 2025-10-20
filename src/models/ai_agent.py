import dotenv

from datetime import datetime
from src.models.you_model import YouChat
from src.utils.arquivos import Arquivos

dotenv.load_dotenv()
Arquivos.criar_arquivo_se_nao_existir("./src/cache/historico.txt")

class AIAgent:
    def __init__(self, max_tokens: int = 1000, 
                 historico: str = "./src/cache/historico.txt", 
                 policy_file: str = "src/config/prompt_policy.txt",
                 debug: bool = False):
        self.__arquivo_historico = historico
        self.__debug = debug
        self.__prompt_policy = open(policy_file, "r",
                                    encoding="utf-8").read()
        self.__cliente = YouChat(is_conversation=True,
                                 max_tokens=max_tokens,
                                 timeout=15,
                                 intro=self.__prompt_policy,
                                 filepath=self.__arquivo_historico,
                                 update_file=True, history_offset=10250
                            )
    
    def get_datetime(self):
        return f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

    def perguntar(self, pergunta: str):
        try:
            request = f"{self.get_datetime()}: {pergunta}"
            reposta = self.__cliente.ask(request)
            mensagem = self.__cliente.get_message(reposta)
            if self.__debug:
                print(f"[MODO DEBUG] Resposta: {mensagem}\n")
            return mensagem
        except Exception as e:
            print(f"Erro ao obter resposta: {e}")
            