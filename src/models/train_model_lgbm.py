"""
Script: train_model_lgbm.py
Objetivo: Construcción, entrenamiento y persistencia de un pipeline
completo de preprocessing + modelo LightGBM para detección de diabetes.

El pipeline incluye:
- Preprocesamiento determinista
- Imputación y tratamiento por tipo de variable
- Entrenamiento de modelo LightGBM balanceado

Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# pylint: disable=C0103
# Las variables de entrenamiento/validación/test usan nombres
# clásicos de ML: X_train, y_train, X_val, y_test, etc.

# Librerías básicas
from pathlib import Path
import pandas as pd
import joblib

# Scikit-learn
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split

# Modelos externos
from lightgbm import LGBMClassifier

# Funciones de preprocesamiento y listas de variables
from src.preprocessing.preprocessing_pipeline import (
    boosting_deterministic_preproc,
    cap_outliers_numeric,
    CATEGORICAL_NOMINAL,
    CATEGORICAL_ORDINAL,
    BINARY_VARS,
    NUMERIC_VARS,
)
def build_lightgbm_pipeline() -> Pipeline:
    """
    Construye un pipeline completo de preprocesamiento y modelo LightGBM.

    - Pipeline determinista previo
    - ColumnTransformer por tipo de variable
    - Modelo LightGBM balanceado
    """

    # Pipelines para cada tipo de variable
    nominal_pipeline_boosting = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent"))]
    )

    ordinal_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent"))]
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "cap_outliers",
                FunctionTransformer(
                    func=cap_outliers_numeric,
                    kw_args={"numeric_vars": NUMERIC_VARS},
                    validate=False,
                ),
            ),
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    # ColumnTransformer final
    preprocessor_boosting = ColumnTransformer(
        transformers=[
            ("nom", nominal_pipeline_boosting, CATEGORICAL_NOMINAL),
            ("bin", "passthrough", BINARY_VARS),
            ("ord", ordinal_transformer, CATEGORICAL_ORDINAL),
            ("num", numeric_pipeline, NUMERIC_VARS),
        ]
    )

    lgb_model = LGBMClassifier(
        n_estimators=200,
        max_depth=-1,
        num_leaves=31,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42,
    )

    # Pipeline final
    final_pipeline = Pipeline(
        [
            ("deterministic", FunctionTransformer(boosting_deterministic_preproc)),
            ("preprocessor", preprocessor_boosting),
            ("model", lgb_model),
        ]
    )

    return final_pipeline

if __name__ == "__main__":
    # Rutas de proyecto y modelos
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DATA_PATH = PROJECT_ROOT / "data" / "cleaned_dataset.csv"
    MODELS_DIR = PROJECT_ROOT / "src" / "models"
    MODELS_DIR.mkdir(exist_ok=True)

    # Cargar datos
    df = pd.read_csv(DATA_PATH, encoding="Latin-1")

    # Preparción del target
    df["DIABETE3"] = df["DIABETE3"].map({1.0: 1, 3.0: 0})
    X = df.drop("DIABETE3", axis=1)
    y = df["DIABETE3"]

    # Separación del dataset
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    # Entrenamiento del pipeline
    model_pipeline = build_lightgbm_pipeline()
    model_pipeline.fit(X_train, y_train)

    # Guardado del pipeline
    model_path = MODELS_DIR / "lgbm_diabetes_pipeline.pkl"
    joblib.dump(model_pipeline, model_path)

    print(f"Pipeline guardado correctamente en: {model_path}")
