# 🌱 SoulMove | Inteligência Artificial & Sustentabilidade

> Plataforma inteligente desenvolvida para a **Sprint 4 da FIAP** (Análise e Desenvolvimento de Sistemas), focada no incentivo à mobilidade urbana sustentável e ações ecológicas através de Machine Learning.

---

## 🏗️ Arquitetura do Sistema

O projeto adota uma arquitetura **desacoplada e orientada a serviços**, dividida em três camadas principais:

1. **Camada de Modelagem & ML (`/notebooks`):** EDA, engenharia de atributos, tratamento de dados e treino dos modelos preditivos em Jupyter Notebook.
2. **Camada de Serviço / Backend (`/api`):** API de alta performance construída com **FastAPI**, responsável por validar dados de entrada via Pydantic e servir inferências em tempo real.
3. **Camada de Apresentação / Frontend (`/interface`):** Painel interativo construído em **Streamlit**, aplicando heurísticas de usabilidade (formulários dinâmicos) e visualizações analíticas modernas via **Plotly**.

---

## 🤖 Modelos de Machine Learning Integrados

* **Regressão (`RandomForestRegressor`):** Serializado via `joblib`, calcula e estima a pontuação exata gerada pela atividade sustentável do utilizador.
* **Classificação (`XGBoost Classifier`):** Salvo em formato nativo `.json` (evitando corrupção de fluxo), categoriza o nível de impacto ecológico (`ALTO` ou `NORMAL`).

---

## 🎨 Identidade Visual & UI/UX

A interface reflete a identidade da marca SoulMove através de uma paleta de cores personalizada via CSS injetado:
* **Tom Escuro (`#231F0E`):** Tipografia de destaque e títulos.
* **Azul Corporativo (`#2563EB`):** Botões de ação e elementos principais.
* **Azul Claro (`#DBEAFE`):** Blocos informativos e caixas de destaque.

---

## 🚀 Acesso ao Projeto em Produção

* **Aplicação Web (Frontend - Streamlit):** [🔗 Aceder ao SoulMove]((https://soulmovelm-view.streamlit.app/))
* **Documentação da API (Backend - FastAPI/Swagger):** [🔗 Ver Swagger Docs]((https://soulmovelm-api.onrender.com/docs#/))
---

## 📂 Estrutura do Projeto

```text
soulMoveLM/
├── api/
│   └── main.py                          # Endpoints FastAPI e regras de inferência
├── interface/
│   └── app.py                           # Painel interativo e dinâmico em Streamlit
├── models/
│   ├── classificacao_columns.json       # Schema de colunas da classificação
│   ├── modelo_classificacao.json        # Modelo XGBoost em formato nativo JSON
│   ├── modelo_classificacao_api.joblib  # Modelo de classificação serializado
│   └── modelo_regressao_api.joblib      # Modelo Random Forest de regressão
├── notebooks/
│   └── SoulMoveModel.ipynb              # Notebook de treino e análise de dados
├── pyproject.toml                       # Configuração do projeto e dependências
├── requirements.txt                     # Dependências legadas / universais
└── uv.lock                              # Lockfile de gestão de pacotes uv


