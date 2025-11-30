import streamlit as st
from utils.data_loader import load_data
from utils.preprocessing import preprocess
from utils.visualizations import plot_time_series

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Suicidios en Antioquia (2005–2024)",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📊 Análisis de Suicidios en Antioquia (2005–2024)")
st.markdown(
    """
    Este panel presenta un resumen ejecutivo del análisis realizado sobre los casos de suicidio 
    en el departamento de **Antioquia, Colombia**, en el periodo **2005–2024**.

    La información aquí mostrada permite explorar tendencias temporales, patrones regionales y 
    variaciones en la tasa por cada 100.000 habitantes.
    """
)

# Carga y procesamiento de datos
df = load_data("static/datasets/suicidios-en-antioquia.csv")
df = preprocess(df)

# Filtros interactivos y sidebar
st.sidebar.header("Filtros de exploración")

year_min, year_max = int(df["Año"].min()), int(df["Año"].max())
year_range = st.sidebar.slider(
    "Selecciona el rango de años:",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

regions = st.sidebar.multiselect(
    "Regiones:",
    options=df["region"].unique(),
    default=df["region"].unique()
)

show_rate = st.sidebar.checkbox(
    "Mostrar tasa por cada 100k habitantes",
    value=True
)

# Aplicar filtros
dff = df[
    (df["Año"].between(*year_range)) &
    (df["region"].isin(regions))
]

# KPIs – Indicadores claves
st.subheader("📌 Indicadores principales")

col1, col2, col3 = st.columns(3)

total_cases = int(dff["Casos"].sum())
avg_rate = round(dff["tasa_100k"].mean(), 2)
peak_year = int(df.groupby("Año")["Casos"].sum().idxmax())

col1.metric("Casos en el rango seleccionado", total_cases)
col2.metric("Tasa promedio (por 100k hab.)", avg_rate)
col3.metric("Año con mayor cantidad de casos", peak_year)

# Gráfico principal - Serie de tiempo
st.subheader("📈 Tendencia histórica de casos")

fig = plot_time_series(dff, show_rate)
st.plotly_chart(fig, use_container_width=True)

# Notas éticas
with st.expander("⚠️ Nota ética y metodológica"):
    st.markdown(
        """
        El análisis de casos de suicidio es un tema sensible.  
        Este panel muestra información agregada sin datos personales.

        Si necesitas ayuda o conoces a alguien que podría necesitar apoyo:  
        **Línea 106 (Atención en Salud Mental – Colombia)**  
        **Línea 123 Social – Medellín**
        """
    )
