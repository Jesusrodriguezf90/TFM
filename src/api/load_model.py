import os
import joblib

# Ruta del modelo desde el script
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/lgbm_diabetes_pipeline.pkl')

def load_pipeline(model_path: str = MODEL_PATH):
    # El pipeline entrenado de LightGBM para inferencia. Devuelve: pipeline listo para usar.
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}")
    
    pipeline = joblib.load(model_path)
    return pipeline