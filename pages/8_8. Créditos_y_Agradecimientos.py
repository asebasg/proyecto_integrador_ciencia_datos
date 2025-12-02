"""
Página dedicada a los créditos y el desarrollo de la aplicación
"""

import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Créditos y Agradecimientos",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Hero section
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 3rem; margin-bottom: 0;'>
        ❤️ Créditos y Agradecimientos
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #f1f5f9; padding: 1.5rem; margin-bottom: 2rem; border-radius: 10px; border: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>Créditos por el desarrollo</h3>
    <ul>
        <li><strong>Andrés Sebastián Ospina Guzmán</strong>: Líder del Proyecto & Frontend</li>
        <li><strong>Juan Esteban García Arboleda</strong>: Data Scientist & Análisis</li>
        <li><strong>Ricardo Andrés Vega Pérez</strong>: Data Engineer & Backend</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: justify; padding: 1rem 2rem;'>
    En este proyecto nos acercamos, con respeto y humildad, a una realidad dolorosa: el suicidio.
    Más que números, cada registro representa una vida, una familia y una comunidad impactada.
    Agradecemos a quienes compartieron datos, conocimientos y tiempo; su apoyo nos permitió transformar cifras en reflexión y empatía. 
    Ojalá este trabajo inspire conversaciones más humanas, decisiones más sabias y acciones concretas para cuidar la vida en nuestro territorio.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 1rem; margin-top: 2rem;'>
    <p>© 2025 Análisis de Suicidios en Antioquia. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)