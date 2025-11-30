# Asignado a Ricardo (@ricardo778)

import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos, verificar_duplicados

st.set_page_config(page_title="Recolección de Datos", layout="wide")
st.title("📊 Recolección de Datos")

st.markdown("""
### 📦 Fuente de Información
Los datos utilizados en este proyecto provienen de fuentes oficiales gubernamentales.

* **Fuente Principal:** Secretaría de Salud y Protección Social de Antioquia.
* **Dataset:** `suicidios_antioquia.csv`
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
        st.write("**Período:**", f"{df['año'].min()} - {df['año'].max()}")
        st.write("**Municipios:**", df['municipio'].nunique() if 'municipio' in df.columns else "N/A")
        
        # Mostrar nombres de columnas
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
    
else:
    st.error("❌ No se pudieron cargar los datos")
    
    # Información de troubleshooting
    st.markdown("""
    ### 🔧 Solución de Problemas
    Si los datos no se cargan, verifica:
    1. Que el archivo `suicidios_antioquia.csv` esté en `static/datasets/`
    2. Que el nombre del archivo sea correcto
    3. Que el archivo tenga datos válidos
    """)

st.markdown("""
### ⚠️ Limitaciones Identificadas
* La variable `NumeroPoblacionObjetivo` viene formateada como texto (con comas).
* No existen variables socioeconómicas detalladas (ingresos, educación) en este dataset.
* Los datos requieren transformación para análisis estadístico.
""")

# Información adicional sobre el proceso
st.markdown("""
### 🔄 Proceso de Carga
Los datos se cargan mediante la función `cargar_datos()` ubicada en `utils/data_loader.py`, 
la cual incluye cache para mejor rendimiento y manejo de errores.
""")