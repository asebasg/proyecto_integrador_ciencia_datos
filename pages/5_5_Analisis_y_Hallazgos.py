import streamlit as st

st.title("Evaluación e interpretación de resultados")

st.markdown("""
Objetivo:
- Medir si el análisis o modelo logra el objetivo de negocio y entender por qué.

Elegir métricas:
- Clasificación: accuracy, precision, recall, F1, AUC.
- Regresión: MAE, RMSE, R².
- Selecciona la métrica que refleje el costo de errores en tu caso.

Validación:
- Baseline: compara con una referencia simple.
- Validación cruzada: evalúa estabilidad en diferentes particiones.
- Pruebas de robustez: cómo cambia el desempeño con distintos subconjuntos.

Interpretación:
- Importancia de variables: qué factores influyen más.
- Análisis de errores: casos en los que falla y por qué.

Validación con negocio:
- ¿Responde la pregunta original?
- ¿Las recomendaciones son útiles y accionables?
- ¿Los resultados son comprensibles para stakeholders?

Salida esperada:
- Métricas clave, conclusiones y puntos de mejora.
""")

st.info("Cuando avances, reemplaza estas indicaciones por la implementación correspondiente de esta etapa.")