import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    """
    Carga el dataset de suicidios desde el archivo CSV
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        df = pd.read_csv('static/datasets/suicidios_antioquia.csv')
        return df
    except FileNotFoundError:
        st.error("❌ No se pudo encontrar el archivo de datos")
        return pd.DataFrame()

def verificar_duplicados(df):
    """
    Verifica y reporta duplicados en el dataset
    Args:
        df (pd.DataFrame): DataFrame a verificar
    Returns:
        dict: Estadísticas de duplicados
    """
    total_duplicados = df.duplicated().sum()
    porcentaje_duplicados = (total_duplicados / len(df)) * 100
    
    return {
        'total_duplicados': total_duplicados,
        'porcentaje_duplicados': porcentaje_duplicados,
        'limpio': total_duplicados == 0
    }