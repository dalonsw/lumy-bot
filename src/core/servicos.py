from src.services.calendario import definir_lembrete

servicos_registrados = {
    'definir_lembrete': definir_lembrete,
}

def bot_servicos(funcao_nome, *args, **kwargs):
    if funcao_nome in servicos_registrados:
        return servicos_registrados[funcao_nome](*args, **kwargs)
    else:
        raise ValueError(f"Função '{funcao_nome}' não está registrada nos serviços.")