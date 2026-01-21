"""
Script: preprocessing_pipeline.py
Objetivo: Definir las variables y funciones de preprocesamiento
determinista utilizadas en el pipeline de Machine Learning basado
en LightGBM.

Incluye transformaciones para:
- Normalización de variables binarias.
- Conversión de variables categóricas nominales.
- Tratamiento de valores faltantes codificados como -1.
- Limitación de valores extremos en variables numéricas.

Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# pylint: disable=C0103
# Se desactiva la comprobación de nombres de variables para
# permitir el uso de convenciones estándar en Machine Learning:
# X, X_input

# Librerías básicas
import numpy as np
import pandas as pd

# Variables categóricas nominales
CATEGORICAL_NOMINAL = ["BPHIGH4", "_RACE"]

# Variables binarias
BINARY_VARS = [
    "BPMEDS",
    "BLOODCHO",
    "HAVARTH3",
    "QLACTLM2",
    "USEEQUIP",
    "BLIND",
    "DECIDE",
    "DIFFWALK",
    "DIFFALON",
    "DIFFDRES",
    "SMOKE100",
    "ADDEPEV2",
    "SEX",
]

# Variables categóricas ordinales
CATEGORICAL_ORDINAL = ["GENHLTH", "_PACAT1", "_AGEG5YR", "_BMI5CAT"]

# Variables numéricas
NUMERIC_VARS = ["EXEROFT1", "_FRUTSUM", "_VEGESUM"]


def boosting_deterministic_preproc(X_input: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformaciones deterministas previas al pipeline de boosting.

    - Reemplaza valores -1 por NaN
    - Convierte variables binarias a 0/1
    - Fuerza tipo categórico en variables nominales
    """
    X = X_input.copy()


    # Reemplazo global de valores -1 por NaN
    X = X.replace(-1, np.nan)

    # Normalización de variables binarias
    for col in BINARY_VARS:
        X[col] = (X[col] == 1).astype(int)

    # Conversión de variables nominales a categóricas
    for col in CATEGORICAL_NOMINAL:
        X[col] = X[col].astype("category")

    return X


def cap_outliers_numeric(X_input, numeric_vars):
    """
    Recorta valores extremos de variables numéricas al percentil 1 y 99.

    Args:
        X_input (pd.DataFrame): Dataset de entrada.
        numeric_vars (list): Lista de columnas numéricas a recortar.

    Returns:
        pd.DataFrame: Dataset con valores acotados.
    """
    X = X_input.copy()

    for col in numeric_vars:
        low = np.nanpercentile(X[col], 1)
        high = np.nanpercentile(X[col], 99)
        X[col] = X[col].clip(low, high)

    return X
