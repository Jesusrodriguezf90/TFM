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
from src.api.schemas import DiabetesInput

# Inicialización de la API
app = FastAPI(title="Diabetes Prediction API")

# Habilitar CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el pipeline de ML entrenado
pipeline = load_pipeline()

# Endpoint de predicción
@app.post("/predict")
def predict(input_data: DiabetesInput):
    """
    Recibe datos de entrada validados por Pydantic, ejecuta
    el pipeline de ML y devuelve la predicción.

    Args:
        input_data (DiabetesInput): Datos del paciente.

    Returns:
        dict: Predicción {"prediction": 0 o 1}
    """
    try:
        # Convertir a DataFrame respetando alias de Pydantic
        df = pd.DataFrame([input_data.model_dump(by_alias=True)])

        # Realizar predicción
        prediction = pipeline.predict(df)

        # Devolver predicción como entero
        return {"prediction": int(prediction[0])}

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e)) from e

# Servir frontend estático
app.mount("/web", StaticFiles(directory="web", html=True), name="web")
