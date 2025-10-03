import datetime

class Lembretes:
    def __init__(self):
        self.lembretes = []

    def adicionar_lembrete(self, atividade, data_hora):
        lembrete = {
            'atividade': atividade,
            'data_hora': data_hora
        }
        self.lembretes.append(lembrete)

    def listar_lembretes(self):
        return self.lembretes
    
    def alterar_lembrete(self, atividade, nova_data_hora):
        for lembrete in self.lembretes:
            if lembrete['atividade'] == atividade:
                lembrete['data_hora'] = nova_data_hora
                return True
        return False

    def remover_lembrete(self, atividade):
        for lembrete in self.lembretes:
            if lembrete['atividade'] == atividade:
                self.lembretes.remove(lembrete)
                return True
        return False
    
    def alertar_lembretes(self):
        agora = datetime.datetime.now()
        alertas = []
        for lembrete in self.lembretes:
            if lembrete['data_hora'] == agora:
                alertas.append(lembrete)
        return alertas
    