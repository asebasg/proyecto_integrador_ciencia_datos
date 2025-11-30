import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos, verificar_duplicados

st.set_page_config(page_title="Recolección de Datos", layout="wide")
st.title("📊 Recolección de Datos")

st.markdown("""
### 📦 Fuente de Información
Los datos utilizados en este proyecto provienen de fuentes oficiales gubernamentales.

* **Fuente Principal:** Secretaría de Salud y Protección Social de Antioquia.
* **Dataset:** `suicidios-en-antioquia.csv`
* **Periodo:** 2005 - 2024
* **Cobertura:** 125 Municipios (9 Subregiones)
""")

# Cargar datos usando tu función
df = cargar_datos()

if not df.empty:
    st.success("✅ Datos cargados exitosamente")
    
    # Mostrar información del dataset
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Metadatos del Dataset")
        st.write(f"**Registros:** {len(df):,}")
        st.write(f"**Columnas:** {len(df.columns)}")
        
        # Usar nombres correctos de columnas (con mayúsculas)
        if 'Año' in df.columns:
            st.write("**Período:**", f"{df['Año'].min()} - {df['Año'].max()}")
        if 'NombreMunicipio' in df.columns:
            st.write("**Municipios:**", df['NombreMunicipio'].nunique())
        
        # Mostrar nombres de columnas REALES
        st.write("**Variables disponibles:**")
        for col in df.columns:
            st.write(f"- {col} ({df[col].dtype})")
    
    with col2:
        st.subheader("🔍 Calidad de Datos")
        duplicados = verificar_duplicados(df)
        st.write(f"**Duplicados:** {duplicados['total_duplicados']} ({duplicados['porcentaje_duplicados']:.2f}%)")
        st.write(f"**Valores faltantes:** {df.isnull().sum().sum()}")
        
        if duplicados['limpio']:
            st.success("✅ Dataset limpio de duplicados")
        else:
            st.warning("⚠️ Se encontraron duplicados")
    
    # Mostrar muestra de datos
    st.subheader("👀 Vista Preliminar de Datos")
    st.dataframe(df.head(10))
    st.caption(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    
    # Mostrar estadísticas básicas
    st.subheader("📊 Estadísticas Básicas")
    st.write(df.describe())
    
else:
    st.error("❌ No se pudieron cargar los datos")

st.markdown("""
### ⚠️ Limitaciones Identificadas
* La variable `NumeroPoblacionObjetivo` viene formateada como texto (con comas).
* No existen variables socioeconómicas detalladas (ingresos, educación) en este dataset.
* Los datos requieren transformación para análisis estadístico.
""")