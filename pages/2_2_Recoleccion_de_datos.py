"""
Página 2: Recolección de Datos

Responsable: Ricardo (Data Engineer)
Descripción: Documenta la fuente de datos, metadatos,
            proceso de recolección y calidad de datos.
"""

import streamlit as st
from utils import cargar_datos, obtener_metadatos, verificar_duplicados
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="Recolección de Datos",
    page_icon="📊",
    layout="wide"
)


# Carga de datos
try:
    df = cargar_datos()
    metadatos = obtener_metadatos(df)
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.stop()


# Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 2.5rem;'>
        📊 Recolección de Datos
    </h1>
    <p style='font-size: 1.1rem; color: #64748b;'>
        Fuentes, metadatos y proceso de obtención de información
    </p>
</div>
""", unsafe_allow_html=True)


# 1. Fuente de datos
st.markdown("## 🗂️ Fuente de Datos")

st.markdown("""
<div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>Secretaría de Salud y Protección Social de Antioquia</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        Los datos utilizados en este análisis provienen de registros oficiales de la 
        <strong>Secretaría de Salud y Protección Social del Departamento de Antioquia</strong>, 
        entidad responsable de la vigilancia epidemiológica y reporte de casos de mortalidad 
        por causas externas en el departamento.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Información de la fuente en columnas
col_fuente1, col_fuente2 = st.columns(2)

with col_fuente1:
    st.markdown("""
    ### 📋 Características de la Fuente
    
    - **Entidad:** Secretaría de Salud de Antioquia
    - **Tipo:** Datos administrativos (registros oficiales)
    - **Sistema:** Sistema de Vigilancia Epidemiológica
    - **Cobertura:** 125 municipios de Antioquia
    - **Actualización:** Registro continuo, consolidación anual
    - **Formato original:** CSV (Comma-Separated Values)
    """)

with col_fuente2:
    st.markdown("""
    ### ✅ Criterios de Calidad
    
    - **Integridad:** Datos completos para todos los municipios
    - **Consistencia:** Validación por códigos DANE
    - **Actualidad:** Incluye datos hasta 2024
    - **Trazabilidad:** Cada registro vinculado a municipio específico
    - **Confiabilidad:** Fuente gubernamental oficial
    - **Accesibilidad:** Datos de dominio público
    """)


# 2. Metadatos del dataset
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📈 Metadatos del Dataset")

# Mostrar métricas principales en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total de Registros",
        value=f"{metadatos['total_registros']:,}",
        help="Número total de filas en el dataset"
    )

with col2:
    st.metric(
        label="🏘️ Municipios",
        value=f"{metadatos['total_municipios']}",
        help="Municipios únicos registrados"
    )

with col3:
    st.metric(
        label="🗺️ Regiones",
        value=f"{metadatos['total_regiones']}",
        help="Regiones de Antioquia cubiertas"
    )

with col4:
    st.metric(
        label="📅 Años Cubiertos",
        value=f"{metadatos['anio_fin'] - metadatos['anio_inicio'] + 1}",
        help=f"Desde {metadatos['anio_inicio']} hasta {metadatos['anio_fin']}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Métricas adicionales en 3 columnas
col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        label="🔢 Total de Casos Históricos",
        value=f"{metadatos['total_casos']:,}",
        help="Suma de casos 2005-2024"
    )

with col6:
    st.metric(
        label="📊 Promedio Anual",
        value=f"{metadatos['casos_promedio_anual']:.1f}",
        help="Casos promedio por año"
    )

with col7:
    st.metric(
        label="💾 Memoria Utilizada",
        value=f"{metadatos['memoria_mb']:.2f} MB",
        help="Tamaño del dataset en memoria"
    )


# 3. Diccionario de datos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📋 Diccionario de Datos")

st.markdown("""
Descripción detallada de cada columna del dataset:
""")

# Información de columnas
columnas_info = {
    'NombreMunicipio': {
        'tipo': 'Texto (Categórica)',
        'descripcion': 'Nombre oficial del municipio de Antioquia',
        'ejemplo': 'Medellín, Envigado, Rionegro',
        'valores_unicos': df['NombreMunicipio'].nunique()
    },
    'CodigoMunicipio': {
        'tipo': 'Entero (int32)',
        'descripcion': 'Código DANE del municipio (identificador único nacional)',
        'ejemplo': '05001, 05266, 05615',
        'valores_unicos': df['CodigoMunicipio'].nunique()
    },
    'Ubicacion': {
        'tipo': 'Texto (Coordenadas)',
        'descripcion': 'Coordenadas geográficas en formato POINT(longitud, latitud)',
        'ejemplo': 'POINT(-75.5636 6.2442)',
        'valores_unicos': 'Variable'
    },
    'NombreRegion': {
        'tipo': 'Texto (Categórica)',
        'descripcion': 'Región de Antioquia a la que pertenece el municipio',
        'ejemplo': 'Valle de Aburrá, Oriente, Suroeste',
        'valores_unicos': df['NombreRegion'].nunique()
    },
    'CodigoRegion': {
        'tipo': 'Entero (int8)',
        'descripcion': 'Código numérico de la región (1-9)',
        'ejemplo': '1, 2, 3, ..., 9',
        'valores_unicos': df['CodigoRegion'].nunique()
    },
    'Anio': {
        'tipo': 'Entero (int16)',
        'descripcion': 'Año del registro',
        'ejemplo': '2005, 2010, 2024',
        'valores_unicos': f"{metadatos['anio_inicio']}-{metadatos['anio_fin']}"
    },
    'CausaMortalidad': {
        'tipo': 'Texto (Categórica)',
        'descripcion': 'Causa de mortalidad (siempre "Suicidios" en este dataset)',
        'ejemplo': 'Suicidios',
        'valores_unicos': df['CausaMortalidad'].nunique()
    },
    'TipoPoblacionObjetivo': {
        'tipo': 'Texto (Categórica)',
        'descripcion': 'Tipo de población considerada para el análisis',
        'ejemplo': 'Total',
        'valores_unicos': df['TipoPoblacionObjetivo'].nunique()
    },
    'NumeroPoblacionObjetivo': {
        'tipo': 'Entero (int32)',
        'descripcion': 'Población del municipio en el año correspondiente',
        'ejemplo': '2,508,452 (Medellín), 3,500 (municipio pequeño)',
        'valores_unicos': 'Variable'
    },
    'NumeroCasos': {
        'tipo': 'Entero (int16)',
        'descripcion': 'Variable objetivo: Número de casos de suicidio registrados',
        'ejemplo': '0, 1, 5, 246',
        'valores_unicos': f"Rango: {df['NumeroCasos'].min()}-{df['NumeroCasos'].max()}"
    }
}

# Crear DataFrame para mostrar
df_diccionario = pd.DataFrame([
    {
        'Columna': col,
        'Tipo': info['tipo'],
        'Descripción': info['descripcion'],
        'Ejemplo': info['ejemplo'],
        'Valores Únicos': info['valores_unicos']
    }
    for col, info in columnas_info.items()
])

st.dataframe(
    df_diccionario,
    use_container_width=True,
    hide_index=True
)


# 4. Calidad de datos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## ✅ Validación de Calidad de Datos")

# Verificar duplicados
st.markdown("### 🔍 Verificación de Duplicados")
duplicados = verificar_duplicados(df)

if duplicados.empty:
    st.success("✅ No se encontraron registros duplicados (municipio-año).")
else:
    st.warning(f"⚠️ Se encontraron {len(duplicados)} registros duplicados.")
    with st.expander("📄 Ver registros duplicados"):
        st.dataframe(duplicados, use_container_width=True)

# Validación de valores nulos
st.markdown("### 🔍 Valores Nulos por Columna")

nulos = df.isna().sum()
df_nulos = pd.DataFrame({
    'Columna': nulos.index,
    'Valores Nulos': nulos.values,
    'Porcentaje': (nulos.values / len(df) * 100).round(2)
})
df_nulos = df_nulos[df_nulos['Valores Nulos'] > 0]

if df_nulos.empty:
    st.success("✅ No se encontraron valores nulos en el dataset.")
else:
    st.dataframe(df_nulos, use_container_width=True, hide_index=True)

# Estadísticas de casos
st.markdown("### 📊 Estadísticas de la Variable Objetivo (NumeroCasos)")

col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)

with col_stats1:
    st.metric("Mínimo", f"{df['NumeroCasos'].min()}")

with col_stats2:
    st.metric("Máximo", f"{df['NumeroCasos'].max()}")

with col_stats3:
    st.metric("Media", f"{df['NumeroCasos'].mean():.2f}")

with col_stats4:
    st.metric("Mediana", f"{df['NumeroCasos'].median():.0f}")


# 5. Proceso de recolección
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📥 Proceso de Recolección")

st.markdown("""
<div style='background-color: #f1f5f9; padding: 1.5rem; border-radius: 10px;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>Metodología de Obtención de Datos</h3>
    <ol style='font-size: 1rem; line-height: 1.8;'>
        <li><strong>Solicitud formal:</strong> Datos obtenidos desde <a href=" https://www.datos.gov.co/">Datos Abiertos Colombia</a>.</li>
        <li><strong>Formato de descarga:</strong> Archivo CSV estructurado</li>
        <li><strong>Validación inicial:</strong> Verificación de integridad y completitud</li>
        <li><strong>Almacenamiento:</strong> Guardado en <code>static/datasets/suicidios_antioquia.csv</code></li>
        <li><strong>Control de versión:</strong> Registro en sistema Git para trazabilidad</li>
        <li><strong>Documentación:</strong> Metadatos y diccionario de datos generados</li>
    </ol>
</div>
""", unsafe_allow_html=True)


# 6. Muestra de datos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 👀 Vista Previa de los Datos")

st.markdown("### 📄 Primeros 10 Registros")
st.dataframe(df.head(10), use_container_width=True)

st.markdown("### 📄 Últimos 10 Registros")
st.dataframe(df.tail(10), use_container_width=True)


# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 2 de 7</strong></p>
</div>
""", unsafe_allow_html=True)
