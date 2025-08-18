# Desafio de Estágio Mastera

## Descrição do Projeto

Esta aplicação foi desenvolvida como parte do desafio de estágio da empresa Mastera. É uma ferramenta interativa em Streamlit que guia pesquisadores da área da saúde na exploração de oportunidades tecnológicas, conforme solicitado no contexto fictício da empresa "SaúdeJá". O usuário insere um tema de pesquisa e a jornada apresenta artigos científicos, estudos genômicos e uma análise de oportunidades de inovação gerada por IA.

**Link para a Aplicação Online:** [Desafio Mastera](https://desafio-mastera.streamlit.app/)

---

## Funcionalidades

* **Jornada Guiada:** O usuário insere um tema de pesquisa que alimenta dinamicamente todas as outras seções de análise.
* **Busca de Artigos Científicos:** Integração com a API da CORE para buscar artigos acadêmicos relevantes, com opção de filtro por idioma.
* **Análise de Estudos Genômicos:** Utiliza o dataset público GWAS Catalog para exibir estudos de associação genômica relacionados ao tema.
* **Análise de Inovação com IA:** Uma aba dedicada utiliza a API do Google Gemini para analisar o tema e sugerir "gaps de mercado" e oportunidades de inovação.
* **Chat Interativo com IA:** O usuário pode conversar com o Gemini para aprofundar a análise de oportunidades.
* **Persistência de Dados:** As buscas do usuário são salvas em um banco de dados PostgreSQL (Supabase) para registrar as interações.

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface:** Streamlit
* **Banco de Dados:** PostgreSQL (via Supabase)
* **Fontes de Dados:** GWAS Catalog, CORE API, Google Gemini API.

---

## Considerações sobre as APIs

* **Limites de Cota da API do Gemini:** Esta aplicação utiliza a API do Google Gemini no seu plano gratuito ("free-tier") para as funcionalidades de tradução e análise de inovação. Este plano possui um limite de requisições diárias. Caso o limite seja atingido durante os testes, as funcionalidades de IA podem não retornar respostas temporariamente. A arquitetura do código está preparada para lidar com essas falhas sem quebrar a aplicação.
