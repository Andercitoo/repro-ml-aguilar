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
    df = pd.read_csv(RAW)
    n0 = len(df)
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    if CODIGOS_FALTANTES:
        df = df.replace(CODIGOS_FALTANTES, np.nan)
    df = df.dropna(subset=[TARGET])

    # ---- Limpieza propia del dataset del grupo (SentryBox) ----
    df = df[df[TARGET] > 0]
    if "tiene_trabajadores_pagados" in df.columns:
        df = df.drop(columns=["tiene_trabajadores_pagados"])
    # --------------------------------------------------------------

    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)
    print(f"raw:       {n0} filas | md5 {md5(RAW)}")
    print(f"processed: {len(df)} filas | md5 {md5(PROCESSED)}")


if __name__ == "__main__":
    main()