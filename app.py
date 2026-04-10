import streamlit as st
# Importamos a nova função de IA que você colocou no main.py
from main import analisar_unidade, VICIOS, SINERGIAS, gerar_analise_ia

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
        # 1. CÁLCULO DE SCORE E SINERGIAS
        soma_base = sum(VICIOS[v]['peso'] for v in vicios_selecionados)
        sinergias_encontradas = []
        vicios_set = set(vicios_selecionados)
        dano_final = soma_base

        for v_comb, info in SINERGIAS.items():
            if set(v_comb).issubset(vicios_set):
                sinergias_encontradas.append(info)
                dano_final *= info['mult']

        score = round(min(dano_final, 10.0), 2)
        
        # 2. SALVAMENTO LOCAL
        analisar_unidade(unidade_id, vicios_selecionados)

        # 3. EXIBIÇÃO DO SCORE
        st.success(f"### Score Final: {score} / 10.0")
        
        if score >= 7.0:
            st.warning("🚨 NÍVEL CRÍTICO DE ATROFIA")
        elif score >= 4.0:
            st.info("⚠️ ALERTA: Atrofia em estágio intermediário.")
        
        if sinergias_encontradas:
            st.write("#### ⚠️ Sinergias Críticas:")
            for s in sinergias_encontradas:
                st.markdown(f"- **{s['nome']}**: Antivírus Sugerido: `{s['av']}`")

        # 4. O PULO DO GATO: CHAMADA DA IA
        st.write("---")
        with st.spinner('🔮 O Oráculo OneThink está processando o destino desta unidade...'):
            # Pegamos o Elo do primeiro vício marcado para dar contexto
            elo_dominante = VICIOS[vicios_selecionados[0]]['elo']
            
            # Chamamos a função de IA que configuramos no main.py
            relatorio_ia = gerar_analise_ia(unidade_id, vicios_selecionados, elo_dominante, score)
            
            st.header("📋 DOSSIÊ DE PREVISÃO (IA)")
            st.markdown(relatorio_ia)
            