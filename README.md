# TFM: Modelo de ML para detección de diabetes

## Descripción
Este proyecto tiene como objetivo desarrollar un modelo de Machine Learning para clasificar individuos en:
- Diabetes
- Prediabetes
- No diabetes

Se utiliza el dataset **BRFSS 2015** del CDC.

## Estructura del proyecto
TFM/
├─ src/ # Scripts de transformación y preprocesamiento de datos
├─ notebooks/ # Notebooks de análisis exploratorio y pruebas de modelos
├─ data/ # Referencias a los datos originales (no se incluyen archivos grandes)
├─ README.md # Este archivo
└─ .gitignore # Archivos ignorados

## Datos
Los datos originales son grandes y se almacenan externamente (Google Drive).  
Variables de ruta o enlaces deben ser ajustadas según el entorno del colaborador.

## Uso
1. Descargar dataset de BRFSS 2015 desde CDC.
2. Ejecutar los scripts en `src/` para limpiar y transformar los datos.
3. Correr notebooks en `notebooks/` para preprocesamiento y entrenamiento de modelos.

## Contribución
- Cada miembro clona el repositorio y trabaja dentro de la estructura de carpetas (`src/`, `notebooks/`, `data/`).
- Hacer **commits claros y frecuentes** con mensajes descriptivos:
  - "Añadir script de transformación XPT a CSV"
  - "Añadir notebook de análisis exploratorio"
- Antes de subir cambios al remoto, hacer **pull** para actualizar tu copia local y evitar conflictos.
- Hacer **push** al remoto solo cuando los cambios estén listos y probados.
- Revisar los cambios de los compañeros antes de integrarlos.

## Autor
Jesús Rodríguez
Rafael Risco
Cristina Crespo
