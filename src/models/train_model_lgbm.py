from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from lightgbm import LGBMClassifier

from src.preprocessing.preprocessing_pipeline import (
    boosting_deterministic_preproc,
    cap_outliers_numeric,
    categorical_nominal,
    categorical_ordinal,
    binary_vars,
    numeric_vars
)

# Se construye el pipeline completo de preprocessing + modelo LightGBM
def build_lightgbm_pipeline():

    nominal_pipeline_boosting = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent'))
    ])

    ordinal_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent'))
    ])

    numeric_pipeline = Pipeline(steps=[
        ('cap_outliers', FunctionTransformer(
            func=cap_outliers_numeric,
            kw_args={'numeric_vars': numeric_vars},
            validate=False
        )),
        ('imputer', SimpleImputer(strategy='median'))
    ])

    preprocessor_boosting = ColumnTransformer(transformers=[
        ('nom', nominal_pipeline_boosting, categorical_nominal),
        ('bin', 'passthrough', binary_vars),
        ('ord', ordinal_transformer, categorical_ordinal),
        ('num', numeric_pipeline, numeric_vars)
    ])

    lgb_model = LGBMClassifier(
        n_estimators=200,
        max_depth=-1,
        num_leaves=31,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        class_weight='balanced',
        n_jobs=-1,
        random_state=42
    )

    pipeline = Pipeline([
        ('deterministic', FunctionTransformer(boosting_deterministic_preproc)),
        ('preprocessor', preprocessor_boosting),
        ('model', lgb_model)
    ])

    return pipeline

if __name__ == "__main__": # Para que se ejecute
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from pathlib import Path

    # Se cargan los datos
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    DATA_PATH = PROJECT_ROOT / "data" / "cleaned_dataset.csv"
    MODELS_DIR = PROJECT_ROOT / "src" / "models"
    MODELS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH, encoding="Latin-1")

    # Se prepara el target
    df['DIABETE3'] = df['DIABETE3'].map({1.0: 1, 3.0: 0})
    X = df.drop("DIABETE3", axis=1)
    y = df["DIABETE3"]

    # Separación del dataset
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    # Se entrena el pipeline
    pipeline = build_lightgbm_pipeline()
    pipeline.fit(X_train, y_train)

    # Se guarda el pipeline
    model_path = MODELS_DIR / "lgbm_diabetes_pipeline.pkl"
    joblib.dump(pipeline, model_path)

    print(f"Pipeline guardado correctamente en: {model_path}")