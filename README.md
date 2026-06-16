---
title: Detección de Riesgo de Diabetes
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.17.3
app_file: app.py
pinned: false
license: mit
short_description: Modelo de ML para detección de diabetes
---

# TFM: Modelo de ML para detección de diabetes

## Descripción
Este proyecto tiene como objetivo desarrollar un modelo de Machine Learning para clasificar individuos en:
- Diabetes
- No diabetes

Se utiliza el dataset **BRFSS 2015** del CDC.

El proyecto está diseñado siguiendo principios de **arquitectura modular y reproducible**, alineados con buenas prácticas utilizadas en entornos profesionales de Machine Learning.
Todos los scripts dentro de `src/` deben ejecutarse como módulos (`python -m`) desde la raíz del proyecto para asegurar la correcta resolución de imports absolutos y la reproducibilidad del flujo.

## Estructura del proyecto

```
TFM/
├─ notebooks/ # Notebooks de análisis exploratorio y pruebas de modelos
│ ├─ data_preprocessing.ipynb
│ ├─ data_preprocessing_spark.ipynb
│ ├─ model_advanced_v1.ipynb
│ ├─ model_advanced_mlp_v1
│ ├─ model_base_v1.ipynb
│ ├─ model_base_v2.ipynb
│ └─ transform_xpt_to_csv.ipynb
│
├─ src/          # Código fuente del proyecto (paquete Python)
│   ├─ __init__.py
│   ├─ preprocessing/
│   │        ├─ __init__.py
│   │        ├─ data_preprocessing.py
│   │        ├─ preprocessing_pipeline.py
│   │        └─ transform_xpt_to_csv.py
│   │
│   ├─ models/
│   │        ├─ __init__.py
│   │        ├─ train_model_lgbm.py
│   │        └─ lgbm_diabetes_pipeline.pkl
│   │
│   └─ api/
│            ├─ __init__.py
│            ├─ main.py
│            ├─ load_model.py
│            └─ schemas.py
│
├─ web/ # Archivos de la aplicación web
│ ├─ index.html
│ ├─ styles.css
│ └─ script.js
│
├─ requirements/
│            ├─ requirements_colab.txt
│            └─ requirements_dev.txt
│
├─ Dockerfile           # Contenedor
├─ start.sh             # Archivo para levantar API (en 8000) + web (en 8000) dentro del contenedor
├─ README.md      # Este archivo
└─ .gitignore     # Archivos ignorados
```

## Datos
Los datos originales son grandes y se almacenan externamente (Google Drive). Las rutas o enlaces deben ajustarse según el entorno del colaborador.
El archivo final utilizado para el entrenamiento estará disponible en:

data/cleaned_dataset.csv

## Uso

### 1️. Preparación del entorno

Dependiendo del entorno de trabajo::

- **En Google Colab**:
```
!pip install -r requirements/requirements_colab.txt
```
- **En entorno local (VS Code)**
```
pip install -r requirements/requirements_dev.txt
```
En ***Google Colab*** se prioriza la experimentación rápida, instalando versiones más flexibles de librerías para probar distintos enfoques y explorar datos sin restricciones estrictas.
En ***entorno de desarrollo local*** (VS Code), se utilizan versiones acotadas y controladas de las dependencias para garantizar ***reproducibilidad exacta***, coherencia con el flujo de producción y alineación con buenas prácticas de empresas de ML.

### 2️. Ejecución de scripts de entrenamiento

Los scripts dentro de `src/` están pensados para ejecutarse **como módulos de Python**, desde la raíz del proyecto (`TFM/`).

Por ejemplo, para entrenar el modelo LightGBM:

```
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

## Estilo de código

Todos los notebooks y scripts Python de este proyecto han sido adaptados siguiendo
las **buenas prácticas de PEP8**. Durante la verificación con `nbqa pylint`, cada
notebook y script de VS Code obtuvo una **puntuación de 10/10**, lo que asegura un 
código consistente, legible y mantenible.

Entre las buenas prácticas aplicadas se incluyen:

- Nombres de variables, funciones y clases consistentes y descriptivos.
- Longitud de líneas controlada para facilitar la lectura.
- Docstrings explicativos en funciones y clases.
- Organización de imports según el estándar PEP8.
- Eliminación de variables no utilizadas y advertencias de redefinitions.
- Uso de pipelines y transformadores de forma clara y modular.

Se recomienda a cualquier colaborador seguir utilizando herramientas como
`pylint` o `nbqa pylint` para mantener la conformidad con PEP8 durante el desarrollo.

## Inferencia / API

Para usar el modelo entrenado en inferencia:

1. Importar la función de carga del modelo:

```
from src.api.load_model import load_pipeline

pipeline = load_pipeline("src/models/lgbm_diabetes_pipeline.pkl")
```

2. Predecir con nuevos datos (DataFrame `X_new`):

```
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
      |
      v
HTML (muestra el resultado en: <p id="prediction">)

```

## Autor

Jesús Rodríguez Fernández  
Rafael Risco Murillo 
Cristina Crespo Barreda
