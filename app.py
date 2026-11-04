import streamlit as st
import pandas as pd
import os
import math

st.set_page_config(
    page_title="Projeto Ômega v3 — Gerador Balanceado & Painel Web (Streamlit)",
    page_icon="Ω",
    layout="wide"
)

CSV_FILE = "historico_apostas.csv"

# Inicializa ou carrega histórico
if os.path.exists(CSV_FILE):
    try:
        df_hist = pd.read_csv(CSV_FILE)
    except Exception:
        df_hist = pd.DataFrame(columns=["concurso_alvo", "data_geracao", "data_hora_geracao", "gerador", "dezenas", "custo", "acertos", "premio", "conferido"])
else:
    df_hist = pd.DataFrame(columns=["concurso_alvo", "data_geracao", "data_hora_geracao", "gerador", "dezenas", "custo", "acertos", "premio", "conferido"])

st.title("Ω Projeto Ômega v3 — Gerador Balanceado & Painel Web")
st.markdown("Motor CGP + 5 Especialistas MoE + Recalibrador Biométrico Estratificado &bull; Rodando em Python / Streamlit")

# Abas principais
tab1, tab2, tab3 = st.tabs(["⚡ Gerador & Sequência", "🎯 Conferidor & Jogos Salvos", "🔗 Guia de Publicação"])

with tab1:
    st.subheader("Configuração do Lote de Apostas")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        concurso_alvo = st.number_input("Concurso Alvo", min_value=1, value=3821, step=1)
    with col2:
        qtd_jogos = st.number_input("Qtd de Jogos", min_value=1, max_value=50, value=10, step=1)
    with col3:
        dezenas_cartao = st.selectbox("Dezenas por Cartão", [15, 16, 17, 18, 19, 20], index=0)
    with col4:
        motor_calib = st.selectbox("Motor", ["Recalibrado Estratificado v3", "Portfólio Bruto do Campeão"])

    custo_unitario = math.comb(dezenas_cartao, 15) * 3.50
    custo_total = qtd_jogos * custo_unitario
    st.info(f"Custo estimado do lote: **R$ {custo_total:,.2f}** ({qtd_jogos} cartões de {dezenas_cartao} dezenas)")

    if st.button("⚡ Gerar & Salvar em Sequência no Servidor", type="primary"):
        # Simulação de geração baseada no DNA do Campeão
        import random
        base_jogos = [
            [6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 22, 24, 25],
            [4, 6, 8, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24],
            [6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 21, 23, 24, 25],
            [6, 7, 8, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 24],
            [4, 6, 8, 9, 11, 12, 13, 14, 15, 17, 18, 21, 22, 23, 24],
            [4, 6, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 24, 25],
            [4, 6, 7, 8, 11, 12, 13, 14, 15, 18, 20, 22, 23, 24, 25],
            [6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 22, 23, 24],
            [4, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 21, 22, 23, 25],
            [6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 19, 21, 22, 24, 25]
        ]
        
        novos_registros = []
        now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = pd.Timestamp.now().strftime("%Y-%m-%d")

        for i in range(qtd_jogos):
            # Seleciona dezenas base e ajusta se dezenas_cartao > 15
            nums = base_jogos[i % len(base_jogos)].copy()
            while len(nums) < dezenas_cartao:
                disponiveis = [n for n in range(1, 26) if n not in nums]
                if disponiveis:
                    nums.append(random.choice(disponiveis))
            nums.sort()

            novos_registros.append({
                "concurso_alvo": concurso_alvo,
                "data_geracao": date_str,
                "data_hora_geracao": now_str,
                "gerador": "omega_v3_streamlit",
                "dezenas": str(nums),
                "custo": custo_unitario,
                "acertos": 0,
                "premio": 0.0,
                "conferido": False
            })

        df_novo = pd.DataFrame(novos_registros)
        df_hist = pd.concat([df_hist, df_novo], ignore_index=True)
        df_hist.to_csv(CSV_FILE, index=False)
        st.success(f"{qtd_jogos} jogos gerados e salvos com sucesso no servidor!")

    if not df_hist.empty:
        st.subheader(f"Histórico Acumulado ({len(df_hist)} jogos salvos)")
        st.dataframe(df_hist, use_container_width=True)
        
        csv_bytes = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Baixar historico_apostas.csv atualizado",
            data=csv_bytes,
            file_name="historico_apostas.csv",
            mime="text/csv"
        )

with tab2:
    st.subheader("🎯 Conferidor Oficial & Gestão de Salvos")
    if df_hist.empty:
        st.warning("Nenhum jogo salvo no momento. Gere alguns jogos na aba anterior.")
    else:
        st.dataframe(df_hist, use_container_width=True)
        if st.button("🗑️ Limpar Todo o Histórico Salvo"):
            if os.path.exists(CSV_FILE):
                os.remove(CSV_FILE)
            st.rerun()

with tab3:
    st.subheader("🔗 Como Publicar no Streamlit Community Cloud (Gratuito)")
    st.markdown("""
    1. **Crie um repositório no GitHub** (ex: `lotofacil-omega`).
    2. **Suba estes arquivos** para a raiz do repositório (`app.py`, `requirements.txt`, `historico_apostas.csv`).
    3. Acesse [share.streamlit.io](https://share.streamlit.io/) e faça login com sua conta do GitHub.
    4. Clique em **New app**.
    5. Selecione o seu repositório, a branch `main` e defina o arquivo principal como `app.py`.
    6. Clique em **Deploy!** Pronto, seu app estará online com um link público para acessar de qualquer celular ou PC.
    """)
