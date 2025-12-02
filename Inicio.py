"""
Inicio.py - Portada del Proyecto
=================================
Responsable: Sebastián (Líder)
Descripción: Página principal de la aplicación Streamlit.
            Muestra resumen ejecutivo, métricas clave y contexto del problema.

ESTRUCTURA:
1. Hero Section (título + contexto)
2. Métricas Clave (KPIs visuales)
3. Resumen Ejecutivo (hallazgos principales)
4. Visualización Principal (tendencia temporal)
5. Distribución Regional (gráfico de dona)
6. Navegación (guía a las páginas)
"""

import streamlit as st
import pandas as pd
from utils import (
    cargar_datos,
    obtener_metadatos,
    agrupar_por_anio,
    agrupar_por_region,
    crear_grafico_tendencia,
    crear_grafico_pie
)

#  Configuracion de pagina
st.set_page_config(
    page_title="Análisis de Suicidios en Antioquia",
    page_icon="📊",
    layout="wide",  # Usar ancho completo
    initial_sidebar_state="expanded"
)

#  Cargar datos (con cache automatico)
@st.cache_data
def cargar_datos_procesados():
    """
    Carga y preprocesa todos los datos necesarios para la portada.
    El decorador @st.cache_data hace que esto se ejecute UNA SOLA VEZ.
    """
    df = cargar_datos()
    metadatos = obtener_metadatos(df)
    df_anual = agrupar_por_anio(df)
    df_regional = agrupar_por_region(df)
    
    return df, metadatos, df_anual, df_regional


# Cargar datos
try:
    df, metadatos, df_anual, df_regional = cargar_datos_procesados()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.info("💡 Verifica que el archivo CSV esté en: `static/datasets/suicidios_antioquia.csv`")
    st.stop()

#  1. Hero section
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 3rem; margin-bottom: 0;'>
        📊 Análisis de Suicidios en Antioquia
    </h1>
    <p style='font-size: 1.3rem; color: #64748b; margin-top: 0.5rem;'>
        Estudio epidemiológico
    </p>
    <p style='font-size: 0.9rem; color: #64748b;'>
        Un análisis que comprende desde los años 2005 - 2024
    </p>
</div>
""", unsafe_allow_html=True)

# Contexto del problema
st.markdown("""
<div style='background-color: #f1f5f9; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>🎯 Contexto del Problema</h3>
    <p style='font-size: 1.1rem; line-height: 1.6;'>
        El suicidio representa una <strong>crisis de salud pública</strong> en Colombia. 
        Antioquia, con 125 municipios distribuidos en 9 regiones, presenta patrones 
        complejos que requieren análisis basado en datos para diseñar intervenciones 
        efectivas en salud mental.
    </p>
    <p style='font-size: 1rem; color: #64748b; margin-bottom: 0;'>
        <strong>Fuente:</strong> Secretaría de Salud y Protección Social de Antioquia | 
        <strong>Período:</strong> 2005-2024 (20 años) | 
        <strong>Registros totales:</strong> {total_registros:,}
    </p>
</div>
""".format(total_registros=metadatos['total_registros']), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  Metricas clave
st.markdown("### 📈 Indicadores Clave")

# Calcular métricas adicionales
casos_2024 = df_anual[df_anual['Anio'] == 2024]['TotalCasos'].values[0] if 2024 in df_anual['Anio'].values else 0
casos_2005 = df_anual[df_anual['Anio'] == 2005]['TotalCasos'].values[0]
incremento_total = ((casos_2024 - casos_2005) / casos_2005 * 100) if casos_2005 > 0 else 0

# Calcular tasa promedio reciente (últimos 5 años)
df_reciente = df_anual[df_anual['Anio'] >= 2020]
tasa_promedio_reciente = df_reciente['TasaPor100k'].mean()

# Mostrar métricas en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total de Casos Históricos",
        value=f"{metadatos['total_casos']:,}",
        delta=None,
        help="Suma total de casos registrados entre 2005 y 2024"
    )

with col2:
    st.metric(
        label="📅 Casos en 2024",
        value=f"{casos_2024:,}",
        delta=f"{incremento_total:+.1f}% vs. 2005",
        delta_color="inverse",
        help="Incremento comparado con el año base 2005"
    )

with col3:
    st.metric(
        label="🌍 Municipios Afectados",
        value=f"{metadatos['total_municipios']}",
        delta=None,
        help="De 125 municipios totales en Antioquia"
    )

with col4:
    st.metric(
        label="📈 Tasa Promedio 2020-2024",
        value=f"{tasa_promedio_reciente:.2f}",
        delta="por 100k hab.",
        delta_color="off",
        help="Tasa de suicidio por cada 100,000 habitantes"
    )

st.markdown("<br>", unsafe_allow_html=True)

#  Resumen ejecutivo
st.markdown("### 🔍 Hallazgos Principales")

# Crear tres columnas para hallazgos
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
    <div style='background-color: #fef3c7; padding: 1rem; border-radius: 8px; height: 180px;'>
        <h4 style='color: #92400e; margin-top: 0;'>⚠️ Tendencia Creciente</h4>
        <p style='font-size: 0.95rem;'>
            Los casos aumentaron <strong>79%</strong> en 20 años, 
            pasando de un promedio de 327 casos/año (2005-2014) 
            a 517 casos/año (2020-2024).
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div style='background-color: #fee2e2; padding: 1rem; border-radius: 8px; height: 180px;'>
        <h4 style='color: #991b1b; margin-top: 0;'>🏙️ Concentración Urbana</h4>
        <p style='font-size: 0.95rem;'>
            El <strong>Valle de Aburrá</strong> concentra el 59.8% 
            de todos los casos, con Medellín representando el 40.3% 
            del total departamental.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div style='background-color: #dbeafe; padding: 1rem; border-radius: 8px; height: 180px;'>
        <h4 style='color: #1e3a8a; margin-top: 0;'>📊 Correlación Poblacional</h4>
        <p style='font-size: 0.95rem;'>
            Existe una correlación de <strong>r=0.9973</strong> 
            entre población y casos absolutos, indicando que 
            municipios grandes concentran más casos.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  4. Visualizacion principal (tendencia temporal)
st.markdown("### 📈 Evolución Temporal de Casos (2005-2024)")

# Crear gráfico de tendencia
fig_tendencia = crear_grafico_tendencia(
    df_anual,
    x='Anio',
    y='TotalCasos',
    titulo='',  # Título ya está en Markdown arriba
    etiqueta_y='Número de Casos',
    mostrar_media=True
)

# Mostrar gráfico
st.plotly_chart(fig_tendencia, use_container_width=True)

# Análisis debajo del gráfico
st.markdown("""
<div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px;'>
    <p style='margin: 0; font-size: 0.95rem;'>
        <strong>📊 Análisis:</strong> Se observan tres períodos distintos: 
        (1) <strong>2005-2014</strong>: estabilidad relativa con promedio de 327 casos/año, 
        (2) <strong>2015-2019</strong>: incremento sostenido hasta 425 casos/año, y 
        (3) <strong>2020-2024</strong>: aceleración crítica alcanzando 517 casos/año, 
        con un pico histórico de <strong>586 casos en 2023</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  5. Distribucion regional
st.markdown("### 🗺️ Distribución Regional de Casos")

# Crear dos columnas: gráfico y tabla
col_grafico, col_tabla = st.columns([2, 1])

with col_grafico:
    # Gráfico de dona
    fig_regional = crear_grafico_pie(
        df_regional,
        columna_categoria='NombreRegion',
        columna_valor='TotalCasos',
        # titulo='',  # Título se define en visualizations.py
        tipo='dona'
    )
    st.plotly_chart(fig_regional, use_container_width=True)

with col_tabla:
    st.markdown("**📊 Top 5 Regiones**")
    
    # Preparar tabla
    df_top5 = df_regional.head(5)[['NombreRegion', 'TotalCasos', 'PorcentajeCasos']].copy()
    df_top5.columns = ['Región', 'Casos', '%']
    
    # Formatear
    df_top5['Casos'] = df_top5['Casos'].apply(lambda x: f"{x:,}")
    df_top5['%'] = df_top5['%'].apply(lambda x: f"{x:.1f}%")
    
    # Mostrar tabla
    st.dataframe(
        df_top5,
        hide_index=True,
        use_container_width=True
    )
    
    # Insight
    st.markdown("""
    <div style='background-color: #fef3c7; padding: 0.8rem; border-radius: 6px; margin-top: 1rem;'>
        <p style='margin: 0; font-size: 0.85rem;'>
            <strong>⚠️ Importante:</strong> Las 3 regiones principales 
            (Valle de Aburrá, Oriente y Suroeste) concentran el 
            <strong>78.9%</strong> de todos los casos.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  6. Navegación y estructura del proyecto
st.markdown("---")
st.markdown("### 🧭 Navegación del Proyecto")

st.markdown("""
Este proyecto sigue una metodología estructurada de ciencia de datos. 
Explora cada sección en el menú lateral (☰) para profundizar en el análisis:
""")

# Crear tabla de navegación en dos columnas
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    st.markdown("""
    **📋 Fase 1: Definición**
    - `1. Definición y Objetivos` - Contexto del problema y objetivos SMART
    
    **📊 Fase 2: Datos**
    - `2. Recolección de Datos` - Fuentes y calidad de datos
    - `3. Exploración Inicial` - EDA y estadísticas descriptivas
    - `4. Limpieza y Preparación` - Transformaciones aplicadas
    """)

with col_nav2:
    st.markdown("""
    **📈 Fase 3: Análisis**
    - `5. Análisis y Hallazgos` - Insights estadísticos profundos
    - `6. Storytelling y Visualización` - Narrativa visual con hallazgos clave
    
    **🤖 Fase 4: IA (Opcional)**
    - `7. IA Generativa` - Chatbot interactivo con Gemini
    """)

#  7. Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Footer con información del equipo
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **👥 Equipo de Trabajo**
    - Sebastián (Líder - Frontend)
    - Ricardo (Data Engineer)
    - Juan (Data Scientist)
    """)

with footer_col2:
    st.markdown("""
    **📅 Información del Proyecto**
    - Período: 2005-2024 (20 años)
    - Registros: 2,500
    - Municipios: 125
    - Regiones: 9
    """)

with footer_col3:
    st.markdown("""
    **🔗 Recursos**
    - [Documentación](https://github.com/asebasg/proyecto_integrador_ciencia_datos/blob/main/Informe_de_Analisis_Suicidios_en_Antioquia.md)
    - [GitHub](https://github.com/asebasg/proyecto_integrador_ciencia_datos.git)
    - [Secretaría de Salud](https://dssa.gov.co/)
    """)

st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 2rem;'>
    <strong>⚠️ Este análisis tiene fines académicos. Para intervenciones de salud pública, 
    consulte fuentes oficiales y profesionales especializados.</strong>
    <p>Proyecto Integrador de Ciencia de Datos - 2025</p>
</div>
""", unsafe_allow_html=True)
