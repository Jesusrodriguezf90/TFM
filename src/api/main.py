from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import ValidationError

from src.api.load_model import load_pipeline
from src.api.schemas import DiabetesInput

# Se crea app FastAPI
app = FastAPI(title="Diabetes Prediction API")

# Se habilita CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Dirección de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, OPTIONS...
    allow_headers=["*"],  # Permite Content-Type, Authorization, etc.
)

# Se carga el pipeline del modelo
pipeline = load_pipeline()

@app.get("/")
def root():
    return {"message": "API de predicción de diabetes funcionando"}

@app.post("/predict")
def predict(input_data: DiabetesInput):
    try:
        # Se covierte el input a DataFrame respetando alias de Pydantic
        df = pd.DataFrame([input_data.model_dump(by_alias=True)])

        # Se realiza predicción
        prediction = pipeline.predict(df)

        return {"prediction": int(prediction[0])}

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Se imprime el error real en consola para debugging
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))