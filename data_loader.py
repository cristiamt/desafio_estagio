#Versão final do Data loader
import pandas as pd
import streamlit as st
import requests
import google.generativeai as genai
from urllib.parse import quote_plus

# --- FONTE DE DADOS GWAS Catalog ---
GWAS_URL = "https://www.ebi.ac.uk/gwas/api/search/downloads/studies_alternative"

#Carregar dados GWAS
@st.cache_data
def carregar_dados_gwas():

    try:
        df = pd.read_csv(GWAS_URL, sep='\t')
        return df
    except Exception as e:
        print(f"Erro ao carregar o dataset GWAS: {e}")
        return None


def filtrar_gwas_por_tema(df, query): #Filtro do df

    if df is not None and query:
        resultados = df[
            df['DISEASE/TRAIT'].str.contains(query, case=False, na=False)
        ]
        return resultados
    return pd.DataFrame()

#Buscado no API da CORE
def buscar_artigos_core(query, idioma='Inglês', max_results=10):

    base_url = "https://api.core.ac.uk/v3/search/works"
    query_formatada = f'"{query}"'
    if idioma == "Português":
        query_formatada += ' AND language.name:"Portuguese"'
    else:
        query_formatada += ' AND language.name:"English"'
    params = {"q": query_formatada, "limit": max_results}
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        artigos = []
        for resultado in data.get('results', []):
            titulo = resultado.get('title', 'Título não disponível')
            resumo = resultado.get('abstract', 'Resumo não disponível.')
            link_final = None
            if download_urls := resultado.get('downloadUrls', []):
                pdf_links = [dl.get('url') for dl in download_urls if dl.get('type') == 'pdf' and dl.get('url')]
                if pdf_links:
                    link_final = pdf_links[0]
            if not link_final:
                if core_id := resultado.get('id'):
                    link_final = f"https://core.ac.uk/display/{core_id}"
            if not link_final:
                titulo_encoded = quote_plus(titulo)
                link_final = f"https://scholar.google.com/scholar?q={titulo_encoded}"
            lista_de_autores = resultado.get('authors', [])
            if lista_de_autores:
                autores = ", ".join([autor['name'] for autor in lista_de_autores if 'name' in autor])
            else:
                autores = "Autores não listados"
            artigos.append({'titulo': titulo, 'autores': autores, 'resumo': resumo, 'link': link_final})
        return artigos
    except Exception as e:
        print(f"Erro ao buscar na API da CORE: {e}")
        return []

#API Gemini
def resumir_com_ia(texto_para_resumir):

    try:
        api_key = st.secrets["google"]["api_key"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Você é um assistente de pesquisa que resume textos acadêmicos em português de forma clara e concisa em até 3 frases. Resuma o seguinte texto: {texto_para_resumir}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Não foi possível gerar o resumo. Verifique a configuração da chave da API do Google."

#Tradutor
def traduzir_texto_para_ingles(texto):

    if not texto: return ""
    try:
        api_key = st.secrets["google"]["api_key"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Traduza o seguinte termo de pesquisa do português para o inglês. Retorne apenas o termo traduzido, sem nenhuma outra palavra ou explicação. Termo: {texto}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini para tradução: {e}")
        return texto

#Gaps de mercado
def buscar_gaps_de_mercado_com_ia(tema):

    try:
        api_key = st.secrets["google"]["api_key"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        Aja como um consultor de inovação na área da saúde.
        Com base no tema de pesquisa '{tema}', analise o cenário atual e identifique 3 a 5 'gaps de mercado' ou oportunidades de inovação.
        Para cada oportunidade, descreva:
        1. A oportunidade em si.
        2. Por que é relevante (qual problema resolve).
        3. Possíveis tipos de soluções (ex: novo dispositivo, software, protocolo clínico, tipo de medicamento).
        Formate a resposta em Tópicos (bullet points) para clareza.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini para Gaps de Mercado: {e}")
        return "Não foi possível gerar as sugestões de inovação. Verifique a configuração da chave da API do Google."


# Chat linkada com Gemini
def chamar_chat_gemini(historico_conversa):

    try:
        api_key = st.secrets["google"]["api_key"]
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        mensagens_para_api = [
            {'role': msg['role'], 'parts': msg['parts']}
            for msg in historico_conversa
        ]

        chat = model.start_chat(history=mensagens_para_api[:-1])  # Envia todo o histórico, exceto a última pergunta

        ultima_pergunta = mensagens_para_api[-1]['parts'][0]  # A última pergunta do usuário

        response = chat.send_message(ultima_pergunta)
        return response.text

    except Exception as e:
        print(f"Erro ao chamar a API do Gemini no modo chat: {e}")
        return "Ocorreu um erro ao processar sua pergunta. Por favor, tente novamente."