import os
import requests
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="SoulMove | Inteligência Artificial",
    page_icon="🌱",
    layout="wide"
)


st.markdown("""
    <style>
        /* Cores da Marca */
        :root {
            --soul-escuro: #231F0E;
            --soul-azul: #2563EB;
            --soul-azul-claro: #DBEAFE;
        }

        /* Títulos principais com o tom escuro */
        h1, h2, h3 {
            color: var(--soul-escuro) !important;
        }

        /* Seletor específico para o botão de envio do formulário */
        [data-testid="stFormSubmitButton"] button {
            background-color: var(--soul-azul) !important;
            color: white !important;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            width: 100%;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            background-color: #1d4ed8 !important;
            color: white !important;
        }

        /* Caixa de informações da sidebar */
        [data-testid="stSidebar"] [data-testid="stInfo"] {
            background-color: var(--soul-azul-claro) !important;
            color: var(--soul-escuro) !important;
            border-left: 5px solid var(--soul-azul);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar de navegação e informações
with st.sidebar:
    st.title("SoulMove AI")
    st.markdown("Plataforma inteligente de incentivo à sustentabilidade urbana.")
    st.divider()
    st.info(
        "**Sprint 4 - FIAP**\n\n"
        "Modelos integrados:\n"
        "- **Random Forest** (Regressão)\n"
        "- **XGBoost** (Classificação)"
    )

# Abas principais
aba_simulador, aba_sobre = st.tabs(["🔮 Simulador de Impacto", "📚 Sobre o Projeto"])

with aba_simulador:
    st.title("Simulador de Atividades Sustentáveis")
    st.write(
        "Preencha os dados da atividade do utilizador para estimar a pontuação "
        "gerada e o nível de impacto ecológico em tempo real."
    )

    with st.form("form_atividade"):
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            tipo = st.selectbox(
                "Tipo de atividade",
                [
                    "BICICLETA",
                    "CAMINHADA",
                    "ECONOMIA_ENERGIA",
                    "RECICLAGEM",
                    "TRANSPORTE_PUBLICO"
                ]
            )
        with col_f2:
            comprovante = st.selectbox(
                "Tipo de comprovante",
                ["FOTO", "GPS", "MANUAL"]
            )
        with col_f3:
            bairro = st.selectbox(
                "Bairro",
                [
                    "BELA VISTA", "CAMPO BELO", "ITAIM BIBI", "MOEMA",
                    "MOOCA", "PERDIZES", "PINHEIROS", "SANTANA", "TATUAPE", "VILA MARIANA"
                ]
            )

        st.divider()
        st.write("### Métricas Específicas da Atividade")

        # Inicializamos variáveis
        duracao = 0.0
        distancia = 0.0
        quantidade = 0.0
        energia = 0.0
        co2 = 0.0

        # Renderização dinâmica baseada no contexto da atividade
        if tipo in ["BICICLETA", "CAMINHADA", "TRANSPORTE_PUBLICO"]:
            col1, col2 = st.columns(2)
            with col1:
                duracao = st.number_input("Duração (minutos)", min_value=0.0, value=00.0)
                distancia = st.number_input("Distância (km)", min_value=0.0, value=0.0)
            with col2:
                co2 = st.number_input("CO₂ evitado estimado (kg)", min_value=0.0, value=0.0)

        elif tipo == "RECICLAGEM":
            col1, col2 = st.columns(2)
            with col1:
                quantidade = st.number_input("Material reciclado (kg)", min_value=0.0, value=0.0)
            with col2:
                co2 = st.number_input("CO₂ evitado estimado (kg)", min_value=0.0, value=0.0)

        elif tipo == "ECONOMIA_ENERGIA":
            col1, col2 = st.columns(2)
            with col1:
                energia = st.number_input("Energia economizada (kWh)", min_value=0.0, value=0.0)
            with col2:
                co2 = st.number_input("CO₂ evitado estimado (kg)", min_value=0.0, value=0.0)

        enviar = st.form_submit_button("🚀 Analisar com Inteligência Artificial")

    if enviar:
        dados = {
            "tipo_atividade": tipo,
            "comprovante_tipo": comprovante,
            "bairro": bairro,
            "duracao_minutos": duracao,
            "distancia_km": distancia,
            "quantidade_kg": quantidade,
            "kwh_economizados": energia,
            "co2_evitado_kg": co2
        }

        try:
            with st.spinner("Conectando à API e consultando os modelos preditivos..."):
                r_reg = requests.post(f"{API_URL}/predict/regressao", json=dados, timeout=30)
                r_reg.raise_for_status()
                res_reg = r_reg.json()

                r_class = requests.post(f"{API_URL}/predict/classificacao", json=dados, timeout=30)
                r_class.raise_for_status()
                res_class = r_class.json()

            st.success("Análise concluída com sucesso!")

            st.divider()
            col_m1, col_m2 = st.columns(2)

            pontos = res_reg["pontos_previstos"]
            classificacao = res_class["classificacao"]

            col_m1.metric(
                label="⭐ Pontos Estimados (Random Forest)",
                value=f"{pontos} pts"
            )

            if classificacao == "ALTO":
                col_m2.metric(
                    label="🌱 Nível de Impacto (XGBoost)",
                    value="ALTO IMPACTO",
                    delta="Destaque Sustentável"
                )
            else:
                col_m2.metric(
                    label="🌱 Nível de Impacto (XGBoost)",
                    value="IMPACTO NORMAL",
                    delta_color="off"
                )

            with st.expander("🔍 Ver detalhes técnicos da resposta da API (JSON)"):
                st.json({
                    "regressao": res_reg,
                    "classificacao": res_class,
                    "payload_enviado": dados
                })

            st.caption(
                "⚠️ **Aviso Acadêmico:** Resultados gerados por modelos de Machine Learning "
                "alimentados por dados sintéticos (Prova de Conceito - FIAP)."
            )

        except requests.RequestException as e:
            st.error(
                f"Erro de comunicação com a API: {e}. "
                "Certifique-se de que o servidor Uvicorn está ativo em http://127.0.0.1:8000"
            )

with aba_sobre:
    st.header("Sobre a Arquitetura de Machine Learning")
    st.write(
        "Este painel faz parte da entrega da Sprint 4. A solução desacopla "
        "a inteligência analítica em três camadas principais:"
    )

    st.markdown("""
    1. **Camada de Treinamento (Google Colab):** EDA, engenharia de atributos, treino de modelos com Scikit-Learn e XGBoost, e salvamento via serialização otimizada.
    2. **Camada de Serviço (FastAPI):** Backend em alta performance que expõe rotas REST para validação e inferência rápida dos modelos.
    3. **Camada de Apresentação (Streamlit):** Interface web interativa voltada para a experiência do utilizador, aplicando formulários dinâmicos e prevenção de erros.
    """)