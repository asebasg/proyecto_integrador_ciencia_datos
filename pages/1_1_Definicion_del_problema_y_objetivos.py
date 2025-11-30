# Asignado a: Sebastian (@asebasg)

import streamlit as st

st.title("1️⃣ Definición del Problema y Objetivos")

st.markdown("""
### 🚩 Contexto del Problema
La salud mental es un desafío creciente en Antioquia. Los datos históricos sugieren un incremento sostenido en los casos de suicidio, pero la asignación de recursos a menudo se basa en conteos absolutos (donde las grandes ciudades siempre "ganan") y no en tasas de riesgo real.

Se ha identificado una necesidad urgente de:
1. **Descentralizar el análisis:** Mirar más allá del Valle de Aburrá.
2. **Normalizar métricas:** Evaluar el riesgo relativo (tasa x 100k hab).
3. **Identificar patrones:** Temporales y geográficos.

### 🎯 Objetivos del Proyecto

#### Objetivo General
Desarrollar un sistema de inteligencia de datos que permita a la Secretaría de Salud identificar **focos de riesgo** en los 125 municipios de Antioquia.

#### Objetivos Específicos
* **Analizar** la tendencia temporal de los últimos 20 años.
* **Detectar** municipios pequeños (<10k hab) con tasas desproporcionadamente altas.
* **Correlacionar** variables demográficas con la incidencia de casos.
* **Visualizar** los hallazgos en un dashboard interactivo para la toma de decisiones.
""")