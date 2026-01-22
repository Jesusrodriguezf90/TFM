"""
Archivo: src/api/schemas.py
Objetivo: Definición de esquemas Pydantic para la
API de predicción de diabetes.
Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# Librerías de validación de datos
from pydantic import BaseModel, Field


class DiabetesInput(BaseModel):
    """
    Esquema Pydantic para la entrada de datos de predicción de diabetes.

    Contiene variables nominales, binarias, ordinales y numéricas
    tal como se encuentran en el dataset BRFSS2015.
    """

    # Variables nominales
    BPHIGH4: int
    # Pydantic v2 no permite campos que empiecen con "_"
    RACE: int = Field(alias="_RACE")

    # Variables binarias
    BPMEDS: int
    BLOODCHO: int
    HAVARTH3: int
    QLACTLM2: int
    USEEQUIP: int
    BLIND: int
    DECIDE: int
    DIFFWALK: int
    DIFFALON: int
    DIFFDRES: int
    SMOKE100: int
    ADDEPEV2: int
    SEX: int

    # Variables ordinales
    GENHLTH: int
    PACAT1: int = Field(alias="_PACAT1")
    AGEG5YR: int = Field(alias="_AGEG5YR")
    BMI5CAT: int = Field(alias="_BMI5CAT")

    # Variables numéricas
    EXEROFT1: float
    FRUTSUM: float = Field(alias="_FRUTSUM")
    VEGESUM: float = Field(alias="_VEGESUM")

    # Configuración del modelo
    model_config = {"populate_by_name": True}  # Permite usar alias al exportar


class InferenceConfig(BaseModel):
    """
    Configuración de inferencia del modelo.

    El threshold define el punto de corte a partir del cual
    una probabilidad predicha se interpreta como 'Diabetes'.
    """

    threshold: float = Field(
        default=0.4733,
        ge=0.0,
        le=1.0,
        description="Umbral de decisión para la probabilidad de diabetes"
    )


class DiabetesRequest(BaseModel):
    """
    Esquema completo de entrada para la predicción.

    Se separan explícitamente:
    - input_data: variables clínicas del paciente
    - config: parámetros de inferencia (threshold)
    """

    input_data: DiabetesInput
    config: InferenceConfig


class DiabetesPrediction(BaseModel):
    """
    Esquema de salida de la API de predicción.
    """

    decision: str
    probability: float
    threshold_used: float
