"""
Página 6: Storytelling y Visualización
=======================================
Responsable: Sebastián (Líder)
Descripción: Narrativa visual que cuenta la historia detrás de los datos.
            7 hallazgos clave con visualizaciones impactantes.

ESTRUCTURA:
1. Introducción narrativa
2. Hallazgo 1: Crisis en crecimiento (tendencia temporal)
3. Hallazgo 2: Epicentro urbano (concentración Valle de Aburrá)
4. Hallazgo 3: Municipios pequeños en riesgo (tasas desproporcionadas)
5. Hallazgo 4: Correlación poblacional (dispersión)
6. Hallazgo 5: Evolución regional (líneas múltiples)
7. Hallazgo 6: Mapa de calor (patrones espaciotemporales)
8. Hallazgo 7: Top 10 municipios críticos (ranking)
9. Conclusiones y recomendaciones
"""

import streamlit as st
from utils import (
    cargar_datos,
    agrupar_por_anio,
    agrupar_por_region,
    obtener_ranking_municipios,
    identificar_municipios_alto_riesgo,
    calcular_correlacion,
    crear_grafico_tendencia,
    crear_grafico_barras_regiones,
    crear_ranking_horizontal,
    crear_grafico_dispersion,
    crear_grafico_lineas_multiples,
    crear_heatmap_region_anio
)
import pandas as pd

#  Configuración de la página
st.set_page_config(
    page_title="Storytelling y Visualización",
    page_icon="📢",
    layout="wide"
)

# Cargar datos
@st.cache_data
def cargar_datos_storytelling():
    """Carga y preprocesa todos los datos necesarios"""
    df = cargar_datos()
    df_anual = agrupar_por_anio(df)
    df_regional = agrupar_por_region(df)
    ranking = obtener_ranking_municipios(df, criterio='casos', top_n=10)
    municipios_riesgo = identificar_municipios_alto_riesgo(df, poblacion_max=20000, percentil_tasa=75)
    
    return df, df_anual, df_regional, ranking, municipios_riesgo

try:
    df, df_anual, df_regional, ranking, municipios_riesgo = cargar_datos_storytelling()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.stop()

#  Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; font-size: 2.8rem; margin: 0;'>
        📢 La Historia Detrás de los Números
    </h1>
    <p style='color: #e0e7ff; font-size: 1.2rem; margin-top: 0.5rem;'>
        7 Hallazgos Clave sobre el Suicidio en Antioquia (2005-2024)
    </p>
</div>
""", unsafe_allow_html=True)

#  Introducción narrativa
st.markdown("""
<div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f59e0b;'>
    <h3 style='margin-top: 0; color: #92400e;'>🎯 El Problema en Síntesis</h3>
    <p style='font-size: 1.1rem; line-height: 1.8;'>
        Durante 20 años, <strong>7,916 personas</strong> perdieron la vida por suicidio en Antioquia. 
        Detrás de esta cifra hay familias destruidas, comunidades afectadas y una crisis de salud 
        pública que no discrimina entre ciudades y pueblos. Este análisis revela patrones ocultos 
        que pueden guiar intervenciones efectivas.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  Hallazgo 1: Crísis en crecimiento
st.markdown("---")
st.markdown("""
## 📈 Hallazgo 1: Una Crisis en Aceleración Sostenida

<div style='background-color: #fee2e2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>🔴 Insight Crítico:</strong> Los casos de suicidio aumentaron un <strong>79%</strong> 
        entre 2005 y 2024, con una aceleración dramática en la última década.
    </p>
</div>
""", unsafe_allow_html=True)

# Gráfico de tendencia
fig_tendencia = crear_grafico_tendencia(
    df_anual,
    x='Anio',
    y='TotalCasos',
    titulo='Evolución de Casos de Suicidio en Antioquia (2005-2024)',
    etiqueta_y='Casos Anuales',
    mostrar_media=True
)
st.plotly_chart(fig_tendencia, use_container_width=True)

# Análisis en columnas
col1_h1, col2_h1, col3_h1 = st.columns(3)

with col1_h1:
    st.metric("2005-2014", "327 casos/año", delta=None, help="Promedio primera década")

with col2_h1:
    st.metric("2015-2019", "425 casos/año", delta="+30% vs. 2005-2014", delta_color="inverse")

with col3_h1:
    st.metric("2020-2024", "517 casos/año", delta="+58% vs. 2005-2014", delta_color="inverse")

st.markdown("""
**💡 Implicación:** La tendencia no es lineal. Existe una **aceleración crítica** después de 2015, 
con el pico histórico en 2023 (586 casos). Se requieren intervenciones urgentes para revertir esta curva.
""")

#  Hallazgo 2: Epicentro urbano
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 🏙️ Hallazgo 2: El Valle de Aburrá como Epicentro

<div style='background-color: #dbeafe; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>📍 Insight Geográfico:</strong> El 60% de todos los casos se concentran en el 
        Valle de Aburrá, con Medellín representando el <strong>40.3%</strong> del total departamental.
    </p>
</div>
""", unsafe_allow_html=True)

# Gráfico de barras regionales
fig_regional = crear_grafico_barras_regiones(
    df_regional,
    columna_region='NombreRegion',
    columna_valor='TotalCasos',
    titulo='Distribución de Casos por Región (2005-2024)',
    orientacion='horizontal'
)
st.plotly_chart(fig_regional, use_container_width=True)

# Tabla complementaria
st.markdown("### 📊 Top 5 Regiones: Datos Detallados")
df_top5_regiones = df_regional.head(5)[['NombreRegion', 'TotalCasos', 'PorcentajeCasos', 'TasaPor100k']].copy()
df_top5_regiones.columns = ['Región', 'Casos Históricos', '% del Total', 'Tasa por 100k hab.']
st.dataframe(df_top5_regiones, use_container_width=True, hide_index=True)

st.markdown("""
**💡 Implicación:** La concentración urbana sugiere factores de riesgo asociados a entornos 
metropolitanos (estrés urbano, aislamiento social, acceso a métodos). Sin embargo, las tasas 
por habitante revelan otra historia (ver Hallazgo 3).
""")

#  Hallazgo 3: Municipios pequeños en riesgo
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## ⚠️ Hallazgo 3: Municipios Pequeños con Tasas Desproporcionadas

<div style='background-color: #fef3c7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>🔎 Insight Oculto:</strong> Mientras grandes ciudades concentran casos absolutos, 
        municipios con menos de 20,000 habitantes presentan <strong>tasas por habitante superiores</strong> 
        al promedio departamental.
    </p>
</div>
""", unsafe_allow_html=True)

# Mostrar top municipios pequeños en riesgo
if not municipios_riesgo.empty:
    st.markdown("### 🚨 Top 10 Municipios Pequeños de Alto Riesgo")
    
    df_riesgo_display = municipios_riesgo.head(10).copy()
    df_riesgo_display['PoblacionPromedio'] = df_riesgo_display['PoblacionPromedio'].apply(lambda x: f"{int(x):,}")
    
    st.dataframe(
        df_riesgo_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "TasaPromedioPor100k": st.column_config.NumberColumn(
                "Tasa por 100k hab.",
                format="%.2f"
            )
        }
    )
    
    st.markdown("""
    **💡 Implicación:** Estos municipios, a pesar de su baja población, requieren atención 
    prioritaria. Factores como aislamiento geográfico, falta de servicios de salud mental y 
    limitada infraestructura de contención pueden explicar estas tasas elevadas.
    """)
else:
    st.warning("⚠️ No se encontraron municipios pequeños con tasas altas en este análisis.")

#  Hallazgo 4: Correlación poblacional
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 📊 Hallazgo 4: Relación Casi Perfecta entre Población y Casos

<div style='background-color: #dbeafe; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>📈 Insight Estadístico:</strong> Existe una correlación de <strong>r = 0.9973</strong> 
        entre población municipal y casos absolutos, sugiriendo que el riesgo aumenta proporcionalmente 
        con la densidad poblacional.
    </p>
</div>
""", unsafe_allow_html=True)

# Calcular correlación
correlacion = calcular_correlacion(df, 'NumeroPoblacionObjetivo', 'NumeroCasos', metodo='pearson')

# Gráfico de dispersión
fig_correlacion = crear_grafico_dispersion(
    df[df['NumeroCasos'] > 0],  # Filtrar ceros para mejor visualización
    x='NumeroPoblacionObjetivo',
    y='NumeroCasos',
    titulo='Correlación: Población Municipal vs. Casos de Suicidio',
    etiqueta_x='Población del Municipio',
    etiqueta_y='Casos Anuales',
    mostrar_tendencia=True
)
st.plotly_chart(fig_correlacion, use_container_width=True)

# Métricas de correlación
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
    }
    </style>
""", unsafe_allow_html=True)

col1_corr, col2_corr, col3_corr = st.columns(3)

with col1_corr:
    st.metric("Coeficiente de Pearson", f"{correlacion['coeficiente']:.4f}")

with col2_corr:
    st.metric("Interpretación", correlacion['interpretacion'])

with col3_corr:
    significancia = "✅ Significativo" if correlacion['significativo'] else "❌ No significativo"
    st.metric("Significancia estadística", significancia)

st.markdown("""
**💡 Implicación:** Aunque la correlación es fuerte, no implica causalidad directa. 
Municipios grandes tienen más casos en números absolutos, pero las **tasas ajustadas por 
población** revelan que el riesgo individual no es uniforme (ver Hallazgo 3).
""")

#  Hallazgo 5: Evolución regional
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 🌐 Hallazgo 5: Dinámicas Regionales Divergentes

<div style='background-color: #fef3c7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>🔄 Insight Temporal:</strong> No todas las regiones evolucionan igual. 
        Mientras el Valle de Aburrá muestra crecimiento sostenido, otras regiones presentan 
        patrones de estabilidad o fluctuación.
    </p>
</div>
""", unsafe_allow_html=True)

# Preparar datos para líneas múltiples (top 5 regiones)
top_regiones = df_regional.head(5)['NombreRegion'].tolist()
df_filtrado = df[df['NombreRegion'].isin(top_regiones)].copy()
df_evolucion_regional = df_filtrado.groupby(['Anio', 'NombreRegion'])['NumeroCasos'].sum().reset_index()

# Gráfico de líneas múltiples
fig_evolucion = crear_grafico_lineas_multiples(
    df_evolucion_regional,
    x='Anio',
    y='NumeroCasos',
    grupo='NombreRegion',
    titulo='Evolución de Casos por Región (Top 5)',
    etiqueta_y='Casos Anuales'
)
st.plotly_chart(fig_evolucion, use_container_width=True)

st.markdown("""
**💡 Implicación:** Las estrategias de prevención deben ser **contextualizadas regionalmente**. 
Lo que funciona en el Valle de Aburrá puede no ser efectivo en Urabá o el Bajo Cauca.
""")

#  Hallazgo 6: Mapa de calor
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 🗺️ Hallazgo 6: Patrones Espaciotemporales Visibles

<div style='background-color: #dbeafe; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>🔥 Insight Visual:</strong> El mapa de calor revela "puntos calientes" consistentes 
        en ciertas regiones a lo largo del tiempo, sugiriendo factores estructurales persistentes.
    </p>
</div>
""", unsafe_allow_html=True)

# Heatmap
fig_heatmap = crear_heatmap_region_anio(
    df,
    titulo='Mapa de Calor: Casos por Región y Año (2005-2024)'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("""
**💡 Implicación:** La persistencia de altos valores en ciertas regiones (Valle de Aburrá, Oriente) 
indica que existen **factores de riesgo estructurales** que no se han abordado adecuadamente en 
las últimas dos décadas.
""")

#  Hallazgo 7: TOP municipios críticos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 🚨 Hallazgo 7: Los 10 Municipios que Concentran la Crisis

<div style='background-color: #fee2e2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='font-size: 1.05rem; margin: 0;'>
        <strong>🎯 Insight Accionable:</strong> Solo 10 municipios concentran el <strong>65%</strong> 
        de todos los casos históricos. Medellín lidera con 3,191 casos (40.3% del total).
    </p>
</div>
""", unsafe_allow_html=True)

# Ranking horizontal
fig_ranking = crear_ranking_horizontal(
    ranking,
    columna_etiqueta='Municipio',
    columna_valor='CasosHistóricos',
    titulo='Top 10 Municipios por Casos Históricos (2005-2024)',
    top_n=10,
    color_escala='Reds'
)
st.plotly_chart(fig_ranking, use_container_width=True)

# Tabla detallada
st.markdown("### 📋 Detalles del Top 10")
df_ranking_display = ranking.head(10).copy()
st.dataframe(df_ranking_display, use_container_width=True, hide_index=True)

st.markdown("""
**💡 Implicación:** Una estrategia focalizada en estos 10 municipios podría impactar 
significativamente las cifras departamentales. Se requiere asignación prioritaria de recursos 
de salud mental en estas zonas.
""")

#  Conclusiones y recomendaciones
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
## 💡 Conclusiones Finales

<div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem; border-radius: 10px;'>
    <h3 style='color: white; margin-top: 0;'>Síntesis de Hallazgos</h3>
    <ol style='font-size: 1.05rem; line-height: 1.8;'>
        <li><strong>Crisis en aceleración:</strong> +79% en 20 años, con aceleración post-2015</li>
        <li><strong>Concentración urbana extrema:</strong> Valle de Aburrá = 60% de casos</li>
        <li><strong>Municipios pequeños vulnerables:</strong> Tasas desproporcionadas en poblaciones < 20k</li>
        <li><strong>Correlación poblacional:</strong> r=0.9973 (población vs. casos absolutos)</li>
        <li><strong>Dinámicas regionales diferentes:</strong> Cada región requiere estrategia específica</li>
        <li><strong>Puntos calientes persistentes:</strong> Factores estructurales no resueltos</li>
        <li><strong>Focalización posible:</strong> 10 municipios = 65% de casos</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recomendaciones en columnas
st.markdown("### 🎯 Recomendaciones Basadas en Evidencia")

rec1, rec2 = st.columns(2)

with rec1:
    st.markdown("""
    **🏥 Para Autoridades de Salud:**
    
    1. **Priorizar Valle de Aburrá:** Asignar 60% de recursos de prevención proporcional a casos
    
    2. **Atención urgente a municipios pequeños:** Diseñar programas específicos para poblaciones < 20k 
       con tasas altas
    
    3. **Estrategias regionalizadas:** No aplicar "receta única"; adaptar intervenciones por región
    
    4. **Fortalecimiento urbano:** Medellín requiere infraestructura robusta de salud mental
    """)

with rec2:
    st.markdown("""
    **📊 Para Futuras Investigaciones:**
    
    1. **Análisis causal:** Identificar factores de riesgo específicos que explican las tendencias
    
    2. **Segmentación por edad/género:** Profundizar en grupos demográficos más vulnerables
    
    3. **Evaluación de intervenciones:** Medir impacto de programas actuales de prevención
    
    4. **Modelos predictivos:** Desarrollar alertas tempranas para municipios en riesgo emergente
    """)

#  Llamado a la acción
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f59e0b; text-align: center;'>
    <h3 style='margin-top: 0; color: #92400e;'>🚨 Llamado a la Acción</h3>
    <p style='font-size: 1.1rem; line-height: 1.7;'>
        Los datos muestran una crisis de salud pública que requiere <strong>acción inmediata</strong>. 
        Cada número representa una vida perdida y una comunidad afectada. Este análisis proporciona 
        la base para <strong>decisiones informadas</strong> que pueden salvar vidas.
    </p>
    <p style='font-size: 1rem; color: #92400e; margin-bottom: 0;'>
        <strong>El conocimiento sin acción es complicidad. Es momento de actuar.</strong>
    </p>
</div>
""", unsafe_allow_html=True)

#  Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 6 de 7</strong> | Siguiente: 🤖 IA Generativa (Opcional)</p>
    <p style='font-size: 0.95rem; margin-top: 3rem;'>
        Este análisis se basa en datos oficiales de la Secretaría de Salud y Protección Social <br>
            del departamento de Antioquia, Colombia; comprendido entre los años 2005 y 2024 (20 años).
    </p>
</div>
""", unsafe_allow_html=True)