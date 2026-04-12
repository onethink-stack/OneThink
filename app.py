import streamlit as st
from main import (
    analisar_unidade, 
    VICIOS, 
    SINERGIAS, 
    G_LOCAL, 
    G_SOCIAL, 
    G_MONETARIO, 
    G_SOCIAL_MONETARIO, 
    calcular_entropia_social,
    simulador_destino_total
)
from brain import brain
from extractor import extractor
from simulator import rodar_monte_carlo

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="OneThink Stack", page_icon="🔬", layout="wide")

# Inicialização da memória de sessão para evitar reset ao clicar em Monte Carlo
if 'diagnostico_pronto' not in st.session_state:
    st.session_state.diagnostico_pronto = False
    st.session_state.resultados = {}

# --- 2. LÓGICA DO CÉREBRO (SIDEBAR) ---
st.sidebar.header("🧠 OneThink Brain - Contexto")
clima_mundo = st.sidebar.selectbox(
    "Clima do Mundo Atual", 
    ["Estável", "Crise Econômica", "Caos Digital (Trends)"]
)

if clima_mundo == "Crise Econômica":
    brain.injetar_evento_mundo("tensao_economica", 0.9)
elif clima_mundo == "Caos Digital (Trends)":
    brain.injetar_evento_mundo("ruido_digital", 0.9)

# --- 3. TÍTULO E INTERFACE ---
st.title("🧠 SISTEMA ONETHINK")
st.subheader("Módulo de Diagnóstico de Atrofia")

# --- 4. MÓDULO DE INGESTÃO AUTOMÁTICA (EXTRATOR) ---
with st.expander("🕵️ Ingestão de Unidade Isolada (Análise Automática)"):
    input_perfil = st.text_area(
        "Cole aqui dados brutos (Bio, posts, comportamentos):", 
        placeholder="Ex: 'Gosta de TV Girl, fala de várias religiões...'"
    )
    if st.button("ANALISAR PERFIL BRUTO"):
        analise = extractor.analisar_perfil_bruto(input_perfil)
        st.write("### 🔍 Resultados da Extração")
        st.json(analise)
        if analise['vicios_detectados']:
            st.info(f"💡 Sugestão de Vícios para marcar abaixo: {', '.join(analise['vicios_detectados'])}")

st.write("---")

# --- 5. ENTRADA DE DADOS MANUAL ---
unidade_id = st.text_input("ID da Unidade (ex: Alvo-01)", placeholder="Digite o nome ou ID...")

st.write("---")
st.write("### 🔍 Selecione os Vícios Detectados")

col1, col2 = st.columns(2)
vicios_selecionados = []

for i, (codigo, info) in enumerate(VICIOS.items()):
    label = f"{codigo}: {info['nome']} ({info['elo']})"
    if i % 2 == 0:
        if col1.checkbox(label, key=codigo):
            vicios_selecionados.append(codigo)
    else:
        if col2.checkbox(label, key=codigo):
            vicios_selecionados.append(codigo)

st.write("---")
st.write("### 🏗️ Contexto de Geodominância e Alcance (G)")

g_local_id = st.selectbox(
    "G-Local (Ambiente):", 
    options=list(G_LOCAL.keys()), 
    format_func=lambda x: f"{x} - {G_LOCAL[x]['nome']}"
)

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    g_soc_idx = st.selectbox("G-Social (Ocupação):", options=list(G_SOCIAL.keys()), 
                             format_func=lambda x: G_SOCIAL[x]['nome'])
with col_g2:
    g_mon_idx = st.selectbox("G-Monetário (Poder):", options=list(G_MONETARIO.keys()), 
                             format_func=lambda x: G_MONETARIO[x]['nome'])
with col_g3:
    g_sm_idx = st.selectbox("G-SM (Influência):", options=list(G_SOCIAL_MONETARIO.keys()), 
                            format_func=lambda x: G_SOCIAL_MONETARIO[x]['nome'])

# --- 6. EXECUÇÃO DO DIAGNÓSTICO ---
if st.button("EXECUTAR DIAGNÓSTICO", type="primary"):
    if not unidade_id or not vicios_selecionados:
        st.error("⚠️ Por favor, preencha o ID e selecione ao menos um vício.")
    else:
        # LÓGICA DE CÁLCULO
        soma_base = sum(VICIOS[v]['peso'] for v in vicios_selecionados)