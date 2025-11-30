# Proyecto Integrador de Ciencia de Datos

Guía rápida para ejecutar, entender la estructura y configurar el proyecto. El contenido de las páginas está pensado para principiantes y sirve como checklist: reemplázalo por la implementación correspondiente cuando avances.

## Estructura del proyecto

- `Inicio.py`: portada del proyecto y equipo de trabajo.
- `pages/`: secciones del flujo del proyecto (negocio, datos, EDA, limpieza, evaluación, comunicación, IA generativa).
- `.streamlit/`: configuración de Streamlit y secretos.
- `static/`: archivos estáticos (datasets de ejemplo, documentación auxiliar).

## Configuración de Streamlit

- Archivo: `c:\Users\jhonf\Desktop\Ejericicios\proyecto_integrador_ciencia_datos\.streamlit\config.toml`
- Contenido mínimo recomendado:

```toml
enableStaticServing = true
```

Esto habilita servir archivos estáticos desde la carpeta `static/`.

### Secretos

- Archivo: `c:\Users\jhonf\Desktop\Ejericicios\proyecto_integrador_ciencia_datos\.streamlit\secrets.toml`
- Guarda aquí claves privadas (no se versiona si mantienes el `.gitignore` actualizado).
- Ejemplo:

```toml
# Ejemplos de secretos (reemplazar con valores reales)
db_username = "Jane"
gemini_api_key = "TU_API_KEY_DE_GEMINI"
```

En el código, accede así:

```python
import streamlit as st
api_key = st.secrets.get("gemini_api_key")
```

## Datos de ejemplo (static)

- Carpeta: `c:\Users\jhonf\Desktop\Ejericicios\proyecto_integrador_ciencia_datos\static\datasets`
- Incluye:
  - `clientes.csv`: clientes y churn.
  - `ventas.csv`: ventas por fecha y categoría.
  - `diccionario_datos.json`: significado de columnas.

Lectura sugerida desde código (cuando implementes):

```python
import pandas as pd
df_clientes = pd.read_csv("static/datasets/clientes.csv")
df_ventas = pd.read_csv("static/datasets/ventas.csv")
```

## Ejecución

1. Crea y activa tu entorno (opcional).
2. Instala dependencias mínimas:

```bash
pip install streamlit
```

3. Ejecuta la app:

```bash
streamlit run Inicio.py
```

## Flujo de trabajo (páginas)

- `1_1. Definición del problema y objetivos.py`: escribe el problema de negocio, KPIs SMART, stakeholders y alcance.
- `2_2. Recolección de datos.py`: documenta fuentes, permisos, trazabilidad y calidad.
- `3_3. Exploración inicial y comprensión de los datos.py.py`: realiza EDA básica y registra hallazgos.
- `4_4. Limpieza y preparación de datos.py`: trata nulos/duplicados, unifica categorías, genera features.
- `5_5. Evaluación e interpretación de resultados.py`: elige métricas, valida, interpreta y alinea con negocio.
- `6_6. Comunicación de resultados (Storytelling & Visualización).py`: plantea narrativa, visuales y recomendaciones.
- `7_7. Apliacación IA Generativa.py`: integra Gemini para Q&A, sugerencias y storytelling basado en tu análisis.

Cada página incluye un aviso: reemplaza las indicaciones por la implementación correspondiente cuando estés listo.

## IA Generativa (Gemini)

- Requisitos: clave en `secrets.toml` (`gemini_api_key`).
- Usa prompts con contexto del proyecto (problema, KPIs, resumen de datos, hallazgos, métricas).
- Interacciones sugeridas: Q&A, recomendaciones de EDA/limpieza/features, explicación de métricas, borradores de reportes.

## Buenas prácticas

- No subas secretos ni datos sensibles; usa `secrets.toml`.
- Documenta versiones/fechas de extracción de datos.
- Mantén reproducibilidad (semillas, splits, transformaciones solo con train).
- Valida con stakeholders que los resultados responden a la pregunta de negocio.

## Problemas comunes y soluciones

- No carga archivos de `static/`: verifica `enableStaticServing = true` en `config.toml` y rutas relativas correctas.
- Clave de Gemini no encontrada: revisa `secrets.toml` y acceso con `st.secrets`.
- Datos con caracteres extraños: especifica `encoding="utf-8"` al leer CSV.
