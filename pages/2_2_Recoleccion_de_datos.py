# Asignado a Ricardo (@ricardo778)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    
    # KPI Cards en la parte superior
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Registros", f"{len(df):,}")
    
    with col2:
        st.metric("🏙️ Municipios", df['NombreMunicipio'].nunique())
    
    with col3:
        st.metric("🗺️ Regiones", df['NombreRegion'].nunique())
    
    with col4:
        st.metric("📅 Período", f"{df['Anio'].min()}-{df['Anio'].max()}")
    
    # GRÁFICA 1: Distribución por región
    st.subheader("🗺️ Distribución Geográfica por Región")
    
    region_data = df['NombreRegion'].value_counts().reset_index()
    region_data.columns = ['Region', 'Cantidad']
    
    fig_regiones = px.bar(
        region_data, 
        x='Region', 
        y='Cantidad',
        color='Cantidad',
        color_continuous_scale='blues',
        title='Registros por Región'
    )
    fig_regiones.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_regiones, use_container_width=True)
    
    # GRÁFICA 2: Evolución temporal de casos
    st.subheader("📈 Evolución Temporal de Casos")
    
    casos_por_año = df.groupby('Anio')['NumeroCasos'].sum().reset_index()
    
    fig_temporal = px.area(
        casos_por_año,
        x='Anio',
        y='NumeroCasos',
        title='Total de Casos por Año - Tendencias',
        line_shape='spline'
    )
    fig_temporal.update_traces(line=dict(width=4), fillcolor='rgba(100, 150, 255, 0.2)')
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # GRÁFICA 3: Top 10 municipios con más casos
    st.subheader("🏆 Top 10 Municipios con Más Casos")
    
    top_municipios = df.groupby('NombreMunicipio')['NumeroCasos'].sum().nlargest(10).reset_index()
    
    fig_top = px.bar(
        top_municipios,
        x='NumeroCasos',
        y='NombreMunicipio',
        orientation='h',
        color='NumeroCasos',
        color_continuous_scale='reds',
        title='Top 10 Municipios por Número de Casos'
    )
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)
    
    # GRÁFICA 4: Distribución de tipos de población
    st.subheader("👥 Distribución por Tipo de Población")
    
    poblacion_data = df['TipoPoblacionObjetivo'].value_counts().reset_index()
    poblacion_data.columns = ['TipoPoblacion', 'Cantidad']
    
    fig_poblacion = px.pie(
        poblacion_data,
        values='Cantidad',
        names='TipoPoblacion',
        title='Distribución por Tipo de Población Objetivo',
        hole=0.4
    )
    st.plotly_chart(fig_poblacion, use_container_width=True)
    
    # GRÁFICA 5: Calidad de datos visual
    st.subheader("🔍 Calidad de Datos - Dashboard Visual")
    
    duplicados = verificar_duplicados(df)
    faltantes = df.isnull().sum().sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Indicador de duplicados
        fig_duplicados = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = duplicados['porcentaje_duplicados'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Duplicados (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 20], 'color': "yellow"},
                    {'range': [20, 100], 'color': "red"}
                ]
            }
        ))
        fig_duplicados.update_layout(height=300)
        st.plotly_chart(fig_duplicados, use_container_width=True)
    
    with col2:
        # Indicador de valores faltantes
        fig_faltantes = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (faltantes / len(df)) * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Valores Faltantes (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 1], 'color': "lightgreen"},
                    {'range': [1, 5], 'color': "yellow"},
                    {'range': [5, 100], 'color': "red"}
                ]
            }
        ))
        fig_faltantes.update_layout(height=300)
        st.plotly_chart(fig_faltantes, use_container_width=True)
    
    with col3:
        # Indicador de completitud
        completitud = 100 - ((faltantes / (len(df) * len(df.columns))) * 100)
        fig_completitud = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = completitud,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Completitud del Dataset (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 80], 'color': "red"},
                    {'range': [80, 95], 'color': "yellow"},
                    {'range': [95, 100], 'color': "lightgreen"}
                ]
            }
        ))
        fig_completitud.update_layout(height=300)
        st.plotly_chart(fig_completitud, use_container_width=True)
    
else:
    st.error("❌ No se pudieron cargar los datos")

st.markdown("""
### ⚠️ Limitaciones Identificadas
* La variable `NumeroPoblacionObjetivo` viene formateada como texto (con comas)
* No existen variables socioeconómicas detalladas (ingresos, educación) en este dataset
* Los datos requieren transformación para análisis estadístico
""")