"""
Página 1: Definición del Problema y Objetivos
==============================================
Responsable: Sebastián (Líder)
Descripción: Establece el contexto del problema, justificación,
            objetivos SMART, alcance y stakeholders.

ESTRUCTURA:
1. Contexto y problemática
2. Justificación del proyecto
3. Objetivos SMART
4. Alcance del análisis
5. Stakeholders
6. Preguntas de investigación
"""

import streamlit as st

#  Configuración de la página
st.set_page_config(
    page_title="Definición y Objetivos",
    page_icon="📋",
    layout="wide"
)

#  Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 2.5rem;'>
        📋 Definición del Problema y Objetivos
    </h1>
    <p style='font-size: 1.1rem; color: #64748b;'>
        Marco conceptual del proyecto de análisis
    </p>
</div>
""", unsafe_allow_html=True)

#  1. Contexto y problemática

st.markdown("## 🌍 Contexto del Problema")

st.markdown("""
<div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f59e0b;'>
    <h3 style='margin-top: 0; color: #92400e;'>⚠️ Crisis de Salud Pública</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        El <strong>suicidio</strong> es una de las principales causas de muerte prevenible a nivel mundial. 
        Según la Organización Mundial de la Salud (OMS), cerca de <strong>700,000 personas</strong> 
        mueren por suicidio cada año, siendo la cuarta causa de muerte entre jóvenes de 15 a 29 años.
    </p>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        En <strong>Colombia</strong>, el fenómeno ha mostrado una tendencia creciente en las últimas 
        dos décadas, con Antioquia posicionándose como uno de los departamentos con mayor número 
        de casos registrados.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Problemática específica
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔴 Problemática en Antioquia
    
    Antioquia enfrenta desafíos particulares:
    
    - **Heterogeneidad territorial:** 125 municipios distribuidos en 9 regiones con 
      características sociodemográficas y económicas diversas
    
    - **Concentración urbana:** El Valle de Aburrá, especialmente Medellín, concentra 
      más del 60% de los casos, pero municipios rurales presentan tasas desproporcionadas
    
    - **Tendencia creciente:** Los datos oficiales muestran un incremento sostenido 
      del 79% en las últimas dos décadas (2005-2024)
    
    - **Subregistro:** Posible existencia de casos no reportados en zonas rurales 
      de difícil acceso
    """)

with col2:
    st.markdown("""
    ### ❓ Vacío de Conocimiento
    
    A pesar de la gravedad del problema, existen limitaciones:
    
    - **Análisis fragmentado:** Los estudios previos se enfocan en períodos cortos 
      o regiones específicas, sin visión integral
    
    - **Falta de identificación de patrones:** No existe claridad sobre qué municipios 
      pequeños presentan riesgo desproporcionado
    
    - **Ausencia de priorización:** Las autoridades carecen de herramientas basadas 
      en datos para asignar recursos de prevención
    
    - **Comunicación ineficaz:** Los hallazgos epidemiológicos no se traducen en 
      narrativas comprensibles para tomadores de decisión
    """)

#  2. Justificación del proyecto
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🎯 Justificación del Proyecto")

st.markdown("""
<div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>¿Por qué es necesario este análisis?</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        Este proyecto responde a la necesidad de <strong>analizar causas variables en las
        problemáticas de salud mental en el departamento</strong> para la toma de decisiones 
        en temas salud pública y prevención. Al analizar 20 años de registros (2005-2024) 
        de los 125 municipios de Antioquia, se busca:
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Beneficios en 3 columnas
ben1, ben2, ben3 = st.columns(3)

with ben1:
    st.markdown("""
    <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; height: 200px;'>
        <h4 style='color: #1e3a8a;'>📊 Evidencia Científica</h4>
        <p style='font-size: 0.95rem;'>
            Generar conocimiento basado en datos sobre patrones temporales, 
            geográficos y demográficos que permitan comprender mejor el fenómeno.
        </p>
    </div>
    """, unsafe_allow_html=True)

with ben2:
    st.markdown("""
    <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; height: 200px;'>
        <h4 style='color: #1e3a8a;'>🎯 Priorización Estratégica</h4>
        <p style='font-size: 0.95rem;'>
            Identificar municipios y regiones que requieren intervención prioritaria, 
            optimizando la asignación de recursos limitados.
        </p>
    </div>
    """, unsafe_allow_html=True)

with ben3:
    st.markdown("""
    <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; height: 200px;'>
        <h4 style='color: #1e3a8a;'>💡 Comunicación Efectiva</h4>
        <p style='font-size: 0.95rem;'>
            Traducir hallazgos complejos en narrativas visuales comprensibles 
            para autoridades de salud pública y comunidad académica.
        </p>
    </div>
    """, unsafe_allow_html=True)

#  3. Objetivos SMART
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🎯 Objetivos del Proyecto")

st.markdown("""
Los objetivos están formulados bajo la metodología **SMART** (Específicos, Medibles, 
Alcanzables, Relevantes y Temporales):
""")

st.markdown("<br>", unsafe_allow_html=True)

# Objetivo General
st.markdown("""
<div style='background-color: #1e3a8a; color: white; padding: 1.5rem; border-radius: 10px;'>
    <h3 style='margin-top: 0; color: white;'>🎯 Objetivo General</h3>
    <p style='font-size: 1.1rem; line-height: 1.7; margin-bottom: 0;'>
        Realizar un análisis epidemiológico integral de los casos de suicidio en Antioquia 
        durante el período 2005-2024, identificando patrones espaciotemporales, grupos de 
        alto riesgo y tendencias evolutivas, con el fin de generar recomendaciones basadas 
        en evidencia para la formulación de políticas públicas de prevención en salud mental.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Objetivos Específicos
st.markdown("### 📌 Objetivos Específicos")

objetivos = [
    {
        "num": "1",
        "titulo": "Caracterizar la tendencia temporal",
        "descripcion": "Analizar la evolución de casos de suicidio entre 2005 y 2024, identificando períodos críticos de incremento y calculando tasas de crecimiento por quinquenio.",
        "medible": "Tasa de crecimiento porcentual, identificación de años pico",
        "plazo": "Análisis completado al 100%"
    },
    {
        "num": "2",
        "titulo": "Identificar concentración geográfica",
        "descripcion": "Determinar qué regiones y municipios concentran el mayor número absoluto de casos, calculando su porcentaje de participación sobre el total departamental.",
        "medible": "Top 10 municipios, distribución porcentual por región",
        "plazo": "Mapa de concentración generado"
    },
    {
        "num": "3",
        "titulo": "Detectar municipios de alto riesgo",
        "descripcion": "Identificar municipios pequeños (población < 20,000 habitantes) que presenten tasas de suicidio superiores al promedio departamental, representando focos de atención prioritaria.",
        "medible": "Listado de municipios con tasa > percentil 75",
        "plazo": "Ranking de riesgo calculado"
    },
    {
        "num": "4",
        "titulo": "Analizar correlaciones clave",
        "descripcion": "Cuantificar la relación estadística entre tamaño poblacional y número de casos, así como entre variables sociodemográficas disponibles.",
        "medible": "Coeficiente de correlación de Pearson (esperado r > 0.9)",
        "plazo": "Análisis correlacional finalizado"
    },
    {
        "num": "5",
        "titulo": "Desarrollar dashboard interactivo",
        "descripcion": "Construir una aplicación web con Streamlit que permita explorar los datos de forma visual e interactiva, facilitando la comunicación de hallazgos a stakeholders.",
        "medible": "Aplicación funcional con 7 secciones navegables",
        "plazo": "Deploy completado en 48 horas"
    }
]

for obj in objetivos:
    with st.expander(f"**Objetivo {obj['num']}:** {obj['titulo']}", expanded=False):
        st.markdown(f"""
        **📝 Descripción:**  
        {obj['descripcion']}
        
        **📊 Indicador Medible:**  
        {obj['medible']}
        
        **⏰ Plazo:**  
        {obj['plazo']}
        """)

#  4. Alcance de análisis
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🔬 Alcance del Análisis")

alcance_col1, alcance_col2 = st.columns(2)

with alcance_col1:
    st.markdown("""
    ### ✅ Dentro del Alcance
    
    Este proyecto **SÍ incluye:**
    
    - ✔️ Análisis de datos oficiales de la Secretaría de Salud de Antioquia
    - ✔️ Período temporal: 2005-2024 (20 años completos)
    - ✔️ Cobertura geográfica: 125 municipios en 9 regiones
    - ✔️ Estadísticas descriptivas e inferenciales
    - ✔️ Visualizaciones interactivas y dashboards
    - ✔️ Identificación de patrones y tendencias
    - ✔️ Correlaciones entre variables disponibles
    - ✔️ Recomendaciones basadas en hallazgos
    """)

with alcance_col2:
    st.markdown("""
    ### ❌ Fuera del Alcance
    
    Este proyecto **NO incluye:**
    
    - ❌ Análisis causal de factores de riesgo individuales
    - ❌ Datos de intentos de suicidio (solo casos consumados)
    - ❌ Variables clínicas o psicológicas individuales
    - ❌ Comparación con otros departamentos o países
    - ❌ Modelos predictivos de casos futuros individuales
    - ❌ Análisis de métodos utilizados
    - ❌ Diseño de programas de intervención específicos
    - ❌ Validación en campo de hipótesis generadas
    """)

#  5. Stakeholders (partes interesadas)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 👥 Partes Interesadas del Análisis")

st.markdown("""
Este análisis es relevante para múltiples actores del ecosistema de salud pública:
""")

stakeholders_data = [
    {
        "actor": "🏛️ Secretaría de Salud de Antioquia",
        "interes": "Diseño de políticas públicas de prevención basadas en evidencia",
        "uso": "Priorización de recursos, identificación de zonas críticas"
    },
    {
        "actor": "🏥 Instituciones Prestadoras de Salud (IPS)",
        "interes": "Fortalecimiento de programas de salud mental",
        "uso": "Identificación de municipios para expandir servicios"
    },
    {
        "actor": "🎓 Academia e Investigadores",
        "interes": "Generación de conocimiento epidemiológico",
        "uso": "Base para investigaciones futuras, benchmark metodológico"
    },
    {
        "actor": "🏘️ Alcaldías Municipales",
        "interes": "Comprensión de problemática local",
        "uso": "Justificación de proyectos de intervención comunitaria"
    },
    {
        "actor": "📊 Organizaciones No Gubernamentales (ONGs)",
        "interes": "Focalización de programas de prevención",
        "uso": "Identificación de poblaciones vulnerables"
    }
]

for sh in stakeholders_data:
    st.markdown(f"""
    <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
        <h4 style='margin-top: 0; color: #1e3a8a;'>{sh['actor']}</h4>
        <p style='margin-bottom: 0.5rem;'><strong>Interés:</strong> {sh['interes']}</p>
        <p style='margin-bottom: 0;'><strong>Uso esperado:</strong> {sh['uso']}</p>
    </div>
    """, unsafe_allow_html=True)

#  6. Preguntas de investigación
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## ❓ Preguntas de Investigación")

st.markdown("""
El análisis busca responder las siguientes preguntas clave:
""")

preguntas = [
    "¿Cuál es la tendencia temporal de casos de suicidio en Antioquia entre 2005 y 2024?",
    "¿Qué regiones concentran el mayor número de casos y qué porcentaje representan del total?",
    "¿Existen municipios pequeños con tasas de suicidio desproporcionadamente altas?",
    "¿Cuál es la correlación entre tamaño poblacional y número absoluto de casos?",
    "¿Se pueden identificar períodos críticos de incremento acelerado?",
    "¿Qué municipios requieren intervención prioritaria según un índice de riesgo combinado?",
    "¿Cómo evolucionó la tasa por 100,000 habitantes a nivel departamental?"
]

for i, pregunta in enumerate(preguntas, 1):
    st.markdown(f"""
    <div style='background-color: #dbeafe; padding: 0.8rem; border-radius: 6px; margin-bottom: 0.5rem; border-left: 4px solid #1e3a8a;'>
        <p style='margin: 0; font-size: 1rem;'><strong>{i}.</strong> {pregunta}</p>
    </div>
    """, unsafe_allow_html=True)

#  7. Footer de metodología
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
### 🔬 Metodología del Proyecto

Este proyecto sigue el ciclo completo de ciencia de datos:

**1. Definición del problema** → **2. Recolección de datos** → **3. Exploración (EDA)** → 
**4. Limpieza y preparación** → **5. Análisis estadístico** → **6. Visualización y storytelling** → 
**7. Comunicación de resultados**

Navega por las siguientes secciones en el menú lateral para seguir el desarrollo del análisis.
""")

st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 2rem;'>
    <p><strong>Página 1 de 7</strong></p>
</div>
""", unsafe_allow_html=True)