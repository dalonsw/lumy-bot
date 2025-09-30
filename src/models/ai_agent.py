import json
import os
import pickle
import datetime

from dotenv import load_dotenv
from putergenai import PuterClient

load_dotenv()

class AIAgent:
    def __init__(self, nome: str, token_file: str = "puter_token.pkl", policy_file: str = "src/config/prompt_policy.json", model: str = "gpt-5-chat-latest", max_tokens: int = 100, ultima_mensagem: json = []):
        self.__nome = nome
        self.__cliente = PuterClient()
        self.__token_file = token_file
        self.__prompt_policy = json.load(open(policy_file, "r", encoding="utf-8"))
        self.__model = model
        self.__max_tokens = max_tokens
        self.__ultima_mensagem = ultima_mensagem

    def get_nome(self):
        return self.__nome

    def trocar_modelo(self, model: str):
        self.__model = model

    def sincronizar_datetime_atual(self):
        return [{
            "role": "system",
            "content": f"A data e hora atual é {datetime.datetime.now()}."
        }]

    def salvar_ultima_mensagem(self, mensagem_usuario: str, mensagem_assistente: str):
        self.__ultima_mensagem = [
            {"role": "user", "content": f"A última mensagem enviada pelo usuário foi: {mensagem_usuario}"},
            {"role": "assistant", "content": f"A última resposta do assistente foi: {mensagem_assistente}"}
        ]

    def conectar(self):
        if os.path.exists(self.__token_file):
            with open(self.__token_file, "rb") as f:
                token = pickle.load(f)
                self.__cliente.token = token
            print("Sessão carregada do token.")
        else:
            self.__cliente.login(os.getenv("CLIENT_NAME"), os.getenv("CLIENT_PASSWORD"))
            with open(self.__token_file, "wb") as f:
                pickle.dump(self.__cliente.token, f)
            print("Login realizado e token salvo.")

    def perguntar(self, pergunta: str,):
        messages = [
            *self.__prompt_policy,
            *self.sincronizar_datetime_atual(),
            *self.__ultima_mensagem,
            {
                "role": "user",
                "content": pergunta
            }
        ]
        response = self.__cliente.ai_chat(
            messages=messages,
            options={"model": self.__model, "temperature": 1, "max_tokens": self.__max_tokens},
            strict_model=True
        )
        return response["response"]["result"]["message"]["content"]
