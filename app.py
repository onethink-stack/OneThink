import streamlit as st
# Importamos a nova função de IA que você colocou no main.py
from main import analisar_unidade, VICIOS, SINERGIAS, G_LOCAL, G_SOCIAL, G_MONETARIO, G_SOCIAL_MONETARIO, calcular_entropia_social, gerar_analise_ia

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
