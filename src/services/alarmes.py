import datetime

class Alarmes:
    def __init__(self, cache_file='./src/cache/alarms.json'):
        self.alarmes = []
        self.cache_file = cache_file

    def adicionar_alarme(self, atividade, data_hora, repetir=None):
        alarme = {
            'atividade': atividade,
            'data_hora': data_hora,
            'repetir': repetir
        }
        self.alarmes.append(alarme)

    def listar_alarmes(self):
        return self.alarmes

    def modificar_alarme(self, atividade, nova_data_hora):
        for alarme in self.alarmes:
            if alarme['atividade'] == atividade:
                alarme['data_hora'] = nova_data_hora
                return True
        return False

    def remover_alarme(self, atividade):
        for alarme in self.alarmes:
            if alarme['atividade'] == atividade:
                self.alarmes.remove(alarme)
                return True
        return False

    def alertar_alarmes(self):
        agora = datetime.datetime.now()
        alertas = []
        for alarme in self.alarmes:
            if alarme['data_hora'] == agora:
                alertas.append(alarme)
        return alertas
    