"""Zona raw -> zona processed.

Run:  PYTHONHASHSEED=0 python -m src.prepare_data
"""
import hashlib

import numpy as np
import pandas as pd

from src.config import CODIGOS_FALTANTES, PROCESSED, RAW, TARGET


def md5(path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def main() -> None:
    df = pd.read_csv(RAW)                       # la zona raw solo se LEE
    n0 = len(df)
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    if CODIGOS_FALTANTES:
        df = df.replace(CODIGOS_FALTANTES, np.nan)
    df = df.dropna(subset=[TARGET])             # sin objetivo no se puede entrenar

    # ---- Limpieza propia del dataset del grupo ----

    # Verificar que todas las variables configuradas existan
    from src.config import COLS_CAT, COLS_NUM

    columnas_requeridas = [TARGET] + COLS_NUM + COLS_CAT

    columnas_faltantes = [
        col for col in columnas_requeridas
        if col not in df.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            f"Faltan columnas necesarias: {columnas_faltantes}"
        )

    # Verificar que la variable objetivo sea numérica
    if not pd.api.types.is_numeric_dtype(df[TARGET]):
        raise TypeError(
            f"La variable objetivo {TARGET} debe ser numérica."
        )

    # Se conserva el valor faltante de nivel_educativo.
    # Su imputación se realizará dentro del Pipeline
    # durante la validación cruzada.

    # --------------------------------------------------------------

    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)
    print(f"raw:       {n0} filas | md5 {md5(RAW)}")
    print(f"processed: {len(df)} filas | md5 {md5(PROCESSED)}")


if __name__ == "__main__":
    main()