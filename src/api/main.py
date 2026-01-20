from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
from pydantic import ValidationError

from src.api.load_model import load_pipeline
from src.api.schemas import DiabetesInput

# Se crea la aplicación FastAPI
app = FastAPI(title="Diabetes Prediction API")

# Se habilita CORS para permitir peticiones desde el navegador (necesario para que el frontend pueda comunicarse con la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Se permiten peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],              # Se permiten métodos GET, POST, OPTIONS...
    allow_headers=["*"],              # Se permiten todas las cabeceras
)

# Se carga el pipeline de Machine Learning previamente entrenado
pipeline = load_pipeline()

@app.post("/predict")
def predict(input_data: DiabetesInput):
    # Endpoint de predicción. Recibe los datos de entrada validados por Pydantic, ejecuta el modelo y devuelve la predicción en formato JSON.
    try:
        # Se convierten los datos de entrada en un DataFrame de pandas respetando los alias definidos en el esquema Pydantic
        df = pd.DataFrame([input_data.model_dump(by_alias=True)])

        # Se realiza la predicción utilizando el pipeline cargado
        prediction = pipeline.predict(df)

        # Se devuelve la predicción como entero (0 = No diabetes, 1 = Diabetes)
        return {"prediction": int(prediction[0])}

    except ValidationError as ve:
        # Se captura cualquier error de validación de datos
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Se imprime el error real por consola para facilitar el debugging
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

# Se sirve el frontend estático (HTML, CSS y JavaScript) desde la ruta /web para evitar conflictos con los endpoints de la API
app.mount("/web", StaticFiles(directory="web", html=True), name="web")