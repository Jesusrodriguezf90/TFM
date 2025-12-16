# TFM: Modelo de ML para detección de diabetes

## Descripción
Este proyecto tiene como objetivo desarrollar un modelo de Machine Learning para clasificar individuos en:
- Diabetes
- No diabetes

Se utiliza el dataset **BRFSS 2015** del CDC.

El proyecto está diseñado siguiendo principios de **arquitectura modular y reproducible**, alineados con buenas prácticas utilizadas en entornos profesionales de Machine Learning.
Todos los scripts dentro de `src/` deben ejecutarse como módulos (`python -m`) desde la raíz del proyecto para asegurar la correcta resolución de imports absolutos y la reproducibilidad del flujo.

## Estructura del proyecto
TFM/
├─ notebooks/ # Notebooks de análisis exploratorio y pruebas de modelos
│ ├─ data_preprocessing.ipynb
│ ├─ model_training_v1.ipynb
│ ├─ model_training_v2.ipynb
│ └─ transform_xpt_to_csv.ipynb
│
├─ src/ # Código fuente del proyecto (paquete Python)
│ ├─ init.py
│ ├─ preprocessing/
│ │ ├─ init.py
│ │ ├─ data_preprocessing.py
│ │ ├─ preprocessing_pipeline.py
│ │ └─ transform_xpt_to_csv.py
│ │
│ ├─ models/
│ │ ├─ init.py
│ │ ├─ train_model_lgbm.py
│ │ └─ lgbm_diabetes_pipeline.pkl
│ │
│ └─ api/
│ ├─ init.py
│ ├─ main.py
│ ├─ load_model.py
│ └─ schemas.py
│
├─ web/ # Archivos de la aplicación web
│ ├─ index.html
│ ├─ styles.css
│ └─ script.js
│
├─ requirements/ # Dependencias del proyecto
│ ├─ requirements_api.txt
│ └─ requirements_dev.txt
│
├─ README.md # Este archivo
└─ .gitignore # Archivos y carpetas ignorados por Git

## Datos
Los datos originales son grandes y se almacenan externamente (Google Drive).  
Las rutas o enlaces deben ajustarse según el entorno del colaborador.

El archivo final utilizado para el entrenamiento se espera en:

data/cleaned_dataset.csv

## Uso

### 1️. Preparación del entorno
Instalar las dependencias necesarias (ejemplo entorno de desarrollo):

```bash
pip install -r requirements/requirements_dev.txt
```

### 2️. Ejecución de scripts de entrenamiento

Los scripts dentro de `src/` están pensados para ejecutarse **como módulos de Python**, desde la raíz del proyecto (`TFM/`).

Por ejemplo, para entrenar el modelo LightGBM:

```bash
cd path/to/TFM
python -m src.models.train_model_lgbm
```

> **Nota importante:**  
> Todos los scripts dentro de `src/` utilizan **imports absolutos** y deben ejecutarse como módulo con `python -m` desde la raíz del proyecto (`TFM/`).  
> Esto garantiza una arquitectura limpia, escalable y reproducible. **No se deben modificar los scripts para parchear imports.**

El pipeline entrenado se guarda automáticamente en:

src/models/lgbm_diabetes_pipeline.pkl

### 3️. Notebooks
Los notebooks en `notebooks/` se utilizan para:
- Análisis exploratorio
- Pruebas de modelos
- Validación de decisiones de preprocessing y modelado

No constituyen el flujo principal de entrenamiento en producción, sino soporte experimental.

## Contribución

- Cada miembro clona el repositorio y trabaja respetando la estructura de carpetas:

```
src/        # Código fuente y paquetes Python
notebooks/  # Notebooks de análisis y experimentación
data/       # Datos originales y procesados
web/        # Archivos de la interfaz web
```

- Hacer **commits claros y frecuentes** con mensajes descriptivos, por ejemplo:

  - "Añadir script de transformación XPT a CSV"
  - "Refactorizar pipeline de preprocessing"
  - "Actualizar notebook de entrenamiento LightGBM"

- Antes de subir cambios al remoto, hacer **pull** para actualizar la copia local y evitar conflictos.

- Subir cambios solo cuando estén probados y funcionales.

- Revisar los cambios de otros miembros antes de integrarlos.

- Para ejecutar correctamente los scripts dentro de `src/`, utilizar siempre:

```bash
cd path/to/TFM
python -m src.models.train_model_lgbm
```

> **Nota:** El proyecto usa imports absolutos y ejecución como módulo para garantizar una arquitectura limpia y reproducible. La forma correcta de ejecución se documenta y automatiza, no se parchea dentro del código.

## Inferencia / API

Para usar el modelo entrenado en inferencia:

1. Importar la función de carga del modelo:

```python
from src.api.load_model import load_pipeline

pipeline = load_pipeline("src/models/lgbm_diabetes_pipeline.pkl")
```

2. Predecir con nuevos datos (DataFrame `X_new`):

```python
y_pred = pipeline.predict(X_new)
```

3. La API `src/api/main.py` permite exponer el modelo como servicio web si se desea.

## Diagrama de flujo básico

Representación simplificada del pipeline de ML:

```
Raw Data (XPT) ---> Preprocessing (src/preprocessing) ---> Features Limpias
      |
      v
  Notebook EDA
      |
      v
  Pipeline Training (LightGBM)
      |
      v
Pipeline Guardado (src/models/lgbm_diabetes_pipeline.pkl)
      |
      v
Inferencia / API (src/api)
```

## Autor

Jesús Rodríguez  
Rafael Risco  
Cristina Crespo
