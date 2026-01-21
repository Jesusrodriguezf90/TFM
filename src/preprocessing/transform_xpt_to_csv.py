"""
Script: transform_xpt_to_csv.py
Objetivo: Convertir el dataset original en formato XPT a CSV para
facilitar su uso en procesos de análisis, preprocessing y modelado.

Autor: Jesús Rodríguez
Fecha: 16/12/2025
"""

# Librerías básicas
from pathlib import Path
import pandas as pd


def convert_xpt_to_csv(xpt_filename: str, csv_filename: str) -> None:
    """
    Convierte un archivo XPT a formato CSV y lo guarda en la carpeta de datos.

    Args:
        xpt_filename (str): Nombre del archivo XPT de entrada.
        csv_filename (str): Nombre del archivo CSV de salida.

    Returns:
        None
    """
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data"

    xpt_path = data_path / xpt_filename
    csv_path = data_path / csv_filename

    # Carga del archivo XPT
    df = pd.read_sas(xpt_path, format="xport", encoding="latin1")

    # Guardado como CSV
    df.to_csv(csv_path, index=False)

    print(f"Archivo CSV creado correctamente en: {csv_path}")


if __name__ == "__main__":
    convert_xpt_to_csv(
        "raw_dataset.xpt", 
        "raw_dataset.csv"
        )
