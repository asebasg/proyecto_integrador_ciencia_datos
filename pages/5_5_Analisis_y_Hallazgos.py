import streamlit as st
import pandas as pd
from utils import preparar_df, calcular_correlacion, calcular_tasa_crecimiento, calcular_indice_riesgo

st.title("Análisis y hallazgos - Suicidios en Antioquia")

RUTA = 'static/datasets/suicidios-en-antioquia.csv'

@st.cache_data
def cargar():
    return preparar_df(RUTA)

df = cargar()

st.header("Correlación entre población y casos")
corr, p = calcular_correlacion(df, 'Poblacion', 'Casos')
st.write(f"Correlación (Pearson) Población vs Casos: r = {corr:.4f}, p = {p:.4g}")

st.header("Tasas de crecimiento por municipio (muestra)")
if 'Anio' in df.columns and 'NombreMunicipio' in df.columns:
    growth = calcular_tasa_crecimiento(df, group_col='NombreMunicipio', value_col='Casos', period_col='Anio')
    st.dataframe(growth.head(30))
else:
    st.info('Para ver tasas de crecimiento se requiere columnas `Anio` y `NombreMunicipio`.')

st.header("Índice de riesgo (z-score de tasa)")
risk = calcular_indice_riesgo(df)
df_risk = df.copy()
df_risk['Indice_Riesgo'] = risk
st.dataframe(df_risk.sort_values('Indice_Riesgo', ascending=False).head(20)[['Anio','NombreMunicipio','Casos','Poblacion','Tasa_x_100k','Indice_Riesgo']])
