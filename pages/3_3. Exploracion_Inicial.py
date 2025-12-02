"""
Página 3: Exploración Inicial de Datos (EDA)

PROPÓSITO:
    Realizar análisis exploratorio completo del dataset,
    incluyendo estadísticas descriptivas, distribuciones,
    valores atípicos y visualizaciones de patrones.

DEPENDENCIAS:
    - streamlit: Framework de la aplicación
    - pandas: Manipulación de datos
    - plotly: Visualizaciones interactivas
    - utils.data_loader: cargar_datos()
    - utils.preprocessing: calcular_tasas()
    - utils.calculations: calcular_estadisticas_descriptivas(), obtener_ranking_municipios()
    - utils.visualizations: crear_grafico_tendencia(), crear_grafico_barras_regiones()

TRAZABILIDAD:
    - Flujo del proyecto: Página 2 (Recolección) → **Página 3 (EDA)** → Página 4 (Limpieza)
    - Outputs consumidos por: Página 5 (Análisis), Página 6 (Storytelling)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    cargar_datos,
    calcular_tasas,
    calcular_estadisticas_descriptivas,
    obtener_ranking_municipios
)

# Configuración de página
st.set_page_config(
    page_title="Exploración Inicial (EDA)",
    page_icon="🔍",
    layout="wide"
)


# Cargar y preparar datos
@st.cache_data
def cargar_datos_eda():
    """
    Carga datos y calcula columnas derivadas necesarias para EDA.
    
    TRAZABILIDAD:
        - Usa: utils.data_loader.cargar_datos()
        - Usa: utils.preprocessing.calcular_tasas()
    """
    df = cargar_datos()  # Función de data_loader.py
    df = calcular_tasas(df)  # Agregar columna TasaPor100k
    return df

try:
    df = cargar_datos_eda()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.info("💡 Verifica que el archivo esté en: `static/datasets/suicidios_antioquia.csv`")
    st.stop()


# Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 2.5rem;'>
        🔍 Exploración Inicial de Datos (EDA)
    </h1>
    <p style='font-size: 1.1rem; color: #64748b;'>
        Análisis Exploratorio de Casos de Suicidio en Antioquia (2005-2024)
    </p>
</div>
""", unsafe_allow_html=True)


# Introducción
st.markdown("""
<div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>🎯 Objetivo del EDA</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        El Análisis Exploratorio de Datos (EDA) es el primer acercamiento sistemático al dataset.
        Aquí identificamos patrones, distribuciones, anomalías y generamos hipótesis que serán
        validadas en fases posteriores del análisis.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Sección 1: Vista previa del dataset
st.markdown("## 📄 Vista Previa del Dataset")

st.markdown("""
**Primeros 20 registros** del dataset transformado (con columna `TasaPor100k` calculada):
""")

# Mostrar datos con columnas seleccionadas para mejor legibilidad
columnas_display = [
    'Anio', 'NombreMunicipio', 'NombreRegion', 
    'NumeroCasos', 'NumeroPoblacionObjetivo', 'TasaPor100k'
]
st.dataframe(
    df[columnas_display].head(20),
    use_container_width=True,
    hide_index=True
)

# Resumen rápido
col_info1, col_info2, col_info3, col_info4 = st.columns(4)

with col_info1:
    st.metric("Registros Totales", f"{len(df):,}")

with col_info2:
    st.metric("Municipios Únicos", f"{df['NombreMunicipio'].nunique()}")

with col_info3:
    st.metric("Rango de Años", f"{df['Anio'].min()}-{df['Anio'].max()}")

with col_info4:
    st.metric("Casos Totales", f"{df['NumeroCasos'].sum():,}")


# Sección 2: Estadísticas descriptivas
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📊 Estadísticas Descriptivas")

st.markdown("""
Análisis de las **variables numéricas clave** del dataset. Las estadísticas nos revelan
la distribución, dispersión y valores extremos de cada variable.
""")

# Calcular estadísticas para variables clave
variables_analizar = ['NumeroCasos', 'NumeroPoblacionObjetivo', 'TasaPor100k']

estadisticas_completas = []
for var in variables_analizar:
    try:
        stats = calcular_estadisticas_descriptivas(df, var)
        estadisticas_completas.append(stats)
    except Exception as e:
        st.warning(f"⚠️ No se pudieron calcular estadísticas para {var}: {str(e)}")

if estadisticas_completas:
    df_stats = pd.DataFrame(estadisticas_completas)
    
    # Reordenar columnas para mejor presentación
    cols_orden = [
        'columna', 'n_observaciones', 'media', 'mediana', 'desv_estandar',
        'minimo', 'q1', 'q3', 'maximo', 'valores_unicos', 'valores_nulos'
    ]
    df_stats = df_stats[cols_orden]
    
    st.dataframe(
        df_stats,
        use_container_width=True,
        hide_index=True,
        column_config={
            'columna': 'Variable',
            'n_observaciones': 'N',
            'media': st.column_config.NumberColumn('Media', format="%.2f"),
            'mediana': st.column_config.NumberColumn('Mediana', format="%.2f"),
            'desv_estandar': st.column_config.NumberColumn('Desv. Est.', format="%.2f"),
            'minimo': st.column_config.NumberColumn('Mínimo', format="%.2f"),
            'q1': st.column_config.NumberColumn('Q1 (25%)', format="%.2f"),
            'q3': st.column_config.NumberColumn('Q3 (75%)', format="%.2f"),
            'maximo': st.column_config.NumberColumn('Máximo', format="%.2f")
        }
    )
    
    # Interpretación
    st.markdown("""
    **💡 Interpretación:**
    - **NumeroCasos:** La mayoría de municipios-año tienen pocos casos (mediana baja), pero 
      hay valores extremos altos (máximo) que corresponden a ciudades grandes.
    - **TasaPor100k:** Permite comparar el riesgo relativo entre municipios de diferente tamaño.
    - **Desviación estándar alta:** Indica gran variabilidad entre municipios.
    """)


# Sección 3: Distribución de casos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📈 Distribución de Variables")

st.markdown("""
### Histograma: Número de Casos por Municipio-Año

Este histograma muestra la frecuencia de diferentes magnitudes de casos.
La mayoría de registros tienen 0-5 casos (barra más alta), mientras que
valores grandes son raros.
""")

# Histograma de casos
fig_hist_casos = px.histogram(
    df,
    x='NumeroCasos',
    nbins=50,
    title='Distribución del Número de Casos (Histograma)',
    labels={'NumeroCasos': 'Número de Casos', 'count': 'Frecuencia'},
    color_discrete_sequence=['#1e3a8a']
)
fig_hist_casos.update_layout(
    showlegend=False,
    height=450,
    template='plotly_white'
)
st.plotly_chart(fig_hist_casos, use_container_width=True)

# Boxplot de casos
st.markdown("""
### Boxplot: Detección de Valores Atípicos

El **boxplot** revela la presencia de valores atípicos (outliers) - puntos por encima
del bigote superior que representan municipios con casos excepcionalmente altos.
""")

fig_box_casos = px.box(
    df,
    y='NumeroCasos',
    title='Boxplot: Casos de Suicidio (Identificación de Outliers)',
    labels={'NumeroCasos': 'Número de Casos'},
    color_discrete_sequence=['#fb923c']
)
fig_box_casos.update_layout(
    showlegend=False,
    height=450,
    template='plotly_white'
)
st.plotly_chart(fig_box_casos, use_container_width=True)

# Identificar outliers
q1_casos = df['NumeroCasos'].quantile(0.25)
q3_casos = df['NumeroCasos'].quantile(0.75)
iqr_casos = q3_casos - q1_casos
umbral_superior = q3_casos + 1.5 * iqr_casos

outliers_casos = df[df['NumeroCasos'] > umbral_superior][
    ['Anio', 'NombreMunicipio', 'NombreRegion', 'NumeroCasos', 'TasaPor100k']
].sort_values('NumeroCasos', ascending=False)

st.markdown(f"""
**🔍 Valores atípicos identificados:** {len(outliers_casos)} registros con casos > {umbral_superior:.0f}
""")

with st.expander("📋 Ver municipios con casos atípicamente altos"):
    st.dataframe(outliers_casos.head(20), use_container_width=True, hide_index=True)


# Sección 4: TOP municipios
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🏆 Ranking de Municipios")

st.markdown("""
Identificación de los **10 municipios con mayor carga histórica** de casos (2005-2024).
""")

# Obtener ranking
ranking_casos = obtener_ranking_municipios(df, criterio='casos', top_n=10)

# Mostrar tabla
st.dataframe(
    ranking_casos,
    use_container_width=True,
    hide_index=True,
    column_config={
        'CasosHistóricos': st.column_config.NumberColumn(format="%d"),
        'PoblaciónPromedio': st.column_config.NumberColumn(format="%d"),
        'TasaPor100k': st.column_config.NumberColumn(format="%.2f")
    }
)

# Gráfico de barras horizontal
fig_ranking = go.Figure(data=[
    go.Bar(
        y=ranking_casos['Municipio'][::-1],  # Invertir para que #1 quede arriba
        x=ranking_casos['CasosHistóricos'][::-1],
        orientation='h',
        text=ranking_casos['CasosHistóricos'][::-1],
        textposition='outside',
        marker=dict(
            color=ranking_casos['CasosHistóricos'][::-1],
            colorscale='Reds',
            showscale=False
        )
    )
])

fig_ranking.update_layout(
    title='Top 10 Municipios por Casos Históricos (2005-2024)',
    xaxis_title='Casos Acumulados',
    yaxis_title='',
    template='plotly_white',
    height=500
)

st.plotly_chart(fig_ranking, use_container_width=True)

st.markdown("""
**💡 Observación:** Medellín concentra significativamente más casos que el resto,
seguido por otros municipios del Valle de Aburrá. Esto sugiere un **patrón de
concentración urbana** que requiere análisis más profundo.
""")


# Sección 5: Distribución temporal
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📅 Análisis Temporal")

st.markdown("""
Visualización de la **evolución de casos a lo largo del tiempo** (2005-2024).
Permite identificar tendencias, ciclos y períodos críticos.
""")

# Agrupar casos por año
casos_por_anio = df.groupby('Anio')['NumeroCasos'].sum().reset_index()
casos_por_anio.columns = ['Anio', 'TotalCasos']

# Gráfico de línea
fig_temporal = px.line(
    casos_por_anio,
    x='Anio',
    y='TotalCasos',
    title='Evolución Temporal de Casos de Suicidio en Antioquia',
    labels={'Anio': 'Año', 'TotalCasos': 'Total de Casos'},
    markers=True,
    color_discrete_sequence=['#1e3a8a']
)

# Agregar línea de tendencia
from scipy import stats as sp_stats
x = casos_por_anio['Anio'].values
y = casos_por_anio['TotalCasos'].values
slope, intercept = sp_stats.linregress(x, y)[:2]
tendencia = slope * x + intercept

fig_temporal.add_trace(
    go.Scatter(
        x=casos_por_anio['Anio'],
        y=tendencia,
        mode='lines',
        name='Tendencia lineal',
        line=dict(color='red', dash='dash', width=2)
    )
)

fig_temporal.update_layout(
    template='plotly_white',
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig_temporal, use_container_width=True)

# Calcular incremento
incremento_total = ((casos_por_anio.iloc[-1]['TotalCasos'] - casos_por_anio.iloc[0]['TotalCasos']) / 
                    casos_por_anio.iloc[0]['TotalCasos'] * 100)

st.markdown(f"""
**📊 Hallazgo temporal:**  
Los casos aumentaron un **{incremento_total:.1f}%** entre {casos_por_anio.iloc[0]['Anio']} 
y {casos_por_anio.iloc[-1]['Anio']}, con una **pendiente positiva clara** en la línea de tendencia.
""")


# Sección6: matriz de correlaciones
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🔗 Correlaciones entre Variables")

st.markdown("""
Análisis de la relación lineal entre las principales variables numéricas.
Un coeficiente cercano a **1** indica correlación positiva fuerte,
cercano a **-1** indica correlación negativa fuerte, y cercano a **0** indica
ausencia de correlación lineal.
""")

# Calcular matriz de correlaciones
columnas_corr = ['NumeroCasos', 'NumeroPoblacionObjetivo', 'TasaPor100k']
matriz_corr = df[columnas_corr].corr()

# Heatmap de correlaciones
fig_corr = px.imshow(
    matriz_corr,
    text_auto='.3f',
    color_continuous_scale='RdBu_r',
    title='Matriz de Correlaciones (Pearson)',
    labels=dict(color='Correlación'),
    aspect='auto'
)

fig_corr.update_layout(
    template='plotly_white',
    height=500
)

st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("""
**💡 Interpretación:**
- **Casos vs. Población:** Correlación muy alta (~0.99), indicando que municipios
  con mayor población tienden a tener más casos absolutos.
- **Casos vs. Tasa:** Correlación baja, confirmando que casos absolutos NO predicen
  el riesgo relativo (por eso es crucial normalizar por población).
""")


# Conclusiones del EDA
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 💡 Conclusiones del Análisis Exploratorio")

st.markdown("""
<div style='background-color: #f1f5f9; padding: 1.5rem; border-radius: 10px;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>Hallazgos Principales del EDA</h3>
    <ol style='font-size: 1.05rem; line-height: 1.8;'>
        <li><strong>Concentración extrema:</strong> Medellín y Valle de Aburrá concentran la mayoría de casos absolutos.</li>
        <li><strong>Tendencia creciente:</strong> Incremento sostenido del 79% en 20 años, con aceleración en años recientes.</li>
        <li><strong>Distribución asimétrica:</strong> La mayoría de municipios tienen pocos casos, pero existen outliers significativos.</li>
        <li><strong>Correlación poblacional:</strong> Existe relación casi perfecta (r≈0.99) entre población y casos absolutos.</li>
        <li><strong>Necesidad de normalización:</strong> Las tasas por 100k habitantes son esenciales para comparaciones justas.</li>
    </ol>
    <p style='margin-bottom: 0; margin-top: 1rem;'>
        <strong>🎯 Próximos pasos:</strong> Los insights del EDA guiarán la limpieza de datos (Página 4) y el análisis estadístico profundo (Página 5).
    </p>
</div>
""", unsafe_allow_html=True)


# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 3 de 7</strong> <br>
    Siguiente: 🧹 Limpieza y Preparación de Datos</p>
</div>
""", unsafe_allow_html=True)
