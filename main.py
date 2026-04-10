import json
import os
import sys
from datetime import datetime

import google.generativeai as genai
import os

# Configuração da IA (A chave será lida do ambiente ou do código por enquanto)
# Para facilitar agora, pode colar direto aqui, mas o ideal é o .env
genai.configure(api_key="AIzaSyBRDQZGLMc9UTPkVRV3W3y_0s8FgwSYwiY")
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_analise_ia(unidade_id, vicios, elo_dominante, score):
    # O "Contrato" de conduta da IA
    prompt = f"""
    Você é o Oráculo do Sistema OneThink, uma IA de análise de atrofia humana.
    Analise a Unidade: {unidade_id}
    Vícios detectados: {', '.join(vicios)}
    Elo Dominante: {elo_dominante}
    Índice de Atrofia: {score}/10.0

    Com base na teoria dos 4 Elos (Necessidade, Medo, Prazer, Orgulho), gere um dossiê prevendo:
    1. Como será a moradia e o ambiente dessa pessoa em 10 anos?
    2. Qual o tipo de amizades e influências que a cercarão?
    3. Qual o destino profissional inevitável se o índice de atrofia não for reduzido?
    4. Qual o maior 'ponto cego' que ela não está vendo?

    Seja direto, técnico e use um tom de diagnóstico sério.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao conectar com o Oráculo: {str(e)}"
    

# CONFIGURAÇÕES DE SISTEMA
DB_FILE = "database.json"

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
    
    salvar_no_banco(pacote_analise)
    print(f"\n[SISTEMA]: Registro de {unidade_id} imortalizado.")

if __name__ == "__main__":
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

    
