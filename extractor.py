# extractor.py

class ContextExtractor:
    def __init__(self):
        # Dicionário de termos que acionam gatilhos automaticamente
        self.gatilhos_semanticos = {
            "ostentação": "V20", # Vangloria
            "ansiedade": "V16",   # Ansiedade
            "militância": "V24",  # Murmuração/Orgulho
            "estética": "V20",    # Foco no Prazer/Imagem
            "religião": "FS_ALTA", # Tentativa de ajuste de frequência
            "algoritmo": "RUIDO"
        }

    def analisar_perfil_bruto(self, texto_perfil):
        """
        Recebe um texto (ex: bio do Insta ou comportamento) 
        e extrai quais Vícios e Gs estão presentes.
        """
        analise = {
            "vicios_detectados": [],
            "pressao_sugerida": 0.5,
            "sinal de alerta": False
        }
        
        texto_low = texto_perfil.lower()
        
        for termo, vicio in self.gatilhos_semanticos.items():
            if termo in texto_low:
                analise["vicios_detectados"].append(vicio)
                analise["sinal de alerta"] = True
        
        return analise

    def capturar_clima_noticias(self, manchete):
        """Traduz notícias em pressão para o Cérebro"""
        if "crise" in manchete or "queda" in manchete:
            return {"tensao_economica": 0.9, "caos_social": 0.7}
        if "viral" in manchete or "trend" in manchete:
            return {"ruido_digital": 0.9}
        return {"ruido_digital": 0.5}

extractor = ContextExtractor()
