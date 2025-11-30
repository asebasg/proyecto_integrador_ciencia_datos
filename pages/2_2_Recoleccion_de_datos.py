import streamlit as st
import pandas as pd
import os

st.title("2️⃣ Recolección de Datos")

st.markdown("""
### 📦 Fuente de Información
Los datos utilizados en este proyecto provienen de fuentes oficiales gubernamentales.

* **Fuente Principal:** Secretaría de Salud y Protección Social de Antioquia.
* **Dataset:** `suicidios-en-antioquia.csv`
* **Periodo:** 2005 - 2024
* **Cobertura:** 125 Municipios (9 Subregiones)
""")

# Mostrar una muestra de los datos crudos (sin limpiar)
st.subheader("🕵️‍♂️ Vista Preliminar (Datos Crudos)")

# Ruta al archivo (ajusta si es necesario)
ruta_csv = 'data/suicidios-en-antioquia.csv'

if os.path.exists(ruta_csv):
    df_raw = pd.read_csv(ruta_csv)
    st.dataframe(df_raw.head())
    st.caption(f"Dimensiones originales: {df_raw.shape[0]} filas x {df_raw.shape[1]} columnas")
else:
    st.error("⚠️ No se encontró el archivo CSV en la carpeta 'data/'.")

st.markdown("""
### ⚠️ Limitaciones Identificadas
* La variable `NumeroPoblacionObjetivo` viene formateada como texto (con comas).
* No existen variables socioeconómicas detalladas (ingresos, educación) en este dataset.
""")