"""
Módulo de preprocesamiento de datos

Funciones para transformar y limpiar el dataset de suicidios en Antioquia

Asignado a Ricardo (@ricardo778)
"""

import pandas as pd
import streamlit as st

def calcular_tasas(df, col_casos='NumeroCasos', col_poblacion='NumeroPoblacionObjetivo', nombre_tasa='tasa_suicidios'):
    """
    Calcula tasas por cada 100,000 habitantes
    """
    try:
        # Convertir población a numérico si viene con comas
        if df[col_poblacion].dtype == 'object':
            df[col_poblacion] = df[col_poblacion].str.replace(',', '').astype(float)
        
        df[nombre_tasa] = (df[col_casos] / df[col_poblacion]) * 100000
        return df
    except Exception as e:
        st.error(f"Error calculando tasas: {e}")
        return df

def filtrar_por_municipio(df, municipio):
    """
    Filtra datos por municipio específico
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        municipio (str): Nombre del municipio a filtrar
    
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    return df[df['NombreMunicipio'] == municipio]

def agrupar_por_año(df):
    """
    Agrupa casos por año
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
    
    Returns:
        pd.DataFrame: DataFrame agrupado por año
    """
    return df.groupby('Año').agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'mean'
    }).reset_index()

def agrupar_por_municipio(df):
    """
    Agrupa casos por municipio (total histórico)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
    
    Returns:
        pd.DataFrame: DataFrame agrupado por municipio
    """
    return df.groupby('NombreMunicipio').agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'mean',
        'Año': 'count'  # Número de años con datos
    }).reset_index()

def crear_categorias_riesgo(df, col_tasa):
    """
    Categoriza municipios por nivel de riesgo según tasas
    
    Args:
        df (pd.DataFrame): DataFrame con tasas calculadas
        col_tasa (str): Columna con la tasa de suicidios
    
    Returns:
        pd.DataFrame: DataFrame con categorías de riesgo
    """
    try:
        categorias = ['Bajo riesgo', 'Riesgo medio', 'Alto riesgo']
        
        df['nivel_riesgo'] = pd.cut(df[col_tasa], 
                                   bins=[0, 5, 10, float('inf')], 
                                   labels=categorias, 
                                   right=False)
        return df
    except Exception as e:
        st.error(f"Error categorizando riesgo: {e}")
        return df

def limpiar_datos_faltantes(df):
    """
    Limpia valores faltantes del dataset
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
    
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    try:
        filas_antes = len(df)
        df_limpio = df.dropna()
        filas_despues = len(df_limpio)
        
        if filas_antes != filas_despues:
            st.warning(f"Se eliminaron {filas_antes - filas_despues} filas con valores faltantes")
        
        return df_limpio
    except Exception as e:
        st.error(f"Error limpiando datos: {e}")
        return df