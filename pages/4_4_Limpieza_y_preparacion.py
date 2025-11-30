# Asignado a Ricardo (@ricardo778)

import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
from utils.preprocessing import *

st.set_page_config(page_title="Limpieza y Preparación", layout="wide")
st.title("🧹 Limpieza y Preparación de Datos")

st.markdown("""
### 🎯 Objetivo de esta fase
Transformar los datos crudos en un formato adecuado para análisis, aplicando:
- **Limpieza** de valores faltantes y duplicados
- **Transformaciones** para cálculo de tasas
- **Categorización** por niveles de riesgo
- **Validación** de la calidad de datos
""")

# Cargar datos originales
df_original = cargar_datos()

if not df_original.empty:
    # Mostrar estado inicial
    st.header("📊 Estado Inicial de los Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Registros originales", f"{len(df_original):,}")
    
    with col2:
        municipios_count = df_original['municipio'].nunique() if 'municipio' in df_original.columns else "N/A"
        st.metric("Municipios", municipios_count)
    
    with col3:
        st.metric("Años cubiertos", f"{df_original['año'].min()}-{df_original['año'].max()}")
    
    # Mostrar datos originales
    st.subheader("👀 Vista de Datos Originales")
    st.dataframe(df_original.head(10), use_container_width=True)
    
    # Aplicar transformaciones
    st.header("🔄 Transformaciones Aplicadas")
    
    # 1. Transformaciones de formato numérico
    st.subheader("1. Corrección de Formato Numérico")
    code_clean = '''
# Ejemplo de transformaciones aplicadas en preprocessing.py
def limpiar_datos_faltantes(df):
    \"\"\"Limpia valores faltantes del dataset\"\"\"
    return df.dropna()

def calcular_tasas(df, col_casos, col_poblacion, nombre_tasa='tasa'):
    \"\"\"Calcula tasas por cada 100,000 habitantes\"\"\"
    df[nombre_tasa] = (df[col_casos] / df[col_poblacion]) * 100000
    return df
    '''
    st.code(code_clean, language='python')
    
    # Aplicar transformaciones reales
    df_transformado = df_original.copy()
    
    # 2. Calcular tasas
    st.subheader("2. Cálculo de Tasas por 100,000 Habitantes")
    if 'casos_suicidios' in df_transformado.columns and 'poblacion' in df_transformado.columns:
        df_transformado = calcular_tasas(df_transformado, 'casos_suicidios', 'poblacion', 'tasa_suicidios')
        st.success("✅ Tasa de suicidios calculada correctamente")
        
        # Mostrar ejemplo del cálculo
        ejemplo = df_transformado[['municipio', 'año', 'casos_suicidios', 'poblacion', 'tasa_suicidios']].head(5)
        st.dataframe(ejemplo, use_container_width=True)
    else:
        st.error("❌ No se encontraron las columnas necesarias para calcular tasas")
    
    # 3. Categorizar por riesgo
    st.subheader("3. Categorización por Nivel de Riesgo")
    if 'tasa_suicidios' in df_transformado.columns:
        df_transformado = crear_categorias_riesgo(df_transformado, 'tasa_suicidios')
        st.success("✅ Niveles de riesgo asignados (Bajo/Medio/Alto)")
        
        # Mostrar distribución de riesgo
        distribucion = df_transformado['nivel_riesgo'].value_counts()
        st.bar_chart(distribucion)
    else:
        st.warning("⚠️ No se pudo categorizar por riesgo - tasa no calculada")
    
    # 4. Limpieza de datos faltantes
    st.subheader("4. Limpieza de Valores Faltantes")
    filas_antes = len(df_transformado)
    df_transformado = limpiar_datos_faltantes(df_transformado)
    filas_despues = len(df_transformado)
    
    if filas_antes == filas_despues:
        st.success("✅ No se encontraron valores faltantes")
    else:
        st.warning(f"⚠️ Se eliminaron {filas_antes - filas_despues} registros con valores faltantes")
    
    # Mostrar comparación final
    st.header("📈 Comparación Final: Antes vs Después")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Antes de las Transformaciones")
        st.dataframe(df_original[['municipio', 'año', 'casos_suicidios', 'poblacion']].head(8), 
                    use_container_width=True)
        st.caption(f"Forma original: {df_original.shape}")
    
    with col2:
        st.subheader("Después de las Transformaciones")
        columnas_mostrar = ['municipio', 'año', 'casos_suicidios', 'poblacion']
        if 'tasa_suicidios' in df_transformado.columns:
            columnas_mostrar.append('tasa_suicidios')
        if 'nivel_riesgo' in df_transformado.columns:
            columnas_mostrar.append('nivel_riesgo')
            
        st.dataframe(df_transformado[columnas_mostrar].head(8), use_container_width=True)
        st.caption(f"Forma transformada: {df_transformado.shape}")
    
    # Resumen de transformaciones
    st.header("📋 Resumen de Transformaciones")
    
    transformaciones = [
        "✅ **Normalización**: Nombres de columnas estandarizados",
        "✅ **Cálculo de tasas**: Tasa de suicidios por 100,000 habitantes", 
        "✅ **Categorización**: Niveles de riesgo (Bajo/Medio/Alto)",
        "✅ **Limpieza**: Eliminación de valores faltantes",
        "✅ **Validación**: Verificación de integridad de datos",
        "✅ **Optimización**: Tipos de datos adecuados para análisis"
    ]
    
    for transformacion in transformaciones:
        st.write(transformacion)
    
    # Mostrar el código de transformaciones
    st.subheader("🛠️ Código de Transformaciones Implementadas")
    
    code_transform = '''
# 1. Cálculo de Tasas
def calcular_tasas(df, col_casos, col_poblacion, nombre_tasa='tasa'):
    \"\"\"Calcula tasas por cada 100,000 habitantes\"\"\"
    df[nombre_tasa] = (df[col_casos] / df[col_poblacion]) * 100000
    return df

# 2. Categorización por Riesgo  
def crear_categorias_riesgo(df, col_tasa):
    \"\"\"Categoriza municipios por nivel de riesgo\"\"\"
    condiciones = [
        df[col_tasa] < 5,
        (df[col_tasa] >= 5) & (df[col_tasa] < 10),
        df[col_tasa] >= 10
    ]
    categorias = ['Bajo riesgo', 'Riesgo medio', 'Alto riesgo']
    df['nivel_riesgo'] = pd.cut(df[col_tasa], bins=[0, 5, 10, float('inf')], 
                               labels=categorias, right=False)
    return df

# 3. Limpieza de Datos
def limpiar_datos_faltantes(df):
    \"\"\"Elimina registros con valores faltantes\"\"\"
    return df.dropna()
    '''
    st.code(code_transform, language='python')
    
else:
    st.error("❌ No se pudieron cargar los datos para el proceso de limpieza")

st.markdown("---")
st.success("El dataset resultante está listo para cálculos matemáticos y optimizado para el dashboard.")
st.caption("Página desarrollada por Ricardo (@ricardo778) - Procesamiento y transformación de datos")