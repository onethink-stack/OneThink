import json
import os
import sys
from datetime import datetime
import streamlit as st  # Adicionamos este para ler os segredos da nuvem
import google.generativeai as genai

# --- CONFIGURAÇÃO UNIVERSAL DA IA ---
try:
    chave = st.secrets["GEMINI_API_KEY"]
except:
    chave = "AIzaSyBRDQZGLMc9UTPkVRV3W3y_0s8FgwSYwiY"

genai.configure(api_key=chave)

# Usando o nome técnico completo que evita o erro 404
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
# -----------------------------------------------------------------------------------

# CONFIGURAÇÕES DE SISTEMA
DB_FILE = "database.json"

# --- MATRIZ DE CONTEXTO G (GRAUS DE ALCANCE) ---

G_SOCIAL = {
    1: {"nome": "Subsistência (Inércia)", "desc": "Visão limitada ao dia seguinte."},
    2: {"nome": "Operacional Reativo", "desc": "Executa ordens, refém do meio."},
    3: {"nome": "Técnico Especialista", "desc": "Ilusão de liberdade pelo saber técnico."},
    4: {"nome": "Gestor de Manutenção", "desc": "Mantém o sistema que o escraviza."},
    5: {"nome": "Estrategista Local", "desc": "Vê as peças do tabuleiro regional."},
    6: {"nome": "Arquiteto de Sistemas", "desc": "Vê a corrupção e projeta saídas."},
    7: {"nome": "Emissário (Visão Global)", "desc": "Consciência total do Plano."}
}

G_MONETARIO = {
    1: {"nome": "Déficit", "desc": "Dependência total de terceiros."},
    2: {"nome": "Equilíbrio Precário", "desc": "Um imprevisto destrói a estrutura."},
    3: {"nome": "Conforto Relativo", "desc": "O 'Rei do Meio'. Gera Orgulho local."},
    4: {"nome": "Segurança Estagnada", "desc": "Inércia pelo medo do risco de subir."},
    5: {"nome": "Acúmulo de Poder", "desc": "Dinheiro usado como Artes ou Vício."},
    6: {"nome": "Liberdade Geográfica", "desc": "O dinheiro descola a unidade do chão."},
    7: {"nome": "Soberania (Capital Próprio)", "desc": "O dinheiro serve à ideia."}
}

G_SOCIAL_MONETARIO = {
    1: {"nome": "Invisível", "desc": "Sem voz ou impacto no grupo."},
    2: {"nome": "Seguidor", "desc": "Validado pela massa."},
    3: {"nome": "Liderança de Bolha", "desc": "Pequeno poder que infla o Orgulho (E3)."},
    4: {"nome": "Influenciador", "desc": "Gera necessidade nos outros."},
    5: {"nome": "Detentor de Portas", "desc": "Quem decide quem entra e quem sai."},
    6: {"nome": "Autoridade Reconhecida", "desc": "O nome precede a presença."},
    7: {"nome": "Titã / Patriarca", "desc": "Cria as regras do jogo social."}
}

G_LOCAL = {
    "G-L1": {"nome": "Zona de Conflito", "rank": 0.1, "pa": 0.98, "elo": "Medo (Sobrevivência)"},
    "G-L2": {"nome": "Periferia Travada", "rank": 0.3, "pa": 0.85, "elo": "Necessidade (Inércia)"},
    "G-L3": {"nome": "Classe Média Adaptada", "rank": 0.5, "pa": 0.70, "elo": "Prazer (Compensação)"},
    "G-L4": {"nome": "Reduto de Status", "rank": 0.6, "pa": 0.65, "elo": "Orgulho (Superioridade)"},
    "G-L5": {"nome": "Hub de Negócios", "rank": 0.7, "pa": 0.45, "elo": "Orgulho/Prazer (Pressa)"},
    "G-L6": {"nome": "Bunker Controlado", "rank": 0.9, "pa": 0.15, "elo": "Nenhum (Proteção de FS)"},
    "G-L7": {"nome": "Geodominância", "rank": 1.0, "pa": 0.05, "elo": "Soberania (Visão Global)"}
}

def calcular_entropia_social(g_local_id, g_mon_idx, score_vicios):
    gl = G_LOCAL[g_local_id]
    rank = gl['rank']
    pa = gl['pa']
    
    fato_futuro = ""
    analise_elo = ""
    travas_detectadas = []

    # 1. LÓGICA: O ABISMO (0.1 - 0.3)
    if rank <= 0.3:
        analise_elo = "ELO Predominante: Medo e Necessidade (Sobrevivência)."
        fato_futuro = (
            "SUBPRODUTO ESTATÍSTICO: A energia da unidade é 100% consumida pela geolocalização. "
            "O ELO de Medo trava a imaginação; sem intervenção externa (mentor), "
            "a unidade é incapaz de conceber uma saída."
        )
        travas_detectadas.append("T-Sobrevivência: Bloqueio de Cognição de Saída")

    # 2. LÓGICA: O POÇO DE COMPENSAÇÃO (0.4 - 0.6)
    elif 0.4 <= rank <= 0.6:
        analise_elo = "ELO Predominante: Prazer e Orgulho (Compensação)."
        # Cruzamento com G-Monetário (O Rei da Favela)
        if g_mon_idx >= 3:
            fato_futuro = (
                "O REI DA FAVELA: G-Monetário alto para o local. "
                "A unidade defenderá a própria gaiola pois o ranking dá a ilusão de vitória. "
                "Risco máximo de V20 (Vangloria)."
            )
            travas_detectadas.append("T-Moral: Cristalização por Superioridade Intelectual")
        else:
            fato_futuro = (
                "ESTAGNAÇÃO: A unidade usa o Prazer para não sentir a falta de movimento. "
                "O ambiente 'confortável' é o maior inimigo da evolução."
            )

    # 3. LÓGICA: ZONA DE ESCAPE (0.7 - 1.0)
    else:
        analise_elo = "ELO em Atrofia: Alcance de Percepção Desbloqueado."
        fato_futuro = (
            "POTENCIAL OPERADOR: Necessidade física inexistente. "
            "O travamento aqui ocorre apenas por Vontade Própria (Vícios Morais). "
            "Tratar como Titã Concorrente ou Aliado Estratégico."
        )

    return {
        "pa": f"{pa*100}%",
        "elo": analise_elo,
        "fato_futuro": fato_futuro,
        "travas": travas_detectadas
    }


# DATABASE BRUTO DO SISTEMA ONETHINK
VICIOS = {
    # I. O ELO DA NECESSIDADE (Alvo: O Minerador)
    "V26": {"nome": "Ignorância", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.7, "atrofia": "G1:E1"},
    "V7":  {"nome": "Preguiça", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.8, "atrofia": "FS4"},
    "V8":  {"nome": "Mentira", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.6, "atrofia": "G1"},
    "V23": {"nome": "Credulidade", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.5, "atrofia": "G1"},
    "V6":  {"nome": "Gula", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.7, "atrofia": "G1"},
    "V11": {"nome": "Distração", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.9, "atrofia": "G1"},
    "V24": {"nome": "Murmuração", "elo": "Necessidade", "alvo": "Minerador", "peso": 0.6, "atrofia": "G1"},

    # II. O ELO DO MEDO (Alvo: O Cuidador/Educador)
    "V13": {"nome": "Medo", "elo": "Medo", "alvo": "Educador", "peso": 0.9, "atrofia": "G2:E2"},
    "V12": {"nome": "Procrastinação", "elo": "Medo", "alvo": "Educador", "peso": 0.7, "atrofia": "A6"},
    "V14": {"nome": "Covardia", "elo": "Medo", "alvo": "Educador", "peso": 0.8, "atrofia": "G2"},
    "V17": {"nome": "Nostalgia", "elo": "Medo", "alvo": "Educador", "peso": 0.5, "atrofia": "G2"},
    "V21": {"nome": "Fanatismo", "elo": "Medo", "alvo": "Educador", "peso": 0.8, "atrofia": "G2"},
    "V10": {"nome": "Maledicência", "elo": "Medo", "alvo": "Educador", "peso": 0.7, "atrofia": "G2"},
    "V27": {"nome": "Ingratidão", "elo": "Medo", "alvo": "Educador", "peso": 0.6, "atrofia": "G2"},

    # III. O ELO DO PRAZER (Alvo: O Regulador)
    "V20": {"nome": "Vangloria", "elo": "Prazer", "alvo": "Regulador", "peso": 0.8, "atrofia": "G4:E4"},
    "V5":  {"nome": "Luxúria", "elo": "Prazer", "alvo": "Regulador", "peso": 0.8, "atrofia": "G4"},
    "V3":  {"nome": "Inveja", "elo": "Prazer", "alvo": "Regulador", "peso": 0.9, "atrofia": "G4"},
    "V19": {"nome": "Impulsividade", "elo": "Prazer", "alvo": "Regulador", "peso": 0.7, "atrofia": "G4"},
    "V15": {"nome": "Adulação", "elo": "Prazer", "alvo": "Regulador", "peso": 0.5, "atrofia": "G4"},
    "V16": {"nome": "Ansiedade A.", "elo": "Prazer", "alvo": "Regulador", "peso": 0.9, "atrofia": "FS3"},
    "V9":  {"nome": "Fofoca", "elo": "Prazer", "alvo": "Regulador", "peso": 0.6, "atrofia": "G4"},

    # IV. O ELO DO ORGULHO (Alvo: O Explorador)
    "V1":  {"nome": "Orgulho", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.9, "atrofia": "G6:E6"},
    "V25": {"nome": "Hubris", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.9, "atrofia": "A5"},
    "V22": {"nome": "Cinismo", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.7, "atrofia": "G6"},
    "V18": {"nome": "Hipocrisia", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.8, "atrofia": "G6"},
    "V4":  {"nome": "Avareza", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.8, "atrofia": "G6"},
    "V2":  {"nome": "Ira", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.9, "atrofia": "FS1"},
    "V28": {"nome": "Ressentimento", "elo": "Orgulho", "alvo": "Explorador", "peso": 0.9, "atrofia": "G6"}
}

SINERGIAS = {
    # --- ELO DA NECESSIDADE (SOBREVIVÊNCIA) ---
    ("V7", "V12"): {"nome": "INÉRCIA ABSOLUTA", "mult": 1.5, "av": "A4-ARITMÉTICA"},
    ("V26", "V23"): {"nome": "ESTUPOR COLETIVO", "mult": 1.4, "av": "A3-FILOSOFIA"},
    ("V8", "V24"): {"nome": "VITIMISMO TÓXICO", "mult": 1.3, "av": "A2-LÓGICA"},

    # --- ELO DO MEDO (SOCIAL) ---
    ("V13", "V6"): {"nome": "CONSUMISMO DE ESCAPE", "mult": 1.4, "av": "A1-JEJUM"},
    ("V10", "V27"): {"nome": "ISOLAMENTO MALIGNO", "mult": 1.5, "av": "A6-GRATIDÃO"},

    # --- ELO DO PRAZER (EGO/ALGORITMO) ---
    ("V11", "V20"): {"nome": "VITRINE VAZIA", "mult": 1.6, "av": "A3-FILOSOFIA"},
    ("V16", "V20"): {"nome": "ESCRAVIDÃO DA IMAGEM", "mult": 1.7, "av": "A5-AUTOESTIMA"},
    ("V11", "V16", "V20"): {"nome": "LOOP DOPAMINÉRGICO", "mult": 2.0, "av": "A1-JEJUM DIGITAL"},

    # --- ELO DO ORGULHO (ESPIRITUAL/HUBRIS) ---
    ("V16", "V25"): {"nome": "COLAPSO ESTRUTURAL", "mult": 1.8, "av": "A2-LÓGICA"},
    ("V1", "V3"): {"nome": "COMPLEXO DE NARCISO", "mult": 1.6, "av": "A6-HUMILDADE"},
    ("V15", "V25"): {"nome": "CÂMARA DE ECO", "mult": 1.5, "av": "A2-DIALÉTICA"},
    ("V2", "V28"): {"nome": "VINDITA CEGA", "mult": 1.9, "av": "A7-PERDÃO"},
    ("V18", "V22"): {"nome": "DECOMPOSIÇÃO MORAL", "mult": 1.7, "av": "A3-ÉTICA"},
    
# --- PONTES ENTRE ELOS ---
    ("V21", "V2"): {"nome": "FANATISMO AGRESSIVO", "mult": 1.6, "av": "A2-LÓGICA"},
    ("V8", "V19"): {"nome": "FRAUDE SISTÊMICA", "mult": 1.5, "av": "A3-HONRA"},
    
    # --- O PERIGO MÁXIMO ---
    ("V1", "V2", "V4", "V25"): {"nome": "TIRANIA DO EU", "mult": 2.5, "av": "A0-MORTE DO EGO"},

    # --- SINERGIAS RESIDUAIS (OS PONTOS CEGOS) ---
    ("V26", "V21"): {"nome": "OBSCURANTISMO", "mult": 1.5, "av": "A3-ESTUDO"},
    ("V4", "V5"): {"nome": "MERCANTILIZAÇÃO DO SER", "mult": 1.6, "av": "A0-VALORES"},
    ("V23", "V15"): {"nome": "CEGUEIRA INDUZIDA", "mult": 1.4, "av": "A2-CRÍTICA"}
}

def salvar_no_banco(dados_da_analise):
    registros = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except:
                registros = []

    registros.append(dados_da_analise)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)

def analisar_unidade(unidade_id, vicios_input):
    print(f"\n--- RELATÓRIO ONETHINK: {unidade_id} ---")
    dano_total = 0
    sinergias_ativas = []
    
    # Detecção de Sinergias
    vicios_set = set(vicios_input)
    for par, info in SINERGIAS.items():
        if set(par).issubset(vicios_set):
            sinergias_ativas.append(info)
            
    # Cálculo de Impacto
    for v in vicios_input:
        if v in VICIOS:
            v_info = VICIOS[v]
            impacto = v_info['peso']
            
            for s in sinergias_ativas:
                impacto *= s['mult']
                
            print(f"[!] Vício: {v_info['nome']} | Alvo: {v_info['atrofia']} | Impacto: {impacto:.2f}")
            dano_total += impacto

    if sinergias_ativas:
        print("\n--- SINERGIAS CRÍTICAS ---")
        for s in sinergias_ativas:
            print(f"⚠️ {s['nome']} detectada! Antivírus: {s['av']}")

    final_score = round(min(dano_total, 10.0), 2)
    print(f"\nÍNDICE DE ATROFIA TOTAL: {final_score}/10.0")

    # PREPARAÇÃO PARA PERSISTÊNCIA
    pacote_analise = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": unidade_id,
        "vicios": vicios_input,
        "sinergias": [s['nome'] for s in sinergias_ativas],
        "atrofia_calculada": final_score
    }
    
# --- DICIONÁRIO DAS 7 ARTES (O ANTIVÍRUS PRÁTICO) ---
# Aqui unimos o Trivium/Quadrivium à ação de quebra de Elo
ARTES = {
    "A1": {"nome": "Jejum/Abstinência (Gramática)", "efeito": "Quebra Elo de Prazer"},
    "A2": {"nome": "Dialética/Lógica (Lógica)", "efeito": "Quebra Elo de Orgulho"},
    "A3": {"nome": "Estudo/Filosofia (Retórica)", "efeito": "Aumenta Alcance de Percepção"},
    "A4": {"nome": "Trabalho Braçal (Aritmética)", "efeito": "Ancoragem na Realidade"},
    "A5": {"nome": "Autoexame (Geometria)", "efeito": "Identificação de Gatilhos e Limites"},
    "A6": {"nome": "Contemplação/Beleza (Música)", "efeito": "Restauração de FS (Frequência)"},
    "A7": {"nome": "Caridade Silenciosa (Astronomia)", "efeito": "Morte do Ego (Soberania)"}
}

# --- MOTOR DE SIMULAÇÃO 10^94 (A GRANDE LIGAÇÃO) ---
def simulador_destino_total(g_local, g_soc, g_mon, vicios_selecionados):
    # 1. Cálculo de Base (Ambiente + Poder)
    gl = G_LOCAL[g_local]
    forca_meio = gl['pa'] # Gravidade do ambiente (Chance de travamento)
    alcance_inicial = g_soc # G-Social define o teto de ocupação
    
    # 2. Processamento de ELOs Ativos
    elos_ativos = list(set([VICIOS[v]['elo'] for v in vicios_selecionados]))
    
    # 3. Lógica de Predição de Gatilhos (Triangulação de Matriz)
    gatilho_predominante = ""
    if "Medo" in elos_ativos and gl['rank'] <= 0.3:
        gatilho_predominante = "Covardia por Sobrevivência (Inibição de FS)"
    elif "Orgulho" in elos_ativos and g_mon >= 3:
        gatilho_predominante = "Superioridade Ilusória (Rei do Poço)"
    elif "Prazer" in elos_ativos and 0.4 <= gl['rank'] <= 0.6:
        gatilho_predominante = "Compensação Dopaminérgica (Fuga do Real)"
    else:
        gatilho_predominante = "Inércia Mecânica (Seguidor)"

    # 4. Cálculo do Antivírus (A Arte que quebra o Elo específico)
    sugestao_arte = []
    if "Prazer" in elos_ativos: 
        sugestao_arte.append(ARTES["A1"])
        sugestao_arte.append(ARTES["A6"])
    if "Orgulho" in elos_ativos: 
        sugestao_arte.append(ARTES["A2"])
        sugestao_arte.append(ARTES["A7"])
    if "Medo" in elos_ativos: 
        sugestao_arte.append(ARTES["A5"])
        sugestao_arte.append(ARTES["A3"])
    if not sugestao_arte: # Caso padrão
        sugestao_arte.append(ARTES["A4"])

    return {
        "gravidade_meio": f"{forca_meio * 100}%",
        "gatilho_base": gatilho_predominante,
        "previsao_ocupacao": G_SOCIAL[alcance_inicial]['nome'],
        "artes_libertadoras": sugestao_arte,
        "soberania_alcancavel": "Alta" if gl['rank'] >= 0.7 else "Baixa (Requer Mentor/Artes)"
    }

    salvar_no_banco(pacote_analise)
    print(f"\n[SISTEMA]: Registro de {unidade_id} imortalizado.")

if __name__ == "__main__":
    print("OneThink Engine Ativo.")
    print("="*30)
    print(" SISTEMA ONETHINK: TERMINAL ")
    print("="*30)
    
    # O programa para e espera você digitar o nome
    nome_unidade = input("\n> Digite o ID da Unidade (ex: Alvo-01): ")
    
    # O programa espera você digitar os códigos
    print("\nVícios disponíveis: V7, V12, V16, V25")
    vicios_digitados = input("> Digite os códigos separados por vírgula (ex: V7, V12): ")
    
    # Esse comando limpa o que você digitou para o Python entender
    lista_vicios = [v.strip().upper() for v in vicios_digitados.split(",")]
    
    # Agora ele chama a análise com o que VOCÊ escreveu
    analisar_unidade(nome_unidade, lista_vicios)

    
