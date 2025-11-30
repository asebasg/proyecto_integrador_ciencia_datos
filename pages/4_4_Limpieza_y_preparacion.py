# Asignado a Ricardo (@ricardo778)

import streamlit as st
import pandas as pd
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import cargar_datos
from utils.preprocessing import *

st.set_page_config(page_title="Limpieza y Preparación", layout="wide")
st.title("🧹 Limpieza y Preparación de Datos")

st.markdown("""
### 🎯 Objetivo de esta fase
Transformar los datos crudos en un formato adecuado para análisis, aplicando:
- **Limpieza** de valores faltantes y duplicados
- **Transformaciones** para cálculo de tasas
- **Categorización** por niveles de riesgo
- **Validación** de la calidad de datos
""")

# Cargar datos originales
df_original = cargar_datos()

if not df_original.empty:
    # Mostrar estado inicial
    st.header("📊 Estado Inicial de los Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Registros originales", f"{len(df_original):,}")
    
    with col2:
        municipios_count = df_original['NombreMunicipio'].nunique()
        st.metric("Municipios", municipios_count)
    
    with col3:
        st.metric("Años cubiertos", f"{df_original['Anio'].min()}-{df_original['Anio'].max()}")
    
    # Mostrar datos originales
    st.subheader("👀 Vista de Datos Originales")
    st.dataframe(df_original.head(8), use_container_width=True)
    
    # Aplicar transformaciones
    st.header("🔄 Transformaciones Aplicadas")
    
    df_transformado = df_original.copy()
    
    # 1. Calcular tasas
    st.subheader("1. Cálculo de Tasas por 100,000 Habitantes")
    try:
        df_transformado = calcular_tasas(
            df_transformado, 
            'NumeroCasos', 
            'NumeroPoblacionObjetivo', 
            'tasa_suicidios'
        )
        st.success("✅ Tasa de suicidios calculada correctamente")
        
        # Mostrar ejemplo del cálculo
        st.write("**Ejemplo del cálculo:**")
        ejemplo = df_transformado[[
            'NombreMunicipio', 
            'Anio', 
            'NumeroCasos', 
            'NumeroPoblacionObjetivo', 
            'tasa_suicidios'
        ]].head(5)
        st.dataframe(ejemplo, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error calculando tasas: {e}")
    
    # 2. Categorizar por riesgo
    st.subheader("2. Categorización por Nivel de Riesgo")
    if 'tasa_suicidios' in df_transformado.columns:
        try:
            df_transformado = crear_categorias_riesgo(df_transformado, 'tasa_suicidios')
            st.success("✅ Niveles de riesgo asignados (Bajo/Medio/Alto)")
            
            # Mostrar distribución de riesgo
            st.write("**Distribución por nivel de riesgo:**")
            distribucion = df_transformado['nivel_riesgo'].value_counts()
            st.bar_chart(distribucion)
            
            # Mostrar estadísticas de riesgo
            st.write("**Resumen por categoría de riesgo:**")
            resumen_riesgo = df_transformado.groupby('nivel_riesgo').agg({
                'tasa_suicidios': ['mean', 'min', 'max'],
                'NombreMunicipio': 'count'
            }).round(2)
            st.dataframe(resumen_riesgo)
            
        except Exception as e:
            st.error(f"❌ Error categorizando riesgo: {e}")
    else:
        st.warning("⚠️ No se pudo categorizar por riesgo - tasa no calculada")
    
    # 3. Limpieza de datos faltantes
    st.subheader("3. Limpieza de Valores Faltantes")
    try:
        filas_antes = len(df_transformado)
        df_transformado = limpiar_datos_faltantes(df_transformado)
        filas_despues = len(df_transformado)
        
        if filas_antes == filas_despues:
            st.success("✅ No se encontraron valores faltantes")
        else:
            st.warning(f"⚠️ Se eliminaron {filas_antes - filas_despues} registros con valores faltantes")
    except Exception as e:
        st.error(f"❌ Error limpiando datos: {e}")
    
    # Mostrar comparación final
    st.header("📈 Comparación Final: Antes vs Después")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Antes de las Transformaciones")
        columnas_original = [
            'NombreMunicipio', 
            'Anio', 
            'NumeroCasos', 
            'NumeroPoblacionObjetivo'
        ]
        st.dataframe(df_original[columnas_original].head(8), use_container_width=True)
        st.caption(f"Forma original: {df_original.shape}")
    
    with col2:
        st.subheader("Después de las Transformaciones")
        columnas_transformadas = [
            'NombreMunicipio', 
            'Anio', 
            'NumeroCasos', 
            'NumeroPoblacionObjetivo'
        ]
        if 'tasa_suicidios' in df_transformado.columns:
            columnas_transformadas.append('tasa_suicidios')
        if 'nivel_riesgo' in df_transformado.columns:
            columnas_transformadas.append('nivel_riesgo')
            
        st.dataframe(df_transformado[columnas_transformadas].head(8), use_container_width=True)
        st.caption(f"Forma transformada: {df_transformado.shape}")
    
    # Resumen de transformaciones
    st.header("📋 Resumen de Transformaciones")
    
    transformaciones = [
        "✅ **Cálculo de tasas**: Tasa de suicidios por 100,000 habitantes", 
        "✅ **Categorización**: Niveles de riesgo (Bajo/Medio/Alto)",
        "✅ **Limpieza**: Eliminación de valores faltantes",
        "✅ **Validación**: Verificación de integridad de datos",
        "✅ **Conversión de formatos**: Población de texto a numérico"
    ]
    
    for transformacion in transformaciones:
        st.write(transformacion)
    
    # Información adicional sobre el dataset
    st.header("📊 Información del Dataset Procesado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Estadísticas de Tasas")
        if 'tasa_suicidios' in df_transformado.columns:
            stats = df_transformado['tasa_suicidios'].describe()
            st.write(f"**Media:** {stats['mean']:.2f}")
            st.write(f"**Mínimo:** {stats['min']:.2f}")
            st.write(f"**Máximo:** {stats['max']:.2f}")
            st.write(f"**Desviación estándar:** {stats['std']:.2f}")
    
    with col2:
        st.subheader("Distribución Geográfica")
        if 'NombreRegion' in df_transformado.columns:
            regiones = df_transformado['NombreRegion'].value_counts()
            st.dataframe(regiones)
        
else:
    st.error("❌ No se pudieron cargar los datos para el proceso de limpieza")

st.markdown("---")
st.success("🎉 El dataset resultante está listo para análisis estadístico y visualización.")
st.caption("Página desarrollada por Ricardo (@ricardo778) - Procesamiento y transformación de datos")