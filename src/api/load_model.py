"""
Módulo: load_model.py
Descripción:
    Funciones para cargar pipelines de modelos entrenados de ML.
    Actualmente se incluye la carga del pipeline de LightGBM para 
    inferencia de riesgo de diabetes.
Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# Librerías básicas
import os
import joblib

# Ruta por defecto del modelo desde el script
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "../models/lgbm_diabetes_pipeline.pkl"
)


def load_pipeline(model_path: str = MODEL_PATH):
    """
    Carga el pipeline entrenado de LightGBM para inferencia.

    Args:
        model_path (str): Ruta al archivo .pkl del pipeline entrenado.
                          Por defecto, MODEL_PATH.

    Returns:
        pipeline: Pipeline listo para usar para predicción.

    Raises:
        FileNotFoundError: Si el archivo del modelo no existe.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}")

    pipeline = joblib.load(model_path)
    return pipeline
