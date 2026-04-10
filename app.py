import streamlit as st
from main import analisar_unidade, VICIOS, SINERGIAS

# Configuração da página do site
st.set_page_config(page_title="ONETHINK - Onisciência", page_icon="🧠", layout="centered")

st.title("🧠 SISTEMA ONETHINK")
st.subheader("Módulo de Diagnóstico de Atrofia")

# Entrada de ID
unidade_id = st.text_input("ID da Unidade (ex: Alvo-01)", placeholder="Digite o nome ou ID...")

st.write("---")
st.write("### 🔍 Selecione os Vícios Detectados")

# Criando colunas para o site não ficar gigante para baixo
col1, col2 = st.columns(2)
vicios_selecionados = []

# Organiza os 28 vícios nas colunas
for i, (codigo, info) in enumerate(VICIOS.items()):
    label = f"{codigo}: {info['nome']} ({info['elo']})"
    if i % 2 == 0:
        if col1.checkbox(label, key=codigo):
            vicios_selecionados.append(codigo)
    else:
        if col2.checkbox(label, key=codigo):
            vicios_selecionados.append(codigo)

st.write("---")

if st.button("EXECUTAR DIAGNÓSTICO", type="primary"):
    if not unidade_id or not vicios_selecionados:
        st.error("⚠️ Por favor, preencha o ID e selecione ao menos um vício.")
    else:
        # Calculando para exibição no site
        soma_base = sum(VICIOS[v]['peso'] for v in vicios_selecionados)
        sinergias_nomes = []
        vicios_set = set(vicios_selecionados)
        dano_final = soma_base

        for v_comb, info in SINERGIAS.items():
            if set(v_comb).issubset(vicios_set):
                sinergias_nomes.append(info)
                dano_final *= info['mult']

        score = round(min(dano_final, 10.0), 2)
        
        # Salvando no banco de dados local
        analisar_unidade(unidade_id, vicios_selecionados)

        # Exibição dos Resultados no Site
        st.success(f"### Score Final: {score} / 10.0")
        
        if score >= 7.0:
            st.warning("🚨 NÍVEL CRÍTICO DE ATROFIA")
        elif score >= 4.0:
            st.info("⚠️ ALERTA: Atrofia em estágio intermediário.")
        
        if sinergias_nomes:
            st.write("#### ⚠️ Sinergias Críticas:")
            for s in sinergias_nomes:
                st.markdown(f"- **{s['nome']}**: Antivírus Sugerido: `{s['av']}`")
                