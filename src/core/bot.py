import datetime
import json
import asyncio
from src.models.ai_agent import AIAgent
from src.services.audio_controller import EntradaAudio, SaidaAudio
from src.core.controller import Controlador

# Configurações
debug = True  # Coloque True para usar modo debug com input
agenteIA = AIAgent("Zeca", max_tokens=500)
controlador = Controlador()
entrada_audio = EntradaAudio()
saida_audio = SaidaAudio()

# ==================== Funções do Bot ====================

async def bot_listen():
    """
    Escuta o microfone e responde usando a IA
    """
    pergunta = await asyncio.to_thread(entrada_audio.ouvir_microfone)
    await bot_core(pergunta)
            
            
async def bot_debug_mode():
    """
    Modo debug: pergunta via input
    """
    pergunta = await asyncio.to_thread(input, "[MODO DEBUG] Insira sua pergunta: ")
    await bot_core(pergunta)


async def bot_core(pergunta):
    """
    Função core do bot, que pode ser expandida futuramente
    """
    try:
        resposta_str = await asyncio.to_thread(agenteIA.perguntar, pergunta)
        respostas = resposta_str.split('$')
        for item in respostas:
            try:
                resposta = json.loads(item)
                if resposta["tipo"] == "funcao":
                    funcao_nome = resposta["mensagem"]
                    parametros = resposta.get("parametros", {})
                    try:
                        resultado = await asyncio.to_thread(
                            controlador.executar_servico, funcao_nome, **parametros
                        )
    
                    except Exception as e:
                        print(f"Erro ao executar a função {funcao_nome}: {e}")
                else:
                    # if resposta.get('dados_adicionais'):
                    #     agenteIA.salvar_dados_adicionais([resposta.get('dados_adicionais', '')])
                    asyncio.create_task(
                        asyncio.to_thread(saida_audio.falar, resposta['mensagem'])
                    )
                print(f"Resposta do bot: {resposta}")
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                print(f"Resposta recebida: {item}")
    except ValueError as e:
        asyncio.create_task(
            asyncio.to_thread(
                saida_audio.falar,
                "Você atingiu o limite de perguntas. Por favor, tente novamente mais tarde."
            )
        )

        
async def bot_lembrete():
    """
    Checa lembretes e fala os alertas
    """
    lembretes = controlador.lembretes.listar_lembretes()
    if lembretes:
        agora = datetime.datetime.now()
        for lembrete in lembretes:
            if lembrete['data_hora'] <= agora:
                mensagem = f"Lembrete: {lembrete['atividade']} agora."
                print(mensagem)
                await asyncio.to_thread(saida_audio.falar, mensagem)
                controlador.lembretes.remover_lembrete(lembrete['atividade'])

# ==================== Loops principais ====================

async def rodar_bot():
    while True:
        if debug:
            await bot_debug_mode()
        else:
            await bot_listen()
        await asyncio.sleep(0.1)


async def rodar_lembretes():
    while True:
        await bot_lembrete()
        await asyncio.sleep(1)

# ==================== Função principal ====================

async def bot_main():
    await asyncio.gather(
        rodar_bot(),
        rodar_lembretes(),
    )
