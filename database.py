# database.py
import streamlit as st
import sqlalchemy

@st.cache_resource
def get_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    try:
        connection_string = st.secrets["database"]["connection_string"]
        
        # A MUDANÇA ESTÁ AQUI: Adicionamos o connect_args para forçar a codificação UTF-8
        engine = sqlalchemy.create_engine(
            connection_string,
            connect_args={"client_encoding": "utf8"}
        )
        
        return engine
    except Exception as e:
        st.error(f"Não foi possível conectar ao banco de dados: {e}")
        return None

# A função salvar_interacao continua a mesma
def salvar_interacao(engine, tema):
    """Salva o tema buscado pelo usuário na tabela 'interacoes'."""
    if engine is not None and tema:
        try:
            with engine.connect() as conn:
                statement = sqlalchemy.text("INSERT INTO interacoes (tema_buscado) VALUES (:tema)")
                conn.execute(statement, {"tema": tema})
                conn.commit()
        except Exception as e:
            st.warning(f"Aviso: Não foi possível salvar a interação no banco de dados. Erro: {e}")