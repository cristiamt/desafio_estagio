#APP.PY VERSÃO FINAL!
import streamlit as st
import pandas as pd
from data_loader import buscar_artigos_core, carregar_dados_gwas, filtrar_gwas_por_tema, resumir_com_ia, \
    traduzir_texto_para_ingles, buscar_gaps_de_mercado_com_ia, chamar_chat_gemini
from database import get_connection, salvar_jornada

# --- Configuração da Página ---
st.set_page_config(
    page_title="Jornada de Inovação em Saúde",
    page_icon="💡",
    layout="wide"
)

# --- Conexão com o Banco de Dados ---
engine = get_connection()

# --- Título Principal ---
st.title("💡 Jornada Interativa de Desenvolvimento e Inovação")
st.markdown("Guiando pesquisadores na exploração de oportunidades tecnológicas.")
st.markdown("---")

# Inicializa o 'session_state'
if 'resultados' not in st.session_state:
    st.session_state.resultados = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Carrega o dataset GWAS
df_gwas_completo = carregar_dados_gwas()

# --- Barra Lateral com Filtros ---
with st.sidebar:
    st.header("Inicie sua Jornada")

    with st.form("form_busca_sidebar"):
        tema_input = st.text_input("Escreva o tema tema de pesquisa",
                                   placeholder="Ex: Câncer, Diabetes, Alzheimer")
        idioma_artigos = st.radio("Idioma para a busca de artigos:", ("Inglês", "Português"), index=0)
        num_resultados = st.slider("Número máximo de resultados:", min_value=5, max_value=25, value=10, step=5)

        submitted = st.form_submit_button("🔎 Iniciar / Atualizar Jornada")

        if submitted:
            if tema_input:
                salvar_jornada(engine, tema_input)
                # Limpa o histórico do chat anterior ao iniciar uma nova jornada
                st.session_state.messages = []

                with st.spinner("Preparando a busca..."):
                    termo_busca_principal = tema_input
                    if idioma_artigos == 'Inglês':
                        termo_busca_principal = traduzir_texto_para_ingles(tema_input)

                with st.spinner("Buscando em todas as fontes..."):
                    st.session_state.resultados = {
                        "tema_original": tema_input,
                        "tema_traduzido": termo_busca_principal,
                        "artigos": buscar_artigos_core(termo_busca_principal, idioma_artigos, num_resultados),
                    }
                st.success("Busca concluída! Por favor navegue pelas abas para ver os resultados.")
            else:
                st.error("Por favor, preencha o tema da pesquisa.")

# --- Abas de Resultados ---
if st.session_state.resultados:
    st.header(f"Resultados para: {st.session_state.resultados['tema_original']}")

    tab_artigos, tab_estudos_genomicos, tab_oportunidades = st.tabs(
        ["🔬 Artigos Científicos", "🧬 Estudos Genômicos", "💡 Oportunidades de Inovação"])

    with tab_artigos:
        st.caption(
            "Nota: A busca é feita no repositório CORE, que é um agregador. Alguns artigos podem não estar mais disponíveis na fonte original ou os links podem estar quebrados.")
        artigos = st.session_state.resultados["artigos"]
        if artigos:
            for i, artigo in enumerate(artigos):
                with st.expander(f"📄 {artigo['titulo']}"):
                    st.caption(f"Autores: {artigo['autores']}")
                    st.markdown(f"[Acessar Artigo]({artigo['link']})")
                    if st.button("Resumir com IA", key=f"resumo_{i}"):
                        if artigo['resumo'] and artigo['resumo'] != 'Resumo não disponível.':
                            st.info(resumir_com_ia(artigo['resumo']))
                        else:
                            st.warning("Não há resumo disponível para este artigo.")
        else:
            st.info("Nenhum artigo encontrado para os filtros selecionados.")

    with tab_estudos_genomicos:
        st.subheader(f"Estudos Genômicos Relacionados a: {st.session_state.resultados['tema_original']}")
        st.caption("Fonte: NHGRI-EBI GWAS Catalog")
        st.write(
            "Estudos de associação genômica ampla (GWAS) ajudam a identificar genes associados a doenças, apontando alvos para novos medicamentos e terapias.")
        st.markdown("---")

        if df_gwas_completo is not None:
            resultados_gwas = filtrar_gwas_por_tema(df_gwas_completo, st.session_state.resultados['tema_traduzido'])
            if not resultados_gwas.empty:
                st.success(f"Encontrados {len(resultados_gwas)} estudos genômicos:")
                for index, row in resultados_gwas.head(st.session_state.get('num_resultados', 10)).iterrows():
                    link_estudo = f"https://www.ebi.ac.uk/gwas/studies/{row['STUDY ACCESSION']}"
                    st.markdown(f"**Doença/Característica:** {row['DISEASE/TRAIT']}")
                    st.markdown(f"**Autor Principal:** {row['FIRST AUTHOR']} et al.")
                    st.markdown(f"**Publicado em:** {row['JOURNAL']} ({row['DATE']})")
                    st.markdown(f"**[Ver detalhes do estudo ({row['STUDY ACCESSION']})]({link_estudo})**")
                    st.markdown("---")
            else:
                st.info("Nenhum estudo genômico encontrado para este tema no dataset.")
        else:
            st.error("Não foi possível carregar o dataset de estudos genômicos.")

    with tab_oportunidades:
        st.subheader(f"Converse com a IA sobre Oportunidades em '{st.session_state.resultados['tema_original']}'")

        if not st.session_state.messages:
            with st.spinner("IA está analisando o cenário para iniciar a conversa..."):
                tema_para_analise = st.session_state.resultados['tema_traduzido']
                analise_inicial = buscar_gaps_de_mercado_com_ia(tema_para_analise)
                st.session_state.messages.append({"role": "model", "parts": [analise_inicial]})

        for message in st.session_state.messages:
            role = "user" if message['role'] == 'user' else "assistant"
            with st.chat_message(role):
                st.markdown(message['parts'][0])

        if prompt := st.chat_input("Faça uma pergunta sobre as oportunidades listadas..."):
            st.session_state.messages.append({"role": "user", "parts": [prompt]})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = chamar_chat_gemini(st.session_state.messages)
                    st.markdown(response)

            st.session_state.messages.append({"role": "model", "parts": [response]})

else:
    st.info("⬅️ Preencha os filtros na barra lateral e inicie sua jornada para ver os resultados.")