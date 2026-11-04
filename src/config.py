"""Configuración del proyecto. Es el ÚNICO archivo que deben adaptar a su dataset."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Zonas del data lake
RAW = ROOT / "data" / "raw" / "sentrybox_enaho2025.csv"
PROCESSED = ROOT / "data" / "processed" / "dataset.csv"
RESULTS = ROOT / "results" / "results_summary.csv"

TARGET = "ganancia_neta_mes"
TAREA = "regresion"

COLS_NUM = [
    "edad",
    "horas_semana",
    "anios_en_ocupacion",
    "personas_en_negocio"
]

COLS_CAT = [
    "sexo_mujer",
    "estado_civil",
    "nivel_educativo",
    "es_empleador",
    "ayuda_familiar_no_remunerado",
    "registro_sunat",
    "lleva_libros_contables",
    "tiene_ocupacion_secundaria",
    "subsector_ciiu",
    "dominio",
    "estrato",
    "mes_encuesta"
]

CODIGOS_FALTANTES = [99, 9999, 999999]

# Algoritmo asignado: Integrante 5 -> SVM (SVR en regresión)
MODELO = "svm"

SEMILLA_PARTICION = 42
SEMILLAS = [0, 1, 2, 3, 42]