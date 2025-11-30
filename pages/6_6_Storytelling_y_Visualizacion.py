# Asignado a Sebastián (@asebasg)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- IMPORTS DE MÓDULOS DEL EQUIPO ---
# Se necesita la función de Carga (Ricardo) y la de Cálculo de Tasas (Juan Esteban)
from src.etl import cargar_datos
from src.analytics import calcular_tasas

st.title("6️⃣ Comunicación de Resultados: Dashboard")

# 1. Cargar y Preparar Datos (Integrando el trabajo de Ricardo y Juan Esteban)
try:
    # Llama al módulo de Ricardo (Data Engineer)
    df_raw = cargar_datos()
    
    # Llama al módulo de Juan Esteban (Data Scientist)
    df_final = calcular_tasas(df_raw)
    
except Exception as e:
    # Si hay un error en src/etl.py o src/analytics.py
    st.error(f"⚠️ Error de Integración del Backend: {e}")
    st.info("Verifica que las funciones 'cargar_datos' y 'calcular_tasas' existan y usen la ruta correcta del CSV.")
    st.stop()


# --- BARRA LATERAL: FILTROS INTERACTIVOS ---
st.sidebar.header("Filtros del Dashboard")
anio_min, anio_max = int(df_final['Anio'].min()), int(df_final['Anio'].max())
rango_anio = st.sidebar.slider("Rango de Años:", anio_min, anio_max, (anio_min, anio_max))

regiones = ['Todas'] + list(df_final['NombreRegion'].unique())
region_sel = st.sidebar.selectbox("Filtrar por Región:", regiones)

# Aplicar Filtrado
df_filter = df_final[(df_final['Anio'] >= rango_anio[0]) & (df_final['Anio'] <= rango_anio[1])]
if region_sel != 'Todas':
    df_filter = df_filter[df_filter['NombreRegion'] == region_sel]


# --- STORYTELLING Y VISUALIZACIONES ---

st.header("Análisis de Riesgo vs. Casos Absolutos")
tab1, tab2, tab3 = st.tabs(["📈 Tendencia Temporal", "🗺️ Riesgo Regional (Tasas)", "⚖️ Correlación Población"])

# Pestaña 1: Tendencia Temporal
with tab1:
    st.subheader("Evolución de Casos de Suicidio (Total)")
    
    df_line = df_filter.groupby('Anio')['NumeroCasos'].sum().reset_index()
    
    # Gráfico de Línea
    fig_line = px.line(df_line, x='Anio', y='NumeroCasos', markers=True, 
                       title=f"Casos Totales {rango_anio[0]}-{rango_anio[1]}",
                       color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig_line, use_container_width=True)
    
    max_casos = df_line['NumeroCasos'].max()
    anio_pico = df_line.loc[df_line['NumeroCasos'].idxmax(), 'Anio']
    st.info(f"El pico histórico registrado en el período seleccionado fue en el año **{anio_pico}** con **{max_casos:,.0f} casos**.")

# Pestaña 2: Riesgo Regional (Usando Tasa - Métrica de Juan Esteban)
with tab2:
    st.subheader("Regiones y Municipios con Mayor Riesgo (Tasa por 100k hab)")
    
    # Resumen de Tasas por Región
    df_tasa_region = df_filter.groupby('NombreRegion', observed=True)['Tasa'].mean().reset_index()
    df_tasa_region = df_tasa_region.sort_values('Tasa', ascending=False)
    
    fig_bar = px.bar(df_tasa_region, x='Tasa', y='NombreRegion', orientation='h', 
                     title="Tasa Promedio de Suicidio por Región",
                     color='Tasa', color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Análisis: Top Municipios Absolutos vs Top Tasas (El gran insight)
    municipios_agrupados = df_filter.groupby('NombreMunicipio').agg(
        Casos_Totales=('NumeroCasos', 'sum'),
        Poblacion_Promedio=('NumeroPoblacionObjetivo', 'mean'),
        Tasa_Promedio=('Tasa', 'mean')
    ).reset_index()

    col_abs, col_tasa = st.columns(2)
    
    with col_abs:
        st.write("#### 🏆 Top 5: Casos Totales (Conteo Crudo)")
        top_abs = municipios_agrupados.sort_values('Casos_Totales', ascending=False).head(5)
        st.dataframe(top_abs[['NombreMunicipio', 'Casos_Totales']], hide_index=True, use_container_width=True)

    with col_tasa:
        st.write("#### 🚨 Top 5: Mayor Riesgo (Tasa Promedio)")
        top_tasa = municipios_agrupados.sort_values('Tasa_Promedio', ascending=False).head(5)
        st.dataframe(top_tasa[['NombreMunicipio', 'Tasa_Promedio']], hide_index=True, use_container_width=True)
        st.warning("El análisis basado en tasas (Trabajo de Juan Esteban) revela que los municipios de mayor riesgo **no son** necesariamente los de mayor conteo absoluto.")
        
# Pestaña 3: Correlación
with tab3:
    st.subheader("Correlación: Población vs Casos")
    
    # Scatter Plot
    fig_scatter = px.scatter(municipios_agrupados, 
                             x='Poblacion_Promedio', 
                             y='Casos_Totales', 
                             size='Tasa_Promedio', 
                             hover_name='NombreMunicipio',
                             title="Correlación entre Población y Casos Absolutos (Riesgo Relativo en Tamaño del Punto)")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Coeficiente de correlación (Métrica clave de Juan Esteban)
    correlacion = municipios_agrupados['Poblacion_Promedio'].corr(municipios_agrupados['Casos_Totales'])
    st.metric("Coeficiente de Correlación (r)", f"{correlacion:.4f}")
    st.caption("Un valor cercano a 1 indica una relación casi lineal: la población explica casi por completo el número *absoluto* de casos.")