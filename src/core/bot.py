import os
import json

from functools import wraps
from src.models.ai_agent import AIAgent
from src.models.audio_controller import EntradaAudio, SaidaAudio
from src.core.servicos import bot_servicos

debug = True

agenteIA = AIAgent("Zeca", max_tokens=500)
agenteIA.conectar()
entrada_audio = EntradaAudio()
saida_audio = SaidaAudio()
on = True

def bot_main():
    while on:
        try:
            if debug:
                bot_debug_mode()
            else:
                bot_listen()
        except Exception as e:
            print(f"Erro: {e}")

def bot_listen():
    pergunta = entrada_audio.ouvir_microfone()
    if pergunta:
        resposta = json.loads(agenteIA.perguntar(pergunta))
        agenteIA.salvar_ultima_mensagem(pergunta, resposta['mensagem'])
        saida_audio.falar(resposta)
    else:
        saida_audio.falar("Desculpe, não entendi sua pergunta.")

def bot_debug_mode():
    pergunta = input("[MODO DEBUG] Insira sua pergunta: ")
    resposta = json.loads(agenteIA.perguntar(pergunta))
    agenteIA.salvar_ultima_mensagem(pergunta, resposta['mensagem'])
    if resposta["tipo"] == "funcao":
        funcao_nome = resposta["mensagem"]
        parametros = resposta.get("parametros", {})
        try:
            resultado_funcao = bot_servicos(funcao_nome, **parametros)
        except Exception as e:
            print(f"Erro ao executar a função {funcao_nome}: {e}")
    print(resposta)

    