from pydantic import BaseModel, Field
from typing import Optional

class DiabetesInput(BaseModel):
    # Variables nominales
    BPHIGH4: Optional[int]
    RACE: Optional[int] = Field(alias="_RACE") # Pydantic v2 no permite campos que empiecen con _

    # Variables binarias
    BPMEDS: Optional[int]
    BLOODCHO: Optional[int]
    HAVARTH3: Optional[int]
    QLACTLM2: Optional[int]
    USEEQUIP: Optional[int]
    BLIND: Optional[int]
    DECIDE: Optional[int]
    DIFFWALK: Optional[int]
    DIFFALON: Optional[int]
    DIFFDRES: Optional[int]
    SMOKE100: Optional[int]
    ADDEPEV2: Optional[int]
    SEX: Optional[int]

    # Variables ordinales
    GENHLTH: Optional[int]
    PACAT1: Optional[int] = Field(alias="_PACAT1")
    AGEG5YR: Optional[int] = Field(alias="_AGEG5YR")
    BMI5CAT: Optional[int] = Field(alias="_BMI5CAT")

    # Variables numéricas
    EXEROFT1: Optional[float]
    FRUTSUM: Optional[float] = Field(alias="_FRUTSUM")
    VEGESUM: Optional[float] = Field(alias="_VEGESUM")

    model_config = {
        "populate_by_name": True  # Para usar dict(by_alias=True)
    }