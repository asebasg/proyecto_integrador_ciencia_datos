import streamlit as st
import pandas as pd
import plotly.express as px
from src.etl import cargar_datos
from src.analytics import calcular_tasas

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Observatorio de Salud Mental - Antioquia",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARGA DE DATOS ---
try:
    df_raw = cargar_datos()
    df_final = calcular_tasas(df_raw)
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("Navegación")
opcion = st.sidebar.radio(
    "Ir a:",
    ["🏠 Inicio & Contexto", "📂 Diccionario de Datos", "📊 Dashboard Interactivo"]
)

# --- SECCIÓN 1: INICIO Y CONTEXTO (Basado en README.md) ---
if opcion == "🏠 Inicio & Contexto":
    st.title("🧠 Informe de Análisis: Suicidios en Antioquia (2005-2024)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Descripción General
        Este proyecto analiza los registros oficiales de casos de suicidio en **125 municipios** de Antioquia 
        durante las últimas dos décadas. El objetivo es identificar patrones geográficos, temporales y 
        poblacionales para apoyar la toma de decisiones en salud pública.
        
        * **Fuente:** Secretaría de Salud y Protección Social de Antioquia.
        * **Periodo:** 2005 - 2024.
        * **Registros:** +2,500 datos anuales por municipio.
        """)
    
    with col2:
        st.info("💡 **Dato Clave:** El análisis revela una crisis concentrada en el Valle de Aburrá, pero tasas alarmantes en municipios pequeños.")

    st.divider()

    st.subheader("❓ Preguntas Clave del Negocio")
    st.markdown("Selecciona una pregunta para ver el hallazgo del análisis:")
    
    # Interactividad para las preguntas del README
    preguntas = {
        "¿Qué regiones requieren intervención prioritaria?": "✅ **SÍ.** El Valle de Aburrá representa el 60% de los casos, requiriendo atención inmediata.",
        "¿Es posible predecir la tendencia futura?": "⚠️ **PARCIALMENTE.** Se identifican tendencias históricas claras (aumento del 79%), pero faltan variables exógenas para un modelo predictivo robusto.",
        "¿Existen tasas altas en municipios pequeños?": "✅ **SÍ.** Al normalizar por población, municipios con menos de 10,000 habitantes muestran tasas superiores al promedio nacional.",
        "¿Existe correlación entre población y casos?": "✅ **SÍ.** Correlación casi perfecta (r=0.997), lo cual es esperado en términos absolutos, pero engañoso para medir riesgo real."
    }
    
    selected_q = st.selectbox("Explorar Hallazgos:", list(preguntas.keys()))
    st.success(preguntas[selected_q])

# --- SECCIÓN 2: DICCIONARIO DE DATOS (Basado en README.md) ---
elif opcion == "📂 Diccionario de Datos":
    st.title("📂 Estructura del Dataset")
    st.markdown("A continuación se detallan las variables utilizadas en el análisis tras la limpieza de datos.")
    
    # Recreamos la tabla del README de forma visual
    datos_dict = [
        {"Variable": "NombreMunicipio", "Tipo": "Texto", "Descripción": "Nombre oficial del municipio"},
        {"Variable": "CodigoMunicipio", "Tipo": "Numérico", "Descripción": "Código DANE único"},
        {"Variable": "NombreRegion", "Tipo": "Categórica", "Descripción": "9 subregiones de Antioquia"},
        {"Variable": "Anio", "Tipo": "Numérico", "Descripción": "Año del registro (2005-2024)"},
        {"Variable": "NumeroCasos", "Tipo": "Numérico", "Descripción": "Cantidad absoluta de suicidios"},
        {"Variable": "NumeroPoblacionObjetivo", "Tipo": "Numérico", "Descripción": "Población total del municipio"},
        {"Variable": "Tasa (Calculada)", "Tipo": "Numérico", "Descripción": "Casos por cada 100,000 habitantes"},
    ]
    st.table(pd.DataFrame(datos_dict))
    
    with st.expander("Ver Muestra del Dataset (Primeras 5 filas)"):
        st.dataframe(df_final.head())

# --- SECCIÓN 3: DASHBOARD INTERACTIVO ---
elif opcion == "📊 Dashboard Interactivo":
    st.title("📊 Tablero de Control")
    
    # Filtros Globales
    st.sidebar.divider()
    st.sidebar.header("Filtros")
    anio_min, anio_max = int(df_final['Anio'].min()), int(df_final['Anio'].max())
    rango_anio = st.sidebar.slider("Rango de Años", anio_min, anio_max, (anio_min, anio_max))
    
    regiones = ['Todas'] + list(df_final['NombreRegion'].unique())
    region_sel = st.sidebar.selectbox("Región", regiones)
    
    # Filtrado
    df_filter = df_final[(df_final['Anio'] >= rango_anio[0]) & (df_final['Anio'] <= rango_anio[1])]
    if region_sel != 'Todas':
        df_filter = df_filter[df_filter['NombreRegion'] == region_sel]
        
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Casos", f"{df_filter['NumeroCasos'].sum():,.0f}")
    col2.metric("Tasa Promedio (x100k)", f"{df_filter['Tasa'].mean():.2f}")
    col3.metric("Municipio Más Crítico", df_filter.loc[df_filter['Tasa'].idxmax()]['NombreMunicipio'])
    
    # Gráficos
    tab1, tab2 = st.tabs(["📈 Tendencia Temporal", "🗺️ Análisis Regional"])
    
    with tab1:
        st.subheader("Evolución de Casos por Año")
        df_line = df_filter.groupby('Anio')[['NumeroCasos']].sum().reset_index()
        fig_line = px.line(df_line, x='Anio', y='NumeroCasos', markers=True, title="Tendencia Histórica")
        st.plotly_chart(fig_line, use_container_width=True)
        
    with tab2:
        st.subheader("Comparativa por Región/Municipio")
        if region_sel == 'Todas':
            df_bar = df_filter.groupby('NombreRegion', observed=True)['NumeroCasos'].sum().reset_index().sort_values('NumeroCasos', ascending=False)
            fig_bar = px.bar(df_bar, x='NombreRegion', y='NumeroCasos', color='NumeroCasos', title="Casos Totales por Región")
        else:
            # Si hay filtro de región, mostramos Top 10 municipios de esa región
            df_bar = df_filter.groupby('NombreMunicipio')['NumeroCasos'].sum().reset_index().sort_values('NumeroCasos', ascending=False).head(10)
            fig_bar = px.bar(df_bar, x='NumeroCasos', y='NombreMunicipio', orientation='h', title=f"Top 10 Municipios en {region_sel}")
            
        st.plotly_chart(fig_bar, use_container_width=True)