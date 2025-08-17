#Versão final Database
import streamlit as st
import sqlalchemy

#Conexão com banco de dados
@st.cache_resource
def get_connection():

    try:
        connection_string = st.secrets["database"]["connection_string"]
        engine = sqlalchemy.create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Não foi possível conectar ao banco de dados: {e}")
        return None

#Salvar tema de pesquisa
def salvar_jornada(engine, tema):

    if engine is not None and tema:
        try:
            with engine.connect() as conn:
                statement = sqlalchemy.text(
                    "INSERT INTO jornadas_usuario (tema_pesquisado) VALUES (:tema)"
                )
                conn.execute(statement, {"tema": tema})
                conn.commit()
        except Exception as e:
            st.warning(f"Aviso: Não foi possível salvar a interação no banco de dados. Erro: {e}")