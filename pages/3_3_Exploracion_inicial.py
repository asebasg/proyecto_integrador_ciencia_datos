# Asignado a Juan Esteban (@Juanes-crypto)

import streamlit as st
import pandas as pd
import plotly.express as px
from src.etl import cargar_datos # Usamos tu módulo

st.title("3️⃣ Exploración Inicial (EDA)")

# Cargar datos usando tu función limpia
df = cargar_datos()

st.markdown("### 📊 Estadísticas Descriptivas")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total de Registros", len(df))
    st.metric("Municipios Cubiertos", df['NombreMunicipio'].nunique())

with col2:
    st.metric("Total de Casos (2005-2024)", f"{df['NumeroCasos'].sum():,.0f}")
    st.metric("Promedio Casos/Año", f"{df.groupby('Anio')['NumeroCasos'].sum().mean():.0f}")

st.markdown("### 🔍 Distribución de Variables")

# Histograma simple de casos
fig = px.histogram(df, x="NumeroCasos", nbins=50, title="Distribución de Casos por Registro Anual")
st.plotly_chart(fig)

st.write("Se observa una distribución sesgada a la derecha: la mayoría de municipios reportan 0 o pocos casos, mientras que unos pocos (Medellín, Bello) reportan cifras muy altas.")