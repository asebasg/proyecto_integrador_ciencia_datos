import pandas as pd
import numpy as np
from scipy.stats import pearsonr, chi2_contingency 

# =================================================================
# PASO 1: CARGA Y LIMPIEZA DE DATOS
# =================================================================

# Carga de Datos REALES
ruta_archivo = 'static/datasets/suicidios-en-antioquia.csv'

# Usamos encoding='latin1' para tildes, pero quitamos el sep=';'
# Pandas detectará automáticamente la coma como separador.
df = pd.read_csv(ruta_archivo, encoding='latin1')

print("Carga de datos exitosa.")
print("Columnas detectadas:", df.columns.tolist()) # Esto nos ayudará a depurar si falla

# Limpieza de nombres de columnas (quita espacios al inicio/final)
df.columns = df.columns.str.strip()

# Validación de seguridad: Verificar si la columna existe antes de operar
if 'NumeroPoblacionObjetivo' not in df.columns:
    print("\n⚠️ ERROR CRÍTICO: No encuentro la columna 'NumeroPoblacionObjetivo'.")
    print("Las columnas disponibles son:", df.columns.tolist())
    exit() # Detiene el script aquí si falla

# Limpieza de la columna de Población
# 1. Eliminar la coma (',') de los números
# 2. Convertir a entero
df['Poblacion'] = df['NumeroPoblacionObjetivo'].astype(str).str.replace(',', '', regex=False).astype(int)

# Limpieza de Casos
df['Casos'] = df['NumeroCasos'].astype(int)

# Eliminamos las columnas originales
df = df.drop(columns=['NumeroPoblacionObjetivo', 'NumeroCasos'])

print("Datos de Población y Casos limpios y listos.")

# =================================================================
# PASO 2: TAREA 1 - CÁLCULO DE TASAS NORMALIZADAS
# =================================================================

# Cálculo de la Tasa de Casos por cada 100.000 habitantes
df['Tasa_x_100k'] = (df['Casos'] / df['Poblacion']) * 100000

print("\n--- Resultados de la Tasa x 100k ---")

# =================================================================
# PASO 3: TAREA 2 - ANÁLISIS DE MUNICIPIOS Y RANKING ANUAL
# =================================================================

# 1. Ranking General
df_ranking = df.sort_values(by='Tasa_x_100k', ascending=False)

print("\nTop 5 de Casos Sobresalientes (Tasa más alta por Municipio y Año):")
print(df_ranking.head(5)[
    ['Anio', 'NombreMunicipio', 'NombreRegion', 'Casos', 'Poblacion', 'Tasa_x_100k']
])

# 2. Análisis de Municipios Pequeños (< 10k hab.)
POBLACION_UMBRAL = 10000
df_pequenos = df[df['Poblacion'] < POBLACION_UMBRAL].copy()

print(f"\nMunicipios Pequeños (< {POBLACION_UMBRAL} hab.) con las Tasas más altas:")
print(df_pequenos.sort_values(by='Tasa_x_100k', ascending=False).head(5)[
    ['Anio', 'NombreMunicipio', 'Poblacion', 'Tasa_x_100k']
])

# =================================================================
# PASO 4: TAREA 3 - INFLUENCIA DE LA REGIÓN Y EXPORTACIÓN
# =================================================================

# Análisis de la Influencia de la Región
df_region_agregado = df.groupby('NombreRegion').agg(
    Poblacion_Acumulada=('Poblacion', 'sum'),
    Casos_Acumulados=('Casos', 'sum')
).reset_index()

df_region_agregado['Tasa_Region_Global_x_100k'] = (
    df_region_agregado['Casos_Acumulados'] / df_region_agregado['Poblacion_Acumulada']
) * 100000

print("\nAnálisis de la Influencia de la Región (Tasa Global Acumulada):")
print(df_region_agregado.sort_values(by='Tasa_Region_Global_x_100k', ascending=False))

# Exportación
df_final = df.copy()
df_final.to_csv('datos_analisis_juan.csv', index=False)
print("\nArchivo 'datos_analisis_juan.csv' generado correctamente.")