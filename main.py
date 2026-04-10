import json
import os
import sys
from datetime import datetime

# CONFIGURAÇÕES DE SISTEMA
DB_FILE = "database.json"

# DATABASE BRUTO DO SISTEMA ONETHINK
VICIOS = {
    "V7":  {"nome": "Preguiça", "atrofia": "FS4", "peso": 0.8},
    "V12": {"nome": "Procrastinação", "atrofia": "A6", "peso": 0.7},
    "V16": {"nome": "Ansiedade", "atrofia": "FS3", "peso": 0.9},
    "V25": {"nome": "Hubris", "atrofia": "A5", "peso": 0.9}
}

SINERGIAS = {
    ("V7", "V12"): {"nome": "INÉRCIA ABSOLUTA", "mult": 1.5, "av": "A4-ARITMÉTICA"},
    ("V16", "V25"): {"nome": "COLAPSO ESTRUTURAL", "mult": 1.8, "av": "A2-LÓGICA"}
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

    
