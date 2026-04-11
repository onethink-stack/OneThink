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

# Configuração da página
st.set_page_config(page_title="OneThink Stack", page_icon="🔬")

st.title("🧠 SISTEMA ONETHINK")
st.subheader("Módulo de Diagnóstico de Atrofia")

# Entrada de ID
unidade_id = st.text_input("ID da Unidade (ex: Alvo-01)", placeholder="Digite o nome ou ID...")

st.write("---")
st.write("### 🔍 Selecione os Vícios Detectados")

# Criando colunas para os vícios
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

# Seletor de Ambiente (G-Local)
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

# BOTÃO DE EXECUÇÃO
if st.button("EXECUTAR DIAGNÓSTICO", type="primary"):
            if not unidade_id or not vicios_selecionados:
                st.error("⚠️ Por favor, preencha o ID e selecione ao menos um vício.")
            else:
                # 1. CÁLCULO DE SCORE E SINERGIAS
                soma_base = sum(VICIOS[v]['weight'] for v in vicios_selecionados) if 'weight' in VICIOS[vicios_selecionados[0]] else sum(VICIOS[v]['peso'] for v in vicios_selecionados)
                sinergias_encontradas = []
                vicios_set = set(vicios_selecionados)
                dano_final = soma_base

                for v_comb, info in SINERGIAS.items():
                    if set(v_comb).issubset(vicios_set):
                        sinergias_encontradas.append(info)
                        dano_final *= info['mult']

                score = round(min(dano_final, 10.0), 2)

                # 2. EXIBIÇÃO DO SCORE
                st.success(f"### Score Final: {score} / 10.0")
                
                if score >= 7.0:
                    st.warning("🚨 NÍVEL CRÍTICO DE ATROFIA")
                elif score >= 4.0:
                    st.info("⚠️ ALERTA: Atrofia em estágio intermediário.")

                # 3. ANÁLISE DE ENTROPIA SOCIAL (G)
                st.write("---")
                st.header("🔬 DOSSIÊ DE PREVISÃO MATEMÁTICA")
                
                entropia = calcular_entropia_social(g_local_id, g_mon_idx, score)
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric("Chance de Travamento (Pa)", entropia['pa'])
                    st.write(f"**{entropia['elo']}**")
                
                with res_col2:
                    if entropia['travas']:
                        for trava in entropia['travas']:
                            st.error(f"⚠️ **Trava Ativa:** {trava}")
                    else:
                        st.success("✅ Nenhuma Trava de Ambiente detectada.")

                st.info(f"🔮 **FATO FUTURO:** {entropia['fato_futuro']}")

                # --- 4. GRANDE LIGAÇÃO: PREVISÃO DE DESTINO (10^94) ---
                st.write("---")
                st.header("🔮 SIMULAÇÃO DE DESTINO TOTAL")

                # Chamada do motor de simulação que liga Gs, ELOs e Artes Liberais
                destino = simulador_destino_total(g_local_id, g_soc_idx, g_mon_idx, vicios_selecionados)

                col_dna, col_artes = st.columns(2)

                with col_dna:
                    st.subheader("🧬 DNA de Atrofia")
                    st.write(f"**Gatilho Base:** {destino['gatilho_base']}")
                    st.write(f"**Gravidade Ambiental:** {destino['gravidade_meio']}")
                    st.write(f"**Teto de Ocupação:** {destino['previsao_ocupacao']}")

                with col_artes:
                    st.subheader("🔑 Engenharia de Saída")
                    st.write(f"**Soberania Alcancável:** {destino['soberania_alcancavel']}")
                    st.write("**Chaves de Libertação (Artes):**")
                    for arte in destino['artes_libertadoras']:
                        st.markdown(f"- 🏛️ **{arte['nome']}**: {arte['efeito']}")

                st.info(f"💡 **CONCLUSÃO DO ESTRATEGISTA:** Sob o gatilho '{destino['gatilho_base']}', o destino converge para '{destino['previsao_ocupacao']}'. A quebra exige prática de {destino['artes_libertadoras'][0]['nome']}.")

                # 5. EXIBIÇÃO DE SINERGIAS CRÍTICAS
                if sinergias_encontradas:
                    st.write("---")
                    st.write("#### ⚠️ Sinergias Críticas Detectadas:")
                    for s in sinergias_encontradas:
                        st.markdown(f"- **{s['nome']}**: Antivírus Sugerido: `{s['av']}`")

                st.write("---")
                st.caption("OneThink Stack v3.0 - Motor de Engenharia Social e Artes Liberais Ativo.")
