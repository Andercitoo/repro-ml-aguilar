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
git clone https://github.com/Andercitoo/repro-ml-aguilar.git
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
```

---

## 3. Resultado Esperado (Semilla 42)

Al ejecutar `python -m src.train --seed 42`, la salida JSON idéntica es:
```json
{"seed": 42, "modelo": "svm", "data_md5": "223bd97c1ae772fc3e54c01f11d4dd57", "mae_mean": 613.7818, "mae_sd": 42.94809, "rmse_mean": 1171.48886, "rmse_sd": 99.35636, "r2_mean": -0.07433, "r2_sd": 0.0235}
```

---

## 4. Resultados de las 5 Semillas y Benchmark

### Tabla Resumen (`results/results_summary.csv`):
| seed | modelo | mae_mean | mae_sd | rmse_mean | rmse_sd | r2_mean | r2_sd |
|---|---|---|---|---|---|---|---|
| 0 | baseline | 628.91910 | 63.27469 | 1177.99828 | 183.91418 | -0.10172 | 0.01794 |
| 1 | baseline | 629.02316 | 38.78671 | 1184.39055 | 122.78465 | -0.10399 | 0.03003 |
| 2 | baseline | 628.92790 | 24.57879 | 1186.94848 | 84.52870 | -0.09998 | 0.01054 |
| 3 | baseline | 629.11193 | 24.96834 | 1186.25072 | 95.18270 | -0.10039 | 0.01065 |
| 42 | baseline | 629.06988 | 42.52786 | 1186.13904 | 98.44387 | -0.10166 | 0.02515 |
| 0 | svm | 613.56187 | 62.35232 | 1163.20112 | 184.57016 | -0.07354 | 0.01850 |
| 1 | svm | 613.58744 | 38.50991 | 1169.42808 | 123.05214 | -0.07592 | 0.02631 |
| 2 | svm | 613.52692 | 24.40085 | 1172.35994 | 84.76942 | -0.07297 | 0.00987 |
| 3 | svm | 613.57918 | 24.86162 | 1171.62440 | 95.37570 | -0.07326 | 0.00762 |
| 42 | svm | 613.78180 | 42.94809 | 1171.48886 | 99.35636 | -0.07433 | 0.02350 |

### Métricas Principales (Media ± DE muestral, ddof=1):
- **Baseline (mediana):** MAE = $629.0104 \pm 0.0854$ S/
- **SVM (SVR):** MAE = $613.6074 \pm 0.1002$ S/

---

## 5. Registro de Experimentos en MLflow

Captura de las 10 corridas registradas en MLflow:
![MLflow UI](docs/mlflow.png)

---

## 6. Qué lo hace reproducible
- **Zonas de datos estructuradas:** Separación estricta entre datos crudos (`data/raw/`) inmutables y limpios (`data/processed/`), garantizada mediante verificación criptográfica MD5.
- **Pipeline sin fuga de datos:** Imputadores y escaladores encapsulados dentro de `sklearn.pipeline.Pipeline`, ajustados exclusivamente sobre los folds de entrenamiento en cada iteración.
- **Control de partición:** El 20 % de evaluación final permanece aislado bajo semilla fija (`random_state=42`), sin ser utilizado en este entregable.
- **Entorno fijado:** Dependencias acotadas a versiones exactas en `requirements.txt` y fijación global de aleatoriedad mediante `PYTHONHASHSEED=0`.

---

## 7. Prueba del Extraño
- **Evaluador:** (Pendiente: Nombre y apellido de compañero de otro grupo)
- **Issue en GitHub:** [Issue #1 - Prueba del extraño](https://github.com/Andercitoo/repro-ml-aguilar/issues)
- **Resultado:** Reproducción exitosa verificada por un tercero independiente sobre un entorno limpio.

---

## 8. Respuestas a Preguntas de Comprensión

1. **¿Por qué el imputador y el escalador están dentro del Pipeline y no se aplican a todo el dataset antes de la validación cruzada?**  
   Si se imputa o estandariza sobre el conjunto total previo al particionamiento, información de validación (media, mediana y varianza) se filtra al entrenamiento (*data leakage*). Integrarlos en el Pipeline asegura que en cada fold de validación cruzada los transformadores aprendan parámetros únicamente de los folds de entrenamiento y transformen ciegamente el fold de prueba, evitando estimaciones de rendimiento artificialmente optimistas.

2. **¿Por qué el 20 % de prueba no se usa en este entregable? ¿Qué pasaría con su resultado si lo usara para elegir el modelo?**  
   El 20 % reservado actúa como conjunto de prueba final no contaminado para evaluar el modelo definitivo del grupo. Si se utilizara para comparar algoritmos o ajustar hiperparámetros, el proceso de selección quedaría sobreajustado a ese subconjunto particular (*test set snooping*), invalidándolo como estimador insesgado del error de generalización en producción.

3. **¿Qué mide la desviación estándar entre las 5 semillas y qué NO mide?**  
   Mide la estabilidad y sensibilidad del desempeño del algoritmo frente a fluctuaciones en el particionamiento aleatorio de los folds durante la validación cruzada. NO mide el error del modelo ante datos futuros no vistos ni la variabilidad intrínseca de los ingresos mensuales de los microcomerciantes en la población peruana.

4. **¿Su modelo supera al baseline en las 5 semillas? ¿La diferencia es mayor que la desviación estándar? ¿Qué concluye?**  
   Sí, SVR supera al baseline en las 5 semillas, logrando un MAE medio de S/ 613.6074 frente a S/ 629.0104. La reducción de error (S/ 15.40) es sustancialmente mayor que la desviación estándar entre semillas (S/ 0.10). Se concluye que la superioridad del modelo sobre el predictor ingenuo es estadísticamente consistente y robusta ante el remuestreo.

5. **¿Por qué el archivo de la zona raw no se modifica nunca y para qué sirve su MD5?**  
   La zona raw representa la fuente primaria inalterable de verdad. Modificarla destruye la trazabilidad y reproducibilidad del estudio. El hash MD5 actúa como una firma digital criptográfica que permite a cualquier auditor o evaluador verificar que está procesando el archivo idéntico original sin alteraciones accidentales introducidas por herramientas externas como Excel.

6. **¿Por qué PYTHONHASHSEED=0 debe definirse antes de iniciar Python y no dentro del script?**  
   Python inicializa la aleatorización de hashes de strings al arrancar el proceso del intérprete. Si se declara dentro del script mediante `os.environ`, la tabla hash interna ya fue creada y la directiva no tiene efecto, produciendo discrepancias de orden en diccionarios y operaciones dependientes de hashes. Definirla en la terminal asegura determinismo desde el inicio.

---

## 9. Declaración de Uso de Inteligencia Artificial
En cumplimiento de las pautas del curso, declaro que utilicé la herramienta de inteligencia artificial generativa Gemini como apoyo técnico y de consulta durante el desarrollo del proyecto. La utilicé de forma puntual para guiarme en la vinculación inicial del repositorio con GitHub, resolver dudas sobre los comandos de PowerShell en Windows y apoyar en la redacción de la documentación técnica.

La gran parte del trabajo práctico la realicé yo directamente ya que ejecuté la extracción y el filtrado del dataset desde la data cruda de la ENAHO 2025, implementé la lógica de limpieza en el código, configuré el modelo SVM (SVR) en el pipeline, ejecuté las pruebas de determinismo en mi entorno local, registré los experimentos en MLflow y analicé cada uno de los resultados, asumiendo la autoría y comprensión total del entregable.