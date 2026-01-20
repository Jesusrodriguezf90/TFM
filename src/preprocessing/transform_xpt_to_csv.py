from pathlib import Path
import pandas as pd


def convert_xpt_to_csv(xpt_filename: str, csv_filename: str) -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "Data"

    # Cargar XPT
    df = pd.read_sas(data_path / xpt_filename, format="xport", encoding="latin1")

    # Guardar como CSV
    df.to_csv(data_path / csv_filename, index=False)


if __name__ == "__main__":
    convert_xpt_to_csv("raw_dataset.xpt", "raw_dataset.csv")
