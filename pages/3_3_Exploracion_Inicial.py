import streamlit as st
import pandas as pd
from utils import preparar_df, calcular_estadisticas_descriptivas, obtener_ranking_municipios

st.title("Exploración inicial de datos - Suicidios en Antioquia")

RUTA = 'static/datasets/suicidios-en-antioquia.csv'

@st.cache_data
def cargar():
    return preparar_df(RUTA)

df = cargar()

st.header("Muestra de los datos")
st.dataframe(df.head(20))

st.header("Estadísticas descriptivas (numéricas)")
st.dataframe(calcular_estadisticas_descriptivas(df))

st.header("Top 10 municipios por tasa (agregado)")
st.dataframe(obtener_ranking_municipios(df, top_n=10))
