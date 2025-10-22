import datetime
import json
import asyncio

from src.utils.notificacoes import Notificacoes
from src.models.ai_agent import AIAgent
from src.services.audio_controller import EntradaAudio, SaidaAudio
from src.core.controller import Controlador

# Configurações
bot_debug = True # Modo debug para entrada via texto
agenteIA = AIAgent(max_tokens=1000)
controlador = Controlador()
notificacoes = Notificacoes()
entrada_audio = EntradaAudio(debug=True)
saida_audio = SaidaAudio()
volume_spotify_atual = str(controlador.volume_atual()) 

# ==================== Funções do Bot ====================

async def bot_ouvir():
    try:
        notificacoes.tocar_som_ativar()
        pergunta = await asyncio.to_thread(
            entrada_audio.ouvir_microfone
            )
        await bot_core(pergunta)
    except Exception as e:
        controlador.controlar_volume_fala(volume_spotify_atual)

async def bot_debug_mode():
    pergunta = await asyncio.to_thread(
        input, "[MODO DEBUG] Insira sua pergunta: "
        )
    await bot_core(pergunta)

async def bot_core(pergunta):
    try:
        resposta_str = await asyncio.to_thread(agenteIA.perguntar, 
                                               pergunta)
        if "&" in resposta_str:
            respostas = resposta_str.split('&')
        else:
            respostas = [resposta_str]
        for resposta in respostas:
            try:
                resposta_json = json.loads(resposta)
                print(resposta_json)
                if resposta_json["tipo"] == "funcao":
                    funcao_nome = resposta_json["funcao"]
                    parametros = resposta_json.get("parametros", {})
                    try:
                        retorno = await asyncio.to_thread(
                            controlador.executar_servico, funcao_nome, 
                            **parametros
                        )
                        if retorno is not None:
                            resumo_web = await asyncio.to_thread(
                                agenteIA.perguntar, f"Resuma: {retorno}"
                            )
                            resumo_web_json = json.loads(resumo_web)
                            await asyncio.to_thread(
                                saida_audio.falar, 
                                resumo_web_json['mensagem']
                            )
                    except Exception as e:
                        print(f"Erro ao executar {funcao_nome}: {e}")
                try:
                    if resposta_json["mensagem"]:
                        await asyncio.to_thread(saida_audio.falar, 
                                                resposta_json["mensagem"])
                except Exception as e:
                    pass
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
    except ValueError as e:
        print(f"Erro ao processar a pergunta: {e}")
   
async def bot_alarmes():
    alarmes = controlador.alarmes.listar_alarmes()
    if alarmes:
        agora = datetime.datetime.now()
        for alarme in alarmes:
            alarme_data_hora = datetime.datetime.strptime(alarme['data_hora'], 
                                                          "%Y-%m-%d %H:%M:%S")
            if alarme_data_hora <= agora:
                controlador.controlar_musica('pause')
                mensagem = f"Lembrete: {alarme['atividade']}"
                saida_audio.falar(mensagem)
                # Testar se o som para ao chamar a lumy
                await asyncio.to_thread(notificacoes.tocar_som_alarme)
                controlador.alarmes.remover_alarme(alarme['atividade'])

# ==================== Loops principais ====================

async def rodar_bot():
    while True:
        if bot_debug:
            await bot_debug_mode()
        else:
            await chamar_bot()

async def rodar_alarmes():
    while True:
        await bot_alarmes()
        await asyncio.sleep(1)
        
async def chamar_bot():
    chamada = await asyncio.to_thread(entrada_audio.ouvir_microfone)
    try:
        if "lume" in chamada:
            controlador.controlar_volume_fala('40')
            saida_audio.parar()
            await bot_ouvir()
    except Exception as e:
        print(e)

# ==================== Função principal ====================

async def bot_main():
    await asyncio.gather(
        rodar_bot(),
        rodar_alarmes()
    )
