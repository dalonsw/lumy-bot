import os

class Arquivos:
    def __init__(self):
        pass

    def criar_arquivo_se_nao_existir(caminho):
        if not os.path.exists(caminho):
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("")
            print(f"Arquivo criado em: {caminho}")