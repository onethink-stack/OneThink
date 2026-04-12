import random

def rodar_monte_carlo(score_base, pa_ambiente, tentativas=1000):
    """
    Simula 1000 cenários de vida para a unidade.
    Variando a pressão ambiental (Pa) e o ruído digital.
    """
    sucessos_soberania = 0  # Quantas vezes ela escapa da atrofia
    colapsos_identidade = 0 # Quantas vezes ela vira "lixo genérico"
    
    for _ in range(tentativas):
        # Adiciona ruído aleatório do mundo (0.9 a 1.1)
        variacao_mundo = random.uniform(0.9, 1.1)
        score_simulado = score_base * variacao_mundo
        
        # Lógica de Quebra: Se score + pressão ultrapassar teto crítico
        if score_simulado + (pa_ambiente * 2) > 9.5:
            colapsos_identidade += 1
        elif score_simulado < 4.0:
            sucessos_soberania += 1
            
    prob_colapso = (colapsos_identidade / tentativas) * 100
    prob_escape = (sucessos_soberania / tentativas) * 100
    
    return {
        "prob_colapso": f"{prob_colapso}%",
        "prob_escape": f"{prob_escape}%",
        "resiliencia": "Alta" if prob_escape > 50 else "Crítica"
    }
