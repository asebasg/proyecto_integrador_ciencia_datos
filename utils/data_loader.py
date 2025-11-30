import streamlit as st
import pandas as pd
import os

@st.cache_data
def cargar_datos():
    """
    Carga el dataset de suicidios desde el archivo CSV
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        # Usar el nombre correcto del archivo
        df = pd.read_csv('static/datasets/suicidios-en-antioquia.csv')
        st.success(f"✅ Datos cargados correctamente: {len(df)} filas × {len(df.columns)} columnas")
        return df
    except FileNotFoundError:
        st.error("❌ No se pudo encontrar el archivo: static/datasets/suicidios-en-antioquia.csv")
        
        # Mostrar qué archivos sí existen para ayudar con el debug
        if os.path.exists('static/datasets'):
            archivos = os.listdir('static/datasets')
            st.write("📁 Archivos en static/datasets/:", archivos)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        return pd.DataFrame()

def verificar_duplicados(df):
    """
    Verifica y reporta duplicados en el dataset
    Args:
        df (pd.DataFrame): DataFrame a verificar
    Returns:
        dict: Estadísticas de duplicados
    """
    if df.empty:
        return {'total_duplicados': 0, 'porcentaje_duplicados': 0, 'limpio': True}
    
    total_duplicados = df.duplicated().sum()
    porcentaje_duplicados = (total_duplicados / len(df)) * 100
    
    return {
        'total_duplicados': total_duplicados,
        'porcentaje_duplicados': porcentaje_duplicados,
        'limpio': total_duplicados == 0
    }