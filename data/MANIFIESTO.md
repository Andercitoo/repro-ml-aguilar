# Manifiesto de Datos - SentryBox

## 1. Identificación y Fuente
- **Fuente Oficial:** Instituto Nacional de Estadística e Informática (INEI), Encuesta Nacional de Hogares (ENAHO) 2025, Módulo 500 «Empleo e Ingresos».
- **URL de Descarga:** https://proyectos.inei.gob.pe/microdatos/
- **Fecha de Descarga:** Octubre 2026
- **Licencia:** Datos abiertos del Estado peruano para fines académicos y de investigación estadística.

## 2. Integridad de los Archivos
- **Archivo Raw:** `data/raw/sentrybox_enaho2025.csv`
  - Filas originales: 4765
  - MD5: `5caa212fdfd858bb9a4f218d43c94d8d`
- **Archivo Processed:** `data/processed/dataset.csv`
  - Filas procesadas: 4761
  - MD5: `223bd97c1ae772fc3e54c01f11d4dd57`

## 3. Diccionario de Variables del Modelo
- `ganancia_neta_mes` (Objetivo): Ganancia neta en soles del mes anterior (P530A).
- `edad`: Edad en años cumplidos (P208A).
- `horas_semana`: Horas trabajadas en la semana previa (P513T).
- `anios_en_ocupacion`: Años en el negocio (P513A1 + P513A2/12).
- `personas_en_negocio`: Total de trabajadores incluido el titular (P512B).
- `sexo_mujer`: 1 si es mujer, 0 si es hombre (P207).
- `estado_civil`: Estado civil codificado 1 a 6 (P209).
- `nivel_educativo`: Nivel educativo aprobado 1 a 12 (P301A).
- `es_empleador`: 1 si es empleador, 0 si es independiente (P507).
- `ayuda_familiar_no_remunerado`: 1 si cuenta con apoyo familiar sin remunerar (P508).
- `registro_sunat`: 1 jurídica, 2 persona natural con RUC, 3 sin RUC (P510A1).
- `lleva_libros_contables`: 1 si lleva libros, 0 si no (P510B).
- `tiene_ocupacion_secundaria`: 1 si tiene otro trabajo (P514).
- `subsector_ciiu`: Código de actividad económica minorista (P506R4).
- `dominio`, `estrato`, `mes_encuesta`: Variables de control geográfico y temporal del INEI.

## 4. Transformaciones Aplicadas
- Filtrado a comerciantes minoristas (CIIU 4700-4799) independientes y empleadores.
- Reemplazo de códigos de omisión (99, 9999, 999999) por valores nulos (NaN).
- Eliminación de registros duplicados y validación de ganancia neta > 0.
- Exclusión de `tiene_trabajadores_pagados` por colinealidad perfecta (r = 1.0) con `es_empleador`.