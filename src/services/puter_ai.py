from putergenai import PuterClient
from dotenv import load_dotenv
import os
import pickle
import json

prompt_policy = json.load(open("src/config/prompt_policy.json", "r", encoding="utf-8"))

load_dotenv()

TOKEN_FILE = "puter_token.pkl"

client = PuterClient()

# Tenta carregar token salvo
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "rb") as f:
        token = pickle.load(f)
        client.token = token
    print("Sessão carregada do token.")
else:
    # Faz login e salva token
    client.login(os.getenv("CLIENT_NAME"), os.getenv("CLIENT_PASSWORD"))
    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(client.token, f)
    print("Login realizado e token salvo.")

def perguntar_puter(pergunta):
    messages = prompt_policy + [
        {
            "role": "user", 
            "content": pergunta
        }
    ]
    response = client.ai_chat(
        messages=messages,
        options={"model": "gpt-5-chat-latest", "temperature": 1, "max_tokens": 100},
        strict_model=True
    )
    return response["response"]["result"]["message"]["content"]

if __name__ == "__main__":
    pergunta = perguntar_puter(input("Digite sua pergunta: "))
    print(pergunta)