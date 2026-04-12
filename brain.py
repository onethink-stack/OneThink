import random

class OneThinkBrain:
    def __init__(self):
        # O Clima Global afeta a gravidade de todos os G-Locais
        self.clima_global = {
            "tensao_economica": 0.5, # 0 a 1
            "ruido_digital": 0.8,    # Afeta a FS (Frequência Seletiva)
            "caos_social": 0.3
        }

    def injetar_evento_mundo(self, evento, intensidade):
        """Injeta um dado do mundo real na simulação"""
        if evento in self.clima_global:
            self.clima_global[evento] = intensidade
            return f"Alerta: O evento {evento} alterou a pressão da Matriz para {intensidade}."

    def simular_reacao(self, perfil_unidade):
        """Preve como o perfil reage ao clima atual"""
        # Exemplo: Se o ruído digital está alto, unidades com G-S3/S4 sofrem mais atrofia
        probabilidade_colapso = (perfil_unidade['score'] * self.clima_global['ruido_digital']) / 10
        
        if probabilidade_colapso > 0.7:
            return "Destino: Dissolução de Identidade (Alta Probabilidade)"
        else:
            return "Destino: Estabilidade Temporária"

# Inicia o cérebro
brain = OneThinkBrain()
