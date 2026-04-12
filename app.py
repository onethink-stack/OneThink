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

# --- 6. EXECUÇÃO DO DIAGNÓSTICO (VERSÃO DESTRAVADA) ---
if st.button("EXECUTAR DIAGNÓSTICO", type="primary"):
    if not unidade_id or not vicios_selecionados:
        st.error("⚠️ Por favor, preencha o ID e selecione ao menos um vício.")
    else:
        try:
            # Cálculo de Score e Sinergias
            soma_base = sum(VICIOS[v].get('peso', VICIOS[v].get('weight', 0)) for v in vicios_selecionados)
            vicios_set = set(vicios_selecionados)
            dano_final = soma_base

            sinergias_encontradas = []
            for v_comb, info in SINERGIAS.items():
                if set(v_comb).issubset(vicios_set):
                    dano_final *= info['mult']
                    sinergias_encontradas.append(info)

            score_calc = round(min(dano_final, 10.0), 2)
            
            # Cálculos dos Motores Auxiliares
            entropia_calc = calcular_entropia_social(g_local_id, g_mon_idx, score_calc)
            destino_calc = simulador_destino_total(g_local_id, g_soc_idx, g_mon_idx, vicios_selecionados)

            # Salva tudo na sessão
            st.session_state.resultados = {
                "score": score_calc,
                "entropia": entropia_calc,
                "destino": destino_calc,
                "sinergias": sinergias_encontradas,
                "unidade": unidade_id
            }
            st.session_state.diagnostico_pronto = True
            
            # Atualiza a página para mostrar os resultados
            st.rerun()

        except Exception as e:
            st.error(f"❌ Erro no Motor de Cálculo: {e}")

# --- 7. EXIBIÇÃO DE RESULTADOS (FORA DO BOTÃO PARA EVITAR RESET) ---
if st.session_state.diagnostico_pronto:
    res = st.session_state.resultados
    
    st.success(f"### Score Final: {res['score']} / 10.0")
    
    st.write("---")
    st.header("🔬 DOSSIÊ DE PREVISÃO MATEMÁTICA")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Chance de Travamento (Pa)", res['entropia']['pa'])
        st.write(f"**{res['entropia']['elo']}**")
    
    with res_col2:
        if res['entropia']['travas']:
            for trava in res['entropia']['travas']:
                st.error(f"⚠️ **Trava Ativa:** {trava}")
        else:
            st.success("✅ Nenhuma Trava de Ambiente detectada.")

    st.info(f"🔮 **FATO FUTURO:** {res['entropia']['fato_futuro']}")

    st.write("---")
    st.header("🔮 SIMULAÇÃO DE DESTINO TOTAL")
    col_dna, col_artes = st.columns(2)

    with col_dna:
        st.subheader("🧬 DNA de Atrofia")
        st.write(f"**Gatilho Base:** {res['destino']['gatilho_base']}")
        st.write(f"**Gravidade Ambiental:** {res['destino']['gravidade_meio']}")
        st.write(f"**Teto de Ocupação:** {res['destino']['previsao_ocupacao']}")

    with col_artes:
        st.subheader("🔑 Engenharia de Saída")
        st.write(f"**Soberania Alcancável:** {res['destino']['soberania_alcancavel']}")
        st.write("**Chaves de Libertação (Artes):**")
        for arte in res['destino']['artes_libertadoras']:
            st.markdown(f"- 🏛️ **{arte['nome']}**: {arte['efeito']}")

    if res['sinergias']:
        st.write("#### ⚠️ Sinergias Críticas Detectadas:")
        for s in res['sinergias']:
            st.markdown(f"- **{s['nome']}**: Antivírus Sugerido: `{s['av']}`")

    # --- PASSO 8: MONTE CARLO ---
    st.write("---")
    st.header("🎲 SIMULAÇÃO DE PROBABILIDADE ESTATÍSTICA")
    
    # Extração segura do valor de Pa
    try:
        pa_valor = float(res['entropia']['pa'].replace('%', '')) / 100 
    except:
        pa_valor = 0.5

    if st.button("PROJETAR DESTINOS (MONTE CARLO)"):
        from simulator import rodar_monte_carlo
        stats = rodar_monte_carlo(res['score'], pa_valor)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Probabilidade de Colapso", stats['prob_colapso'])
        c2.metric("Probabilidade de Escape", stats['prob_escape'])
        c3.metric("Resiliência da Unidade", stats['resiliencia'])
        
        st.info(f"💡 Simulação de 1.000 iterações concluída para {res['unidade']}.")

st.write("---")
st.caption("OneThink Stack v3.0 - Motor de Engenharia Social e Artes Liberais Ativo.")
