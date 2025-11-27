import pandas as pd
import streamlit as st 
import plotly.express as px 

# La ruta del nuevo archivo
RUTA_DATASET = 'static/datasets/suicidios-en-antioquia.csv'

# Tarea 1: Asegurar que st.cache_data esté implementado para optimizar la carga.
@st.cache_data
def cargar_y_validar_datos(ruta_archivo):
    """
    Carga el DataFrame de Antioquia, realiza validaciones (nulos y duplicados) 
    y reporta los resultados con gráficas.
    """
    
    # --- Carga de Datos y manejo de errores ---
    try:
        # Tarea 1: Modularización (Cargar datos en una función)
        df = pd.read_csv(ruta_archivo)
    except FileNotFoundError as e:
        st.error(f"Error al cargar el archivo: Verifica la ruta '{e.filename}'.")
        return None 

    # --- Tarea 2: Implementar Validaciones con Gráficas de Barras ---
    
    # --- 2.1 Validación de Calidad: Valores Nulos ---
    st.subheader("📊 Validación de Calidad: Valores Nulos")
    
    nulos_totales = df.isnull().sum().sum()
    
    if nulos_totales > 0:
        # Crea DataFrame para Plotly que muestra las columnas con nulos
        df_nulos = df.isnull().sum().reset_index()
        df_nulos.columns = ['Columna', 'Nulos']
        df_nulos = df_nulos[df_nulos['Nulos'] > 0]
        
        fig_nulos = px.bar(
            df_nulos, 
            x='Columna', 
            y='Nulos', 
            title=f'Valores Nulos por Columna ({nulos_totales} en total)',
            color='Columna',
            color_discrete_sequence=['#FF6347'] 
        )
        st.plotly_chart(fig_nulos, use_container_width=True) 
        st.warning("Se detectaron NULOS. Verifique la consola (terminal) para detalles por columna.")
        print("\n--- Nulos detectados en el dataset ---")
        print(df.isnull().sum()[df.isnull().sum() > 0])
    else:
        st.success("No se encontraron valores nulos.")

    # --- 2.2 Validación de Calidad: Registros Duplicados ---
    st.subheader("📊 Validación de Calidad: Registros Duplicados")
    
    duplicados = df.duplicated().sum()
    
    if duplicados > 0:
        # Gráfica de barras simple para mostrar el total de duplicados
        df_dup = pd.DataFrame({'Tipo': ['Duplicados'], 'Conteo': [duplicados]})
        fig_dup = px.bar(df_dup, x='Tipo', y='Conteo', title='Total de Registros Duplicados')
        st.plotly_chart(fig_dup, use_container_width=True)
        st.error(f"Se encontraron {duplicados} registros duplicados.")
    else:
        st.success("No se encontraron registros duplicados.")

    return df

# --- LLAMADA A LA FUNCIÓN ---
df_antioquia = cargar_y_validar_datos(RUTA_DATASET)

# --- CUERPO DE LA APLICACIÓN STREAMLIT ---
st.title("Proyecto Integrador de Ciencia de Datos")

st.markdown("""
# 💻 Portada del Proyecto
*Aquí va el contenido real de la portada del proyecto.*
""")

# Visualización Rápida de Datos Cargados (EN GRÁFICAS)
st.markdown("## 📊 Datos Cargados (Verificación Visual)")

if df_antioquia is not None:
    # Ejemplo de Visualización: Conteo por Municipio
    # AJUSTA 'Municipio' por el nombre de columna categórica clave en tu archivo
    if 'Municipio' in df_antioquia.columns:
        st.subheader("Conteo por Municipio (Top 10)")
        df_conteo = df_antioquia['Municipio'].value_counts().nlargest(10).reset_index()
        df_conteo.columns = ['Municipio', 'Conteo']
        
        fig_municipio = px.bar(
            df_conteo, 
            x='Municipio', 
            y='Conteo', 
            title='Top 10 Municipios con más Registros'
        )
        st.plotly_chart(fig_municipio, use_container_width=True)
        
    # Primeras Filas (Para referencia)
    st.markdown("### Primeras Filas (Verificación en Tabla)")
    st.caption(f"Primeras 5 filas del dataset de Antioquia ({df_antioquia.shape[0]} registros)")
    st.dataframe(df_antioquia.head())