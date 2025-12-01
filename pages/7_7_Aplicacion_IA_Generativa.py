# Asignado a Sebastián (@asebasg)

import streamlit as st

st.title("Aplicación IA Generativa (Gemini)")

st.markdown("""
Objetivo
- Usar Gemini en Streamlit para apoyar el análisis anterior.

Qué hará
- Q&A sobre datos y negocio.
- Sugerencias para EDA, limpieza y features.
- Explicación de métricas y resultados.
- Borradores de reportes y storytelling.

Prerrequisitos
- API Key de Gemini en `.streamlit/secrets.toml`.
- Respetar privacidad (no enviar PII).

Flujo
- Entrada: pregunta + contexto del proyecto.
- Proceso: prompt → Gemini.
- Salida: respuesta y acciones sugeridas.

Siguientes pasos
- Configurar secretos y cliente.
- Conectar UI (entrada, modo, botón) a la API.
- Mostrar respuestas y permitir iteración.
""")

st.info("Cuando avances, reemplaza estas indicaciones por la implementación correspondiente de esta etapa.")