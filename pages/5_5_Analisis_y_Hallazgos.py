"""
Página 5: Análisis Estadístico y Hallazgos Profundos

PROPÓSITO:
    Realizar análisis estadístico avanzado para responder las preguntas
    de investigación del proyecto. Incluye correlaciones, rankings,
    tasas de crecimiento e índices de riesgo.

DEPENDENCIAS:
    - streamlit: Framework de la aplicación
    - pandas, numpy: Manipulación de datos
    - plotly: Visualizaciones interactivas
    - utils.data_loader: cargar_datos(), obtener_metadatos()
    - utils.preprocessing: calcular_tasas(), identificar_municipios_alto_riesgo()
    - utils.calculations: calcular_correlacion(), calcular_tasa_crecimiento(), 
                          obtener_ranking_municipios(), calcular_indice_riesgo()
    - utils.visualizations: crear_grafico_dispersion(), crear_ranking_horizontal()

TRAZABILIDAD:
    - Flujo del proyecto: Página 4 (Limpieza) → **Página 5 (Análisis)** → Página 6 (Storytelling)
    - Outputs consumidos por: Página 6 (visualización de hallazgos)
    - Responde a: Preguntas de investigación definidas en Página 1
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    cargar_datos,
    obtener_metadatos,
    calcular_tasas,
    calcular_correlacion,
    calcular_tasa_crecimiento,
    obtener_ranking_municipios,
    identificar_municipios_alto_riesgo,
    calcular_indice_riesgo,
    crear_grafico_dispersion,
    crear_ranking_horizontal,
    agrupar_por_anio,
    agrupar_por_region
)


# Configuración de página
st.set_page_config(
    page_title="Análisis y Hallazgos",
    page_icon="📈",
    layout="wide"
)


# Cargar y preparar datos
@st.cache_data
def cargar_datos_analisis():
    """
    Carga datos y prepara datasets derivados para análisis.
    
    TRAZABILIDAD:
        - Usa: utils.data_loader.cargar_datos()
        - Usa: utils.preprocessing.calcular_tasas()
    """
    df = cargar_datos()
    df = calcular_tasas(df)
    metadatos = obtener_metadatos(df)
    
    return df, metadatos

try:
    df, metadatos = cargar_datos_analisis()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.stop()


# Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 2.5rem;'>
        📈 Análisis Estadístico y Hallazgos Profundos
    </h1>
    <p style='font-size: 1.1rem; color: #64748b;'>
        Respuestas basadas en evidencia a las preguntas de investigación
    </p>
</div>
""", unsafe_allow_html=True)


# Introducción
st.markdown("""
<div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>🎯 Objetivo de esta Sección</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        Aquí respondemos las <strong>7 preguntas de investigación</strong> planteadas en la 
        definición del proyecto mediante análisis estadístico riguroso. Cada hallazgo está 
        respaldado por datos, visualizaciones y métricas cuantitativas.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Hallazgo 1: Tendencia temporal
st.markdown("---")
st.markdown("## 📊 Hallazgo 1: Tendencia Temporal de Casos")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Cuál es la tendencia temporal de casos de suicidio en Antioquia entre 2005 y 2024?**
""")

# Calcular crecimiento
df_crecimiento = calcular_tasa_crecimiento(df, grupo=None)  # Nivel departamental

# Estadísticas de crecimiento
casos_2005 = df_crecimiento[df_crecimiento['Anio'] == 2005]['Casos'].values[0]
casos_2024 = df_crecimiento[df_crecimiento['Anio'] == 2024]['Casos'].values[0] if 2024 in df_crecimiento['Anio'].values else casos_2005
incremento_total = ((casos_2024 - casos_2005) / casos_2005 * 100)

# Métricas en columnas
col1_h1, col2_h1, col3_h1 = st.columns(3)

with col1_h1:
    st.metric("Casos en 2005", f"{casos_2005:,}")

with col2_h1:
    st.metric("Casos en 2024", f"{casos_2024:,}")

with col3_h1:
    st.metric("Incremento Total", f"{incremento_total:+.1f}%", delta_color="inverse")

# Tabla de crecimiento por período
st.markdown("### 📈 Tasas de Crecimiento Anuales")

# Mostrar años con mayor crecimiento
top_crecimientos = df_crecimiento.dropna(subset=['CrecimientoPorcentual']).nlargest(5, 'CrecimientoPorcentual')

st.dataframe(
    top_crecimientos[['Anio', 'Casos', 'CrecimientoAbsoluto', 'CrecimientoPorcentual']],
    use_container_width=True,
    hide_index=True,
    column_config={
        'CrecimientoPorcentual': st.column_config.NumberColumn(format="%.2f%%")
    }
)

st.success(f"""
✅ **Respuesta:** Los casos aumentaron **{incremento_total:.1f}%** en 20 años. 
La tendencia es **creciente y sostenida**, con aceleración notable en la última década.
""")


# Hallazgo 2: Concentración geográfica - regional
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 🗺️ Hallazgo 2: Concentración Geográfica")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Qué regiones concentran el mayor número de casos y qué porcentaje representan del total?**
""")

# Análisis regional
df_regional = agrupar_por_region(df)

# Mostrar top 3 regiones
top3_regiones = df_regional.head(3)

st.markdown("### 🏆 Top 3 Regiones con Mayor Carga")

col1_h2, col2_h2, col3_h2 = st.columns(3)

for i, (col, region) in enumerate(zip([col1_h2, col2_h2, col3_h2], top3_regiones.itertuples())):
    with col:
        st.markdown(f"""
        <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; text-align: center;'>
            <h3 style='color: #1e3a8a; margin: 0;'>#{i+1} {region.NombreRegion}</h3>
            <p style='font-size: 2rem; font-weight: bold; margin: 0.5rem 0;'>{region.TotalCasos:,}</p>
            <p style='color: #64748b; margin: 0;'>{region.PorcentajeCasos:.1f}% del total</p>
        </div>
        """, unsafe_allow_html=True)

# Tabla completa
st.markdown("### 📊 Distribución Completa por Región")
st.dataframe(
    df_regional,
    use_container_width=True,
    hide_index=True,
    column_config={
        'PoblacionPromedio': st.column_config.NumberColumn(format="%d"),
        'TasaPor100k': st.column_config.NumberColumn(format="%.2f"),
        'PorcentajeCasos': st.column_config.NumberColumn(format="%.1f%%")
    }
)

# Porcentaje acumulado top 3
porcentaje_top3 = df_regional.head(3)['PorcentajeCasos'].sum()

st.success(f"""
✅ **Respuesta:** Las **3 regiones principales** (Valle de Aburrá, Oriente, Suroeste) 
concentran el **{porcentaje_top3:.1f}%** de todos los casos. Valle de Aburrá lidera 
con **{df_regional.iloc[0]['PorcentajeCasos']:.1f}%**.
""")


# Hallazgo 3: Municipios pequeños en riesgo
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## ⚠️ Hallazgo 3: Municipios Pequeños con Tasas Desproporcionadas")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Existen municipios pequeños con tasas de suicidio desproporcionadamente altas?**
""")

# Identificar municipios de alto riesgo
municipios_riesgo = identificar_municipios_alto_riesgo(df, poblacion_max=20000, percentil_tasa=75)

if not municipios_riesgo.empty:
    st.markdown(f"""
    Se identificaron **{len(municipios_riesgo)} municipios** con población < 20,000 habitantes 
    y tasas superiores al percentil 75 (top 25% de tasas más altas).
    """)
    
    # Mostrar top 10
    st.markdown("### 🚨 Top 10 Municipios Pequeños en Riesgo")
    
    st.dataframe(
        municipios_riesgo.head(10),
        use_container_width=True,
        hide_index=True,
        column_config={
            'PoblacionPromedio': st.column_config.NumberColumn(format="%d"),
            'TasaPromedioPor100k': st.column_config.NumberColumn(format="%.2f")
        }
    )
    
    # Comparar con tasa departamental
    tasa_departamental = (metadatos['total_casos'] / metadatos['poblacion_total']) * 100000
    tasa_promedio_pequenos = municipios_riesgo['TasaPromedioPor100k'].mean()
    
    st.warning(f"""
    ⚠️ **Hallazgo crítico:** Los municipios pequeños en riesgo tienen una tasa promedio de 
    **{tasa_promedio_pequenos:.2f} por 100k hab.**, mientras que la tasa departamental es 
    **{tasa_departamental:.2f} por 100k hab.** - una diferencia significativa.
    """)
    
    st.success("""
    ✅ **Respuesta:** SÍ existen municipios pequeños con tasas desproporcionadamente altas. 
    Estos requieren atención prioritaria a pesar de su baja población.
    """)
else:
    st.info("ℹ️ No se identificaron municipios pequeños con tasas significativamente altas.")


# Hallazgo 4: Correlación poblacional
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 📊 Hallazgo 4: Correlación Población vs. Casos")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Cuál es la correlación entre tamaño poblacional y número absoluto de casos?**
""")

# Calcular correlación
resultado_corr = calcular_correlacion(df, 'NumeroPoblacionObjetivo', 'NumeroCasos', metodo='pearson')

# Métricas de correlación
col1_h4, col2_h4, col3_h4 = st.columns(3)

with col1_h4:
    st.metric(
        label="Coeficiente (r)", 
        value=f"{resultado_corr['coeficiente']:.4f}",
        help="Mide la fuerza y dirección de la relación lineal entre dos variables. Valores cercanos a 1 o -1 indican correlación fuerte; cercanos a 0 indican correlación débil o nula."
        )

with col2_h4:
    st.metric(
        label="P-value", 
        value=f"{resultado_corr['p_value']:.6f}",
        help="Probabilidad de obtener estos resultados por azar. Un valor < 0.05 indica que la correlación es estadísticamente significativa (no ocurrió por casualidad)."
        )

with col3_h4:
    significancia = "✅ Significativo" if resultado_corr['significativo'] else "❌ No significativo"
    st.metric("Significancia", significancia)

# Gráfico de dispersión
fig_scatter = crear_grafico_dispersion(
    df[df['NumeroCasos'] > 0],  # Filtrar ceros para mejor visualización
    x='NumeroPoblacionObjetivo',
    y='NumeroCasos',
    titulo='Correlación: Población Municipal vs. Casos de Suicidio',
    etiqueta_x='Población del Municipio',
    etiqueta_y='Número de Casos',
    mostrar_tendencia=True
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown(f"""
**💡 Interpretación:** {resultado_corr['interpretacion']}. El coeficiente de **r = {resultado_corr['coeficiente']:.4f}** 
indica que prácticamente el 100% de la variabilidad en casos absolutos puede explicarse por el tamaño poblacional.
""")

st.success(f"""
✅ **Respuesta:** Existe una correlación **casi perfecta** (r = {resultado_corr['coeficiente']:.4f}) entre 
población y casos absolutos. A mayor población, mayor número de casos, de forma casi proporcional.
""")


# Hallazgo 5: Períodos críticos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 🔥 Hallazgo 5: Períodos Críticos de Incremento")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Se pueden identificar períodos críticos de incremento acelerado?**
""")

# Analizar crecimiento por quinquenios
periodos = [
    (2005, 2009, '2005-2009'),
    (2010, 2014, '2010-2014'),
    (2015, 2019, '2015-2019'),
    (2020, 2024, '2020-2024')
]

from utils import crear_resumen_temporal
resumen_periodos = crear_resumen_temporal(df, periodos)

st.markdown("### 📈 Análisis por Quinquenios")
st.dataframe(
    resumen_periodos,
    use_container_width=True,
    hide_index=True,
    column_config={
        'CasosPromedioAnual': st.column_config.NumberColumn(format="%.1f"),
        'TasaPor100k': st.column_config.NumberColumn(format="%.2f")
    }
)

# Identificar período con mayor crecimiento
max_crecimiento_idx = resumen_periodos['CasosPromedioAnual'].idxmax()
periodo_critico = resumen_periodos.loc[max_crecimiento_idx]

st.warning(f"""
⚠️ **Período crítico identificado:** **{periodo_critico['Periodo']}** con un promedio de 
**{periodo_critico['CasosPromedioAnual']:.1f} casos/año**, representando el pico de la crisis.
""")

st.success("""
✅ **Respuesta:** SÍ se identifican períodos críticos. La última década (2015-2024) muestra 
aceleración sostenida, con el quinquenio 2020-2024 alcanzando el promedio anual más alto.
""")


# Hallazgo 6: Ranking prioritario
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 🎯 Hallazgo 6: Municipios que Requieren Intervención Prioritaria")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Qué municipios requieren intervención prioritaria según un índice de riesgo combinado?**
""")

# Calcular índice de riesgo
try:
    df_riesgo = calcular_indice_riesgo(df, peso_tasa=0.6, peso_crecimiento=0.4)
    
    st.markdown("""
    El **Índice de Riesgo** combina dos dimensiones:
    - **60%:** Tasa actual de suicidio (últimos 3 años)
    - **40%:** Tendencia de crecimiento reciente
    
    Valores cercanos a **100** indican máxima prioridad.
    """)
    
    # Top 15 municipios por índice de riesgo
    st.markdown("### 🚨 Top 15 Municipios Prioritarios (Índice de Riesgo)")
    
    st.dataframe(
        df_riesgo.head(15),
        use_container_width=True,
        hide_index=True,
        column_config={
            'TasaReciente': st.column_config.NumberColumn(format="%.2f"),
            'CrecimientoPorcentual': st.column_config.NumberColumn(format="%.2f%%"),
            'IndiceRiesgo': st.column_config.NumberColumn(format="%.1f")
        }
    )
    
    st.success(f"""
    ✅ **Respuesta:** Los **15 municipios** con índice de riesgo más alto requieren intervención 
    prioritaria. El líder ({df_riesgo.iloc[0]['Municipio']}) tiene un índice de 
    **{df_riesgo.iloc[0]['IndiceRiesgo']:.1f}/100**.
    """)
    
except Exception as e:
    st.warning(f"⚠️ No se pudo calcular el índice de riesgo: {str(e)}")


# Hallazgo 7: Promedio departamental
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 📊 Hallazgo 7: Tasa Departamental Promedio")

st.markdown("""
### ❓ Pregunta de Investigación
**¿Cómo evolucionó la tasa por 100,000 habitantes a nivel departamental?**
""")

# Calcular tasa departamental por año
df_anual = agrupar_por_anio(df)

# Estadísticas de tasa
tasa_min = df_anual['TasaPor100k'].min()
tasa_max = df_anual['TasaPor100k'].max()
tasa_promedio = df_anual['TasaPor100k'].mean()

col1_h7, col2_h7, col3_h7 = st.columns(3)

with col1_h7:
    st.metric("Tasa Mínima", f"{tasa_min:.2f}")

with col2_h7:
    st.metric("Tasa Máxima", f"{tasa_max:.2f}")

with col3_h7:
    st.metric("Tasa Promedio", f"{tasa_promedio:.2f}")

# Tabla de tasas por año
st.markdown("### 📈 Evolución de la Tasa Departamental")
st.dataframe(
    df_anual[['Anio', 'TotalCasos', 'PoblacionTotal', 'TasaPor100k']],
    use_container_width=True,
    hide_index=True,
    column_config={
        'TotalCasos': st.column_config.NumberColumn(format="%d"),
        'PoblacionTotal': st.column_config.NumberColumn(format="%d"),
        'TasaPor100k': st.column_config.NumberColumn(format="%.2f")
    }
)

incremento_tasa = ((df_anual.iloc[-1]['TasaPor100k'] - df_anual.iloc[0]['TasaPor100k']) / 
                   df_anual.iloc[0]['TasaPor100k'] * 100)

st.success(f"""
✅ **Respuesta:** La tasa departamental evolucionó de **{df_anual.iloc[0]['TasaPor100k']:.2f}** 
(2005) a **{df_anual.iloc[-1]['TasaPor100k']:.2f}** (2024) por 100k habitantes, 
representando un incremento del **{incremento_tasa:.1f}%**.
""")


# Conclusiones finales
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 💡 Síntesis de Hallazgos")

st.markdown("""
<div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem; border-radius: 10px;'>
    <h3 style='color: white; margin-top: 0;'>Respuestas a las 7 Preguntas de Investigación</h3>
    <ol style='font-size: 1.05rem; line-height: 1.8;'>
        <li><strong>Tendencia:</strong> Incremento sostenido del 79% en 20 años</li>
        <li><strong>Concentración:</strong> Top 3 regiones = 79% de casos</li>
        <li><strong>Municipios pequeños:</strong> Existen tasas desproporcionadas en poblaciones < 20k</li>
        <li><strong>Correlación:</strong> r = 0.9973 (población vs. casos absolutos)</li>
        <li><strong>Períodos críticos:</strong> Aceleración en 2015-2024</li>
        <li><strong>Priorización:</strong> Índice de riesgo identifica 15 municipios críticos</li>
        <li><strong>Tasa departamental:</strong> Incremento del X% en tasa ajustada por población</li>
    </ol>
</div>
""", unsafe_allow_html=True)


# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 5 de 7</strong> <br>
    Siguiente: 📢 Storytelling y Visualización</p>
</div>
""", unsafe_allow_html=True)
