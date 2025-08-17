'''Buscar dados da internet e carregar em um DataFrame do pandas'''

import pandas as pd
import streamlit as st

# URL direta para o arquivo CSV de dados de COVID por estado do New York Times
DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

@st.cache_data
def carregar_dados():
    """
    Carrega os dados de COVID-19 do repositório do NYT e os prepara para análise.
    Usa o cache do Streamlit para não precisar baixar os dados a cada interação.
    """
    try:
        # Carrega o CSV diretamente da URL para um DataFrame do pandas
        df = pd.read_csv(DATA_URL)
        
        # Converte a coluna 'date' para o formato de data, essencial para gráficos de tempo
        df['date'] = pd.to_datetime(df['date'])
        
        # Converte o nome do estado para minúsculas para facilitar a busca
        df['state_lower'] = df['state'].str.lower()
        
        return df
    except Exception as e:
        # Em caso de erro (ex: sem internet), mostra uma mensagem de erro no app
        st.error(f"Erro ao carregar os dados: {e}")
        return None

def filtrar_dados_por_estado(df, estado):
    """
    Filtra o DataFrame para retornar apenas os dados de um estado específico.
    """
    if df is not None and estado:
        # Filtra o DataFrame usando o nome do estado em minúsculas
        df_estado = df[df['state_lower'] == estado.lower()]
        return df_estado
    return pd.DataFrame() # Retorna um DataFrame vazio se não houver dados ou estado