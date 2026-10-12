from pathlib import Path
import json
import joblib
import pandas as pd
import xgboost as xgb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="SoulMove API",
    description="API de Machine Learning para sustentabilidade",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = BASE_DIR / "models"

# 1. Carregar Modelo de Regressão (Random Forest via joblib)
regressao_path = MODELOS_DIR / "modelo_regressao_api.joblib"
regressao_dict = joblib.load(regressao_path)
modelo_reg = regressao_dict["model"]
colunas_reg = regressao_dict["feature_columns"]

# 2. Carregar Modelo de Classificação (XGBoost via .json nativo)
modelo_class = xgb.XGBClassifier()
modelo_class.load_model(MODELOS_DIR / "modelo_classificacao.json")

with open(MODELOS_DIR / "classificacao_columns.json", "r") as f:
    colunas_class = json.load(f)


class DadosAtividade(BaseModel):
    tipo_atividade: str
    comprovante_tipo: str
    bairro: str
    duracao_minutos: float = Field(ge=0)
    distancia_km: float = Field(ge=0)
    quantidade_kg: float = Field(ge=0)
    kwh_economizados: float = Field(ge=0)
    co2_evitado_kg: float = Field(ge=0)


def preparar_entrada(dados, colunas):
    df = pd.DataFrame([dados.model_dump()])
    df = pd.get_dummies(
        df,
        columns=["tipo_atividade", "comprovante_tipo", "bairro"],
        drop_first=True,
        dtype=int
    )
    return df.reindex(columns=colunas, fill_value=0)


@app.get("/")
def inicio():
    return {"mensagem": "SoulMove API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict/regressao")
def prever_pontos(dados: DadosAtividade):
    try:
        entrada = preparar_entrada(dados, colunas_reg)
        previsao = modelo_reg.predict(entrada)[0]
        return {
            "modelo": "Random Forest Regressor",
            "pontos_previstos": round(float(previsao), 2)
        }
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar previsão: {str(erro)}"
        ) from erro


@app.post("/predict/classificacao")
def classificar_impacto(dados: DadosAtividade):
    try:
        entrada = preparar_entrada(dados, colunas_class)
        previsao = int(modelo_class.predict(entrada)[0])
        return {
            "modelo": "XGBoost Classifier",
            "impacto_alto": previsao,
            "classificacao": "ALTO" if previsao == 1 else "NAO_ALTO"
        }
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao classificar impacto: {str(erro)}"
        ) from erro