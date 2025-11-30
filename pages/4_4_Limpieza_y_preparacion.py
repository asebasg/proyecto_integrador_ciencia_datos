# Asignado a Ricardo (@ricardo778)

import streamlit as st

st.title("4️⃣ Limpieza y Preparación de Datos")

st.markdown("""
Para garantizar la calidad del análisis, se implementó un pipeline de limpieza en el módulo `src/etl.py`.
""")

st.subheader("🛠️ Transformaciones Realizadas")

code = '''
# 1. Corrección de Formato Numérico
# El original tenía '2,500' como texto. Se eliminaron comas y convirtió a int.
df['NumeroPoblacionObjetivo'] = df['NumeroPoblacionObjetivo'].str.replace(',', '').astype(int)

# 2. Optimización de Memoria
# Las columnas repetitivas se convirtieron a tipo 'category'.
cols_cat = ['NombreRegion', 'TipoPoblacionObjetivo', 'CausaMortalidad']
for col in cols_cat:
    df[col] = df[col].astype('category')

# 3. Validación de Nulos
# Se verificó que no existieran registros vacíos en campos críticos.
df.dropna(subset=['NumeroCasos', 'Anio'], inplace=True)
'''
st.code(code, language='python')

st.markdown("### ✅ Resultado")
st.success("El dataset resultante está listo para cálculos matemáticos y optimizado para el dashboard.")