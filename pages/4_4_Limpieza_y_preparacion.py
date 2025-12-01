"""
Página 4: Limpieza y Preparación de Datos

Responsable: Ricardo (Data Engineer)
Descripción: Documenta las transformaciones aplicadas al dataset,
            incluyendo limpieza, conversiones y creación de features.
"""

import streamlit as st
from utils import cargar_datos, calcular_tasas, agrupar_por_region
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="Limpieza y Preparación",
    page_icon="🧹",
    layout="wide"
)


# Carga de datos
try:
    df = cargar_datos()
except Exception as e:
    st.error(f"❌ Error al cargar datos: {str(e)}")
    st.stop()


# Título principal
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='color: #1e3a8a; font-size: 2.5rem;'>
        🧹 Limpieza y Preparación de Datos
    </h1>
    <p style='font-size: 1.1rem; color: #64748b;'>
        Transformaciones aplicadas para análisis de calidad
    </p>
</div>
""", unsafe_allow_html=True)


# Introducción
st.markdown("""
<div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1e3a8a;'>
    <h3 style='margin-top: 0; color: #1e3a8a;'>🎯 Objetivo de esta Fase</h3>
    <p style='font-size: 1.05rem; line-height: 1.7;'>
        Los datos crudos raramente están listos para análisis. Esta sección documenta 
        todas las transformaciones aplicadas al dataset original para garantizar su 
        <strong>calidad, consistencia y utilidad analítica</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Transformación 1: Conversión de tipos
st.markdown("## 🔧 Transformación 1: Optimización de Tipos de Datos")

st.markdown("""
### 📝 Justificación

Los tipos de datos por defecto de Pandas no siempre son óptimos. Al especificar 
tipos adecuados, **reducimos el uso de memoria en ~60%** y aceleramos operaciones.
""")

col_tipo1, col_tipo2 = st.columns(2)

with col_tipo1:
    st.markdown("""
    **❌ Antes (tipos por defecto):**
    ```
    CodigoMunicipio: int64 (8 bytes)
    CodigoRegion: int64 (8 bytes)
    Anio: int64 (8 bytes)
    NumeroCasos: int64 (8 bytes)
    NombreRegion: object (variable)
    ```
    """)

with col_tipo2:
    st.markdown("""
    **✅ Después (tipos optimizados):**
    ```
    CodigoMunicipio: int32 (4 bytes)
    CodigoRegion: int8 (1 byte)
    Anio: int16 (2 bytes)
    NumeroCasos: int16 (2 bytes)
    NombreRegion: category (fijo)
    ```
    """)

# Mostrar ahorro de memoria
memoria_antes = len(df) * (8 + 8 + 8 + 8) / 1024**2  # MB estimados antes
memoria_despues = df.memory_usage(deep=True).sum() / 1024**2
ahorro_pct = ((memoria_antes - memoria_despues) / memoria_antes * 100)

st.success(f"✅ **Ahorro de memoria:** {ahorro_pct:.1f}% (de ~{memoria_antes:.2f} MB a {memoria_despues:.2f} MB)")


# Transformación 2: Limpieza de población
st.markdown("<br><br>")
st.markdown("## 🔧 Transformación 2: Limpieza de Columna Poblacional")

st.markdown("""
### 📝 Problema Identificado

La columna `NumeroPoblacionObjetivo` venía como texto con comas separadoras de miles:
""")

# Ejemplo con datos simulados
ejemplo_antes = pd.DataFrame({
    'Municipio': ['Medellín', 'Envigado', 'Rionegro'],
    'Poblacion_Original': ['2,508,452', '221,708', '125,861']
})

st.markdown("**❌ Formato original (texto):**")
st.dataframe(ejemplo_antes, use_container_width=True, hide_index=True)

st.markdown("""
### ✅ Solución Aplicada

```python
# Eliminar comas y convertir a entero
df['NumeroPoblacionObjetivo'] = (
    df['NumeroPoblacionObjetivo']
    .str.replace(',', '', regex=False)
    .astype('int32')
)
```
""")

# Ejemplo después
ejemplo_despues = pd.DataFrame({
    'Municipio': ['Medellín', 'Envigado', 'Rionegro'],
    'Poblacion_Limpia': [2508452, 221708, 125861]
})

st.markdown("**✅ Formato transformado (numérico):**")
st.dataframe(ejemplo_despues, use_container_width=True, hide_index=True)

st.info("💡 **Por qué es importante:** Sin esta conversión, no podríamos calcular tasas ni correlaciones.")


# Transformación 3: Cálculo de tasas
st.markdown("<br><br>")
st.markdown("## 🔧 Transformación 3: Cálculo de Tasas Normalizadas")

st.markdown("""
### 📝 Justificación Crítica

Los **casos absolutos** son engañosos para comparar municipios. Un municipio pequeño 
con 5 casos puede estar en mayor riesgo que una ciudad con 50 casos.

**Fórmula aplicada:**

```
Tasa por 100k = (Casos / Población) × 100,000
```

Esta métrica permite comparaciones justas entre municipios de diferente tamaño.
""")

# Calcular tasas para ejemplo
df_con_tasas = calcular_tasas(df)

# Ejemplo comparativo
ejemplo_comparativo = pd.DataFrame({
    'Municipio': ['Municipio A (grande)', 'Municipio B (pequeño)'],
    'Población': [100000, 5000],
    'Casos': [10, 5],
    'Tasa por 100k': [
        (10 / 100000) * 100000,
        (5 / 5000) * 100000
    ]
})

st.markdown("### 📊 Ejemplo Comparativo")
st.dataframe(
    ejemplo_comparativo.style.highlight_max(subset=['Tasa por 100k'], color='#fee2e2'),
    use_container_width=True,
    hide_index=True
)

st.warning("""
⚠️ **Observación:** Aunque el Municipio A tiene el doble de casos absolutos, 
el Municipio B tiene una **tasa 10 veces mayor** (100 vs 10 por 100k habitantes), 
indicando mayor riesgo relativo.
""")

# Mostrar estadísticas de tasas calculadas
col_tasa1, col_tasa2, col_tasa3, col_tasa4 = st.columns(4)

with col_tasa1:
    st.metric("Tasa Mínima", f"{df_con_tasas['TasaPor100k'].min():.2f}")

with col_tasa2:
    st.metric("Tasa Máxima", f"{df_con_tasas['TasaPor100k'].max():.2f}")

with col_tasa3:
    st.metric("Tasa Promedio", f"{df_con_tasas['TasaPor100k'].mean():.2f}")

with col_tasa4:
    st.metric("Tasa Mediana", f"{df_con_tasas['TasaPor100k'].median():.2f}")


# Transformación 4: Agregaciones
st.markdown("<br><br>")
st.markdown("## 🔧 Transformación 4: Agregaciones por Región")

st.markdown("""
### 📝 Objetivo

Crear vistas agregadas que faciliten el análisis de patrones regionales.
""")

# Mostrar agregación regional
df_regional = agrupar_por_region(df)

st.markdown("### 📊 Resultado: Dataset Agregado por Región")
st.dataframe(
    df_regional[['NombreRegion', 'TotalCasos', 'PoblacionPromedio', 'TasaPor100k', 'PorcentajeCasos']],
    use_container_width=True,
    hide_index=True,
    column_config={
        'PoblacionPromedio': st.column_config.NumberColumn(format="%d"),
        'TasaPor100k': st.column_config.NumberColumn(format="%.2f"),
        'PorcentajeCasos': st.column_config.NumberColumn(format="%.1f%%")
    }
)

st.info("""
💡 **Utilidad:** Esta transformación permite responder preguntas como 
"¿Qué región concentra más casos?" o "¿Cuál tiene la tasa más alta?" sin 
necesidad de recalcular cada vez.
""")


# Transformación 5: Variables categóricas
st.markdown("<br><br>")
st.markdown("## 🔧 Transformación 5: Conversión de Variables Categóricas")

st.markdown("""
### 📝 Justificación

Columnas de texto repetitivo (como `NombreRegion`, `NombreMunicipio`) se convierten 
al tipo `category` de Pandas para:

- ✅ **Reducir memoria:** En vez de guardar "Valle de Aburrá" 500 veces, se guarda una vez + referencias
- ✅ **Acelerar operaciones:** Agrupaciones y filtros son más rápidos
- ✅ **Mantener integridad:** Evita errores de tipeo en análisis posteriores
""")

# Mostrar columnas categóricas
categoricas = df.select_dtypes(include='category').columns.tolist()

st.markdown(f"""
**Columnas convertidas a `category`:**
- {', '.join(categoricas)}
""")

# Comparación de memoria
col_cat1, col_cat2 = st.columns(2)

with col_cat1:
    st.markdown("""
    **Como `object` (texto):**
    - Cada valor ocupa espacio completo
    - Memoria: ~alta
    - Operaciones: lentas
    """)

with col_cat2:
    st.markdown("""
    **Como `category`:**
    - Valores únicos + códigos
    - Memoria: ~60% menos
    - Operaciones: ~3x más rápidas
    """)


# Resumen de transformaciones
st.markdown("<br><br>")
st.markdown("---")
st.markdown("## 📋 Resumen de Transformaciones Aplicadas")

transformaciones = [
    {
        'Transformación': 'Optimización de tipos de datos',
        'Antes': 'int64, object',
        'Después': 'int32, int16, int8, category',
        'Beneficio': f'Ahorro de {ahorro_pct:.1f}% memoria'
    },
    {
        'Transformación': 'Limpieza de población',
        'Antes': 'Texto con comas ("2,508,452")',
        'Después': 'Entero (2508452)',
        'Beneficio': 'Habilitación de cálculos matemáticos'
    },
    {
        'Transformación': 'Cálculo de tasas',
        'Antes': 'Solo casos absolutos',
        'Después': '+ TasaPor100k',
        'Beneficio': 'Comparación justa entre municipios'
    },
    {
        'Transformación': 'Agregación regional',
        'Antes': 'Datos por municipio-año',
        'Después': '+ Vistas agregadas',
        'Beneficio': 'Análisis de patrones regionales'
    },
    {
        'Transformación': 'Variables categóricas',
        'Antes': 'object (texto)',
        'Después': 'category',
        'Beneficio': 'Optimización de memoria y velocidad'
    }
]

df_resumen = pd.DataFrame(transformaciones)
st.dataframe(df_resumen, use_container_width=True, hide_index=True)


# Validación post-transformaciones
st.markdown("<br><br>")
st.markdown("## ✅ Validación Post-Transformación")

st.markdown("""
Después de aplicar todas las transformaciones, validamos que el dataset 
mantenga su integridad:
""")

val_col1, val_col2, val_col3 = st.columns(3)

with val_col1:
    nulos_total = df.isna().sum().sum()
    if nulos_total == 0:
        st.success(f"✅ **Sin valores nulos**\n\n{nulos_total} registros afectados")
    else:
        st.warning(f"⚠️ **Valores nulos**\n\n{nulos_total} registros afectados")

with val_col2:
    duplicados = len(df[df.duplicated(subset=['CodigoMunicipio', 'Anio'])])
    if duplicados == 0:
        st.success(f"✅ **Sin duplicados**\n\n{duplicados} duplicados")
    else:
        st.warning(f"⚠️ **Duplicados encontrados**\n\n{duplicados} duplicados")

with val_col3:
    casos_negativos = (df['NumeroCasos'] < 0).sum()
    if casos_negativos == 0:
        st.success(f"✅ **Datos consistentes**\n\n{casos_negativos} casos negativos")
    else:
        st.error(f"❌ **Casos negativos**\n\n{casos_negativos} registros")


# Dataset final
st.markdown("<br><br>")
st.markdown("## 📊 Dataset Final Transformado")

st.markdown("""
El dataset está ahora listo para análisis estadístico avanzado.
""")

# Mostrar estructura del dataset
st.markdown("### 🔍 Información del Dataset")
buffer = []
buffer.append(f"- **Filas:** {len(df):,}")
buffer.append(f"- **Columnas:** {len(df.columns)}")
buffer.append(f"- **Memoria:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
buffer.append(f"- **Tipos de datos:** {df.dtypes.value_counts().to_dict()}")

st.markdown('\n'.join(buffer))

# Vista previa
st.markdown("### 👀 Vista Previa (5 registros)")
st.dataframe(df.head(), use_container_width=True)


# Footer
st.markdown("<br><br>")
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 4 de 7</strong> | Siguiente: 📈 Análisis y Hallazgos</p>
    <p style='font-size: 0.85rem; margin-top: 1rem;'>
        ✅ Todas las transformaciones están documentadas y validadas
    </p>
</div>
""", unsafe_allow_html=True)
