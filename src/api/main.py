"""
Notebook: main.py
Objetivo: Exponer el pipeline de ML para detección de diabetes
como una API REST usando FastAPI.

Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# Librerías básicas
import pandas as pd

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Pydantic
from pydantic import ValidationError

# Funciones internas
from src.api.load_model import load_pipeline
from src.api.schemas import (
    DiabetesRequest,
    DiabetesPrediction
)

# Inicialización API
app = FastAPI(title="Diabetes Prediction API")

# Habilitar CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend estático
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# Cargar pipeline entrenado
pipeline = load_pipeline()


# Endpoint de predicción
@app.post("/predict", response_model=DiabetesPrediction)
def predict(request: DiabetesRequest):
    """
    Ejecuta el pipeline de ML y devuelve decisión,
    probabilidad y threshold usado.
    """
    try:
        # Convertir input a DataFrame respetando alias
        df = pd.DataFrame([request.input_data.model_dump(by_alias=True)])

        # Probabilidad clase positiva
        proba = pipeline.predict_proba(df)[0][1]

        # Threshold validado por Pydantic
        threshold = request.config.threshold

        # Decisión final
        decision = (
            "Realizar prueba HbA1c"
            if proba >= threshold
            else "No realizar prueba HbA1c"
        )

        return DiabetesPrediction(
            decision=decision,
            probability=round(proba * 100, 2),  # %
            threshold_used=threshold
        )

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e)) from e
