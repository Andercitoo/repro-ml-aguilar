# Pipeline de Machine Learning Reproducible - SentryBox

Repositorio individual para la EC2 del curso Machine Learning I (Universidad Científica del Sur).
- **Autor:** Anderson Aguilar Huamán
- **Algoritmo asignado:** SVM (Support Vector Regression - SVR)
- **Problema:** Estimación de la ganancia neta mensual de microcomerciantes peruanos (ENAHO 2025) para preaprobar líneas de capital de trabajo.

---

## 1. Entorno de Ejecución
- **Sistema Operativo:** Windows 11 (64-bit)
- **Versión de Python:** Python 3.11+
- **Dependencias:** Listadas con versiones fijadas en `requirements.txt`.

---

## 2. Cómo Reproducir

### En Windows (PowerShell):
```powershell
# 1. Clonar el repositorio y entrar
git clone [https://github.com/Andercitoo/repro-ml-aguilar.git](https://github.com/Andercitoo/repro-ml-aguilar.git)
cd repro-ml-aguilar

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Instalar dependencias exactas
pip install -r requirements.txt

# 4. Fijar semilla hash y preparar datos
$env:PYTHONHASHSEED=0
python -m src.prepare_data

# 5. Ejecutar corrida determinista (semilla 42)
python -m src.train --seed 42

# 6. Ejecutar las 5 semillas y registrar en MLflow
python -m src.run_seeds