import streamlit as st
from PIL import Image

# Configuración de página
st.set_page_config(
    page_title="Observatorio Salud Mental Antioquia",
    page_icon="🧠",
    layout="wide"
)

# Título y Bienvenida
st.title("🧠 Observatorio de Salud Mental: Antioquia (2005-2024)")
st.markdown("### Proyecto Integrador de Ciencia de Datos")

col1, col2 = st.columns([1, 2])

with col1:
    # Puedes subir una imagen alusiva a la carpeta static/img/
    # st.image("static/img/logo_salud.png") 
    st.info("""
    **Equipo de Trabajo:**
    * **Sebastián** (Líder / Analytics Engineer)
    * **Juan Esteban** (Data Scientist)
    * **Ricardo** (Data Engineer)
    
    **Grupo:** Datos-3
    """)

with col2:
    st.markdown("""
    Bienvenidos al sistema de análisis de datos sobre la incidencia de suicidios en el departamento de Antioquia.
    
    Este proyecto busca responder preguntas críticas como:
    * ¿Qué regiones requieren intervención prioritaria?
    * ¿Existe una correlación entre el tamaño poblacional y la tasa de suicidios?
    * ¿Qué municipios pequeños presentan alertas tempranas?
    
    👈 **Navega por el menú lateral** para ver cada etapa del proceso de Ciencia de Datos.
    """)
    
    st.warning("Estado del Proyecto: 🟡 En desarrollo...")