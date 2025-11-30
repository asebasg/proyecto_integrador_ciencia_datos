# Asignado a Ricardo (@ricardo778)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    # KPI Cards principales
    st.header("📊 Estado Inicial del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📥 Registros Iniciales", f"{len(df_original):,}")
    
    with col2:
        st.metric("🏙️ Municipios", df_original['NombreMunicipio'].nunique())
    
    with col3:
        st.metric("📅 Rango de Años", f"{df_original['Anio'].min()}-{df_original['Anio'].max()}")
    
    with col4:
        st.metric("🗺️ Regiones", df_original['NombreRegion'].nunique())
    
    # Aplicar transformaciones
    st.header("🔄 Proceso de Transformación")
    
    df_transformado = df_original.copy()
    
    # 1. CALCULAR TASAS - SECCIÓN VISUAL
    st.subheader("📊 1. Cálculo de Tasas por 100,000 Habitantes")
    
    try:
        df_transformado = calcular_tasas(
            df_transformado, 
            'NumeroCasos', 
            'NumeroPoblacionObjetivo', 
            'tasa_suicidios'
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # KPI de tasa promedio
            tasa_promedio = df_transformado['tasa_suicidios'].mean()
            fig_kpi_tasa = go.Figure(go.Indicator(
                mode = "number",
                value = tasa_promedio,
                number = {'suffix': " por 100k"},
                title = {"text": "Tasa Promedio de Suicidios"},
                domain = {'x': [0, 1], 'y': [0, 1]}
            ))
            fig_kpi_tasa.update_layout(height=200)
            st.plotly_chart(fig_kpi_tasa, use_container_width=True)
        
        with col2:
            # Histograma de tasas
            fig_tasas = px.histogram(
                df_transformado,
                x='tasa_suicidios',
                nbins=50,
                title='Distribución de Tasas de Suicidio',
                color_discrete_sequence=['#FF6B6B']
            )
            st.plotly_chart(fig_tasas, use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ Error calculando tasas: {e}")
    
    # 2. CATEGORIZACIÓN DE RIESGO - SECCIÓN VISUAL
    st.subheader("🎯 2. Categorización por Nivel de Riesgo")
    
    if 'tasa_suicidios' in df_transformado.columns:
        try:
            df_transformado = crear_categorias_riesgo(df_transformado, 'tasa_suicidios')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart de distribución de riesgo
                riesgo_counts = df_transformado['nivel_riesgo'].value_counts()
                fig_riesgo = px.pie(
                    values=riesgo_counts.values,
                    names=riesgo_counts.index,
                    title='Distribución por Nivel de Riesgo',
                    color_discrete_sequence=['#4CAF50', '#FFC107', '#F44336'],
                    hole=0.3
                )
                st.plotly_chart(fig_riesgo, use_container_width=True)
            
            with col2:
                # Violin plot de tasas por categoría
                fig_violin = px.violin(
                    df_transformado,
                    x='nivel_riesgo',
                    y='tasa_suicidios',
                    title='Distribución de Tasas por Nivel de Riesgo',
                    color='nivel_riesgo',
                    color_discrete_sequence=['#4CAF50', '#FFC107', '#F44336'],
                    box=True
                )
                st.plotly_chart(fig_violin, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error categorizando riesgo: {e}")
    
    # 3. LIMPIEZA DE DATOS - SECCIÓN VISUAL
    st.subheader("🧼 3. Limpieza de Valores Faltantes")
    
    try:
        filas_antes = len(df_transformado)
        df_transformado = limpiar_datos_faltantes(df_transformado)
        filas_despues = len(df_transformado)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Indicador de retención
            retencion = (filas_despues / filas_antes) * 100
            fig_retencion = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = retencion,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Retención de Datos (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "green"},
                    'steps': [
                        {'range': [0, 90], 'color': "red"},
                        {'range': [90, 99], 'color': "yellow"},
                        {'range': [99, 100], 'color': "lightgreen"}
                    ]
                }
            ))
            fig_retencion.update_layout(height=300)
            st.plotly_chart(fig_retencion, use_container_width=True)
        
        with col2:
            # Gráfica de comparación antes/después
            fig_comparacion = go.Figure()
            fig_comparacion.add_trace(go.Bar(
                name='Antes de Limpieza',
                x=['Registros'],
                y=[filas_antes],
                marker_color='orange'
            ))
            fig_comparacion.add_trace(go.Bar(
                name='Después de Limpieza',
                x=['Registros'],
                y=[filas_despues],
                marker_color='green'
            ))
            fig_comparacion.update_layout(title='Comparación: Registros Antes y Después de Limpieza')
            st.plotly_chart(fig_comparacion, use_container_width=True)
                
    except Exception as e:
        st.error(f"❌ Error limpiando datos: {e}")
    
    # RESUMEN VISUAL DEL PROCESO
    st.header("📈 Resumen Visual del Proceso de Transformación")
    
    # Gráfica de radar para mostrar el progreso
    categorias = ['Carga Datos', 'Cálculo Tasas', 'Categorización', 'Limpieza']
    valores = [100, 100, 100, retencion]  # Asumiendo 100% éxito en otros pasos
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Progreso del Proceso',
        line=dict(color='blue')
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Progreso del Proceso de Transformación"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # KPI FINALES
    st.header("🎉 Resultados Finales del Proceso")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_final_registros = go.Figure(go.Indicator(
            mode = "number",
            value = len(df_transformado),
            title = {"text": "Registros Finales"},
            number = {'valueformat': ","},
            domain = {'x': [0, 1], 'y': [0, 1]}
        ))
        fig_final_registros.update_layout(height=200)
        st.plotly_chart(fig_final_registros, use_container_width=True)
    
    with col2:
        if 'tasa_suicidios' in df_transformado.columns:
            fig_final_tasa = go.Figure(go.Indicator(
                mode = "number",
                value = df_transformado['tasa_suicidios'].mean(),
                title = {"text": "Tasa Promedio Final"},
                number = {'suffix': " por 100k"},
                domain = {'x': [0, 1], 'y': [0, 1]}
            ))
            fig_final_tasa.update_layout(height=200)
            st.plotly_chart(fig_final_tasa, use_container_width=True)
    
    with col3:
        if 'nivel_riesgo' in df_transformado.columns:
            alto_riesgo = (df_transformado['nivel_riesgo'] == 'Alto riesgo').sum()
            fig_alto_riesgo = go.Figure(go.Indicator(
                mode = "number",
                value = alto_riesgo,
                title = {"text": "Municipios Alto Riesgo"},
                domain = {'x': [0, 1], 'y': [0, 1]}
            ))
            fig_alto_riesgo.update_layout(height=200)
            st.plotly_chart(fig_alto_riesgo, use_container_width=True)
        
else:
    st.error("❌ No se pudieron cargar los datos para el proceso de limpieza")

st.markdown("---")
st.success("🎉 Proceso completado: Dataset listo para análisis avanzado")
st.caption("Página desarrollada por Ricardo (@ricardo778) - Procesamiento y transformación de datos")