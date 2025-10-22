import datetime
import json

class Alarmes:
    def __init__(self, cache_file='./src/cache/alarmes.json'):
        self.alarmes = []
        self.cache_file = cache_file
        self.carregar_alarmes()

    def adicionar_alarme(self, atividade, data_hora, repetir=None):
        alarme = {
            'atividade': atividade,
            'data_hora': data_hora,
            'repetir': repetir
        }
        self.alarmes.append(alarme)
        self.salvar_alarmes()
        
    def listar_alarmes(self):
        return self.alarmes

    def modificar_alarme(self, atividade, nova_data_hora):
        for alarme in self.alarmes:
            if alarme['atividade'] == atividade:
                alarme['data_hora'] = nova_data_hora
                self.salvar_alarmes()
                return True
        return False

    def remover_alarme(self, atividade):
        for alarme in self.alarmes:
            if alarme['atividade'] == atividade:
                self.alarmes.remove(alarme)
                self.salvar_alarmes()
                return True
        return False

    def alertar_alarmes(self):
        agora = datetime.datetime.now()
        alertas = []
        for alarme in self.alarmes:
            if alarme['data_hora'] == agora:
                alertas.append(alarme)
        return alertas
    
    def salvar_alarmes(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.alarmes, f, default=str)
            
    def carregar_alarmes(self):
        with open(self.cache_file, 'r') as f:
            self.alarmes = json.load(f)