# app.py

import streamlit as st
import pandas as pd
from data_loader import carregar_dados, filtrar_dados_por_estado
from database import get_connection, salvar_interacao # <-- IMPORTE AS NOVAS FUNÇÕES

# --- Configuração da Página ---
st.set_page_config(
    page_title="Jornada de Inovação em Saúde",
    page_icon="⚕️",
    layout="wide"
)

# --- CONEXÃO COM O BANCO DE DADOS ---
engine = get_connection()

# --- Título e Descrição ---
st.title("⚕️ Jornada Interativa de Inovação em Saúde")
st.markdown("""
Esta ferramenta (um protótipo para o desafio da **Mastera**) permite explorar dados de saúde pública 
para identificar tendências e oportunidades.
""")

df_completo = carregar_dados()

if df_completo is not None:
    st.sidebar.header("Filtros")
    lista_estados = sorted(df_completo['state'].unique())
    estado_selecionado = st.sidebar.selectbox(
        "Selecione um Estado para Análise:",
        options=lista_estados
    )

    if estado_selecionado:
        # --- SALVA A INTERAÇÃO NO BANCO DE DADOS ---
        # Para evitar salvar a mesma busca repetidamente, usamos o estado da sessão
        if 'last_saved' not in st.session_state or st.session_state.last_saved != estado_selecionado:
            salvar_interacao(engine, estado_selecionado)
            st.session_state.last_saved = estado_selecionado

        st.header(f"Análise de Casos de COVID-19 para: {estado_selecionado}")
        df_estado = filtrar_dados_por_estado(df_completo, estado_selecionado)

        if not df_estado.empty:
            df_grafico = df_estado.set_index('date')
            st.subheader("Evolução do Número de Casos")
            st.line_chart(df_grafico['cases'])
            st.subheader("Evolução do Número de Mortes")
            st.line_chart(df_grafico['deaths'])
            st.subheader("Dados Tabulados")
            st.dataframe(df_estado)
        else:
            st.warning("Nenhum dado encontrado para o estado selecionado.")
else:
    st.error("Não foi possível carregar os dados para iniciar a análise.")