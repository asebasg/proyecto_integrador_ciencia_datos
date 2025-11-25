import streamlit as st
import plotly.express as px
from src.etl import cargar_datos
from src.analytics import calcular_tasas

st.title("6️⃣ Comunicación de Resultados (Dashboard)")

# Cargar y Calcular
df = cargar_datos()
df_final = calcular_tasas(df)

# --- DASHBOARD ---
tab1, tab2, tab3 = st.tabs(["📈 Tendencias", "🗺️ Mapa Regional", "⚖️ Tasas vs Absolutos"])

with tab1:
    st.subheader("Evolución Histórica")
    df_anio = df_final.groupby('Anio')['NumeroCasos'].sum().reset_index()
    fig = px.line(df_anio, x='Anio', y='NumeroCasos', markers=True, color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Se evidencia un pico histórico reciente y una tendencia creciente desde 2015.")

with tab2:
    st.subheader("Análisis por Subregión")
    region_sel = st.selectbox("Filtrar Región:", ['Todas'] + list(df_final['NombreRegion'].unique()))
    
    if region_sel == 'Todas':
        df_view = df_final.groupby('NombreRegion', observed=True)['NumeroCasos'].sum().reset_index()
        fig = px.bar(df_view, x='NombreRegion', y='NumeroCasos', color='NumeroCasos')
    else:
        df_view = df_final[df_final['NombreRegion'] == region_sel].groupby('NombreMunicipio')['NumeroCasos'].sum().reset_index()
        fig = px.bar(df_view.sort_values('NumeroCasos', ascending=False).head(10), 
                     x='NumeroCasos', y='NombreMunicipio', orientation='h')
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("La Trampa de los Datos Absolutos")
    st.markdown("Comparativa: Municipios con más casos vs. Municipios con mayor tasa de riesgo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 5 Casos Totales (Absolutos)**")
        top_abs = df_final.groupby('NombreMunicipio')['NumeroCasos'].sum().nlargest(5)
        st.table(top_abs)
    
    with col2:
        st.write("**Top 5 Tasa de Riesgo (x 100k hab)**")
        # Calculamos tasa promedio histórica
        df_tasas = df_final.groupby('NombreMunicipio')[['NumeroCasos', 'NumeroPoblacionObjetivo']].sum()
        df_tasas['Tasa_Global'] = (df_tasas['NumeroCasos'] / df_tasas['NumeroPoblacionObjetivo']) * 100000
        st.table(df_tasas['Tasa_Global'].nlargest(5))