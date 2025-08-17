# Desafio de Estágio Mastera

## Descrição do Projeto

Esta aplicação foi desenvolvida como parte do desafio de estágio da empresa Mastera. [cite_start]É uma ferramenta interativa em Streamlit que guia pesquisadores da área da saúde na exploração de oportunidades tecnológicas, conforme solicitado no contexto fictício da empresa "SaúdeJá"[cite: 6]. O usuário insere um tema de pesquisa e a jornada apresenta artigos científicos, estudos genômicos e uma análise de oportunidades de inovação gerada por IA.

**Link para a Aplicação Online:** [https://seu-app.streamlit.app](https://seu-app.streamlit.app) <-- (Coloque o link aqui quando fizer o deploy)

---

## Funcionalidades

* [cite_start]**Jornada Guiada:** O usuário insere um tema de pesquisa que alimenta dinamicamente todas as outras seções de análise[cite: 9, 11].
* **Busca de Artigos Científicos:** Integração com a API da CORE para buscar artigos acadêmicos relevantes, com opção de filtro por idioma.
* **Análise de Estudos Genômicos:** Utiliza o dataset público GWAS Catalog para exibir estudos de associação genômica relacionados ao tema.
* [cite_start]**Análise de Inovação com IA:** Uma aba dedicada utiliza a API do Google Gemini para analisar o tema e sugerir "gaps de mercado" e oportunidades de inovação[cite: 36].
* **Chat Interativo com IA:** O usuário pode conversar com o Gemini para aprofundar a análise de oportunidades.
* [cite_start]**Persistência de Dados:** As buscas do usuário são salvas em um banco de dados PostgreSQL (Supabase) para registrar as interações[cite: 23].

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* [cite_start]**Interface:** Streamlit [cite: 13]
* [cite_start]**Banco de Dados:** PostgreSQL (via Supabase) [cite: 23, 24]
* [cite_start]**Fontes de Dados:** GWAS Catalog [cite: 18][cite_start], CORE API, Google Gemini API[cite: 26].

---

## Setup e Execução Local

Siga os passos abaixo para executar o projeto em sua máquina.

**1. Clone o Repositório:**
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
