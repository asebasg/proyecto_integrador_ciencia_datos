# Guía de desarrollo

## Instructivo completo de desarrollo para el proyecto

La siguiente guía es creada con el fin de orientar a los desarrolladores en sus tareas de contribución al proyecto mediante el desarrollo estructurado y lógico.

## Arquitectura del proyecto

A continuación se muestra el esquema de arquitectura esperado del proyecto:

```
proyecto_suicidios_antioquia/
├── Inicio.py                        # Sebastián (Líder)
├── pages/
│   ├── 1_1_Definicion_y_Objetivos.py      # Sebastián
│   ├── 2_2_Recoleccion_de_Datos.py        # Ricardo
│   ├── 3_3_Exploracion_Inicial.py         # Juan (R)
│   ├── 4_4_Limpieza_y_Preparacion.py      # Ricardo
│   ├── 5_5_Analisis_y_Hallazgos.py        # Juan (R)
│   ├── 6_6_Storytelling_y_Visualizacion.py # Sebastián
│   └── 7_7_IA_Generativa.py              # Sebastián (opcional)
├── .streamlit/
│   ├── config.toml                  # Sebastián
│   └── secrets.toml                 # Sebastián (NO versionar)
├── static/
│   ├── datasets/suicidios_antioquia.csv    # Ricardo
│   └── images/                      # Sebastián (logos, etc.)
├── utils/
│   ├── __init__.py                  # Ricardo
│   ├── data_loader.py              # Ricardo
│   ├── preprocessing.py            # Ricardo
│   ├── calculations.py             # Juan (R)
│   └── visualizations.py           # Sebastián
├── docs/
│   └── Informe_Analisis_Suicidios.md      # Juan (revisar documentación)
├── requirements.txt                 # Ricardo
├── .gitignore                      # Ricardo
└── README.md                       # Sebastián
```

> _En cada directorio del esquema se muestra el responsable asignado para la tarea, además, en cada archivo se encontrará un comentario indicando explícitamente quién es el responsable de la tarea_

## Fase 1: Configuración base del proyecto

**Objetivo**: Sentar fundamentos técnicos para que todos puedan trabajar sin conflictos

| Tarea                             | Responsable                                   | Archivo                           | Prioridad | Dependencias | Tiempo estimado |
| --------------------------------- | --------------------------------------------- | --------------------------------- | --------- | ------------ | --------------- |
| 1.1. Crear estructura de carpetas | Sebastian (@asebasg)                          | Todo el proyecto                  | 🔴 Alta   | -            | 10 min          |
| 1.2. Configurar `.gitignore`      | Sebastian (@asebasg)                          | Todo el proyecto                  | 🔴 Alta   | 1.1          | 5 min           |
| 1.3. Crear `requirements.txt`     | Sebastian (@asebasg)                          | `requirements.txt`                | 🔴 Alta   | 1.1          | 1 min           |
| 1.4. Configurar tema visual       | Sebastian (@asebasg)                          | `.streamlit/config.toml`          | 🔴 Alta   | 1.1          | 15 min          |
| 1.5. Colocar CSV en `static/`     | Sebastian (@asebasg)                          | `static/datasets/`                | 🔴 Alta   | 1.1          | 5 min           |
| 1.6. Crear `utils/__init__.py`    | Sebastian (@asebasg)                          | `utils/__init__.py`               | 🔴 Alta   | 1.1          | 10 min          |
| 1.7. Instalar dependencias        | TODOS (@asebasg, @Juanes-crypto, @ricardo778) | `pip install -r requirements.txt` | 🔴 Alta   | 1.3          | 5 min           |

**Criterio de Completitud**: Todos pueden ejecutar streamlit run Inicio.py sin errores (aunque esté vacío).

## Fase 2: Motor de datos

**Objetivo**: Crear funciones reutilizables para cargar, transformar y analizar datos

| Tarea | Responsable           | Archivo                   | Descripción                                                                       | Dependencias | Tiempo estimado |
| ----- | --------------------- | ------------------------- | --------------------------------------------------------------------------------- | ------------ | --------------- |
| 2.1   | Ricardo (@ricardo778) | `utils/data_loader.py`    | Crear cargador de datos con caché - Función `cargar_datos()` con `@st.cache_data` | Fase 1       | 45 min          |
| 2.2   | Ricardo (@ricardo778) | `utils/data_loader.py`    | Implementar validación de duplicados - Función `verificar_duplicados()`           | 2.1          | 20 min          |
| 2.3   | Ricardo (@ricardo778) | `utils/preprocessing.py`  | Crear funciones de transformación - 6 funciones: tasas, filtros, agrupaciones     | 2.1          | 1 hora          |
| 2.4   | Juan (@Juanes-crypto) | `utils/calculations.py`   | Crear funciones estadísticas - Correlaciones, rankings, crecimiento               | 2.1          | 1.5 horas       |
| 2.5   | Sebastián (@asebasg)  | `utils/visualizations.py` | Crear funciones de visualización - 8 tipos de gráficos con Plotly                 | 2.1          | 1.5 horas       |
| 2.6   | Ricardo (@ricardo778) | `utils/__init__.py`       | Actualizar **init**.py con imports - Exponer todas las funciones                  | 2.1-2.5      | 15 min          |
| 2.7   | TODOS                 | Terminal Python           | Probar imports localmente - `from utils import \*` sin errores                    | 2.6          | 10 min          |

**Criterio de Completitud**: Ejecutar sin errores:

```python
from utils import cargar_datos, calcular_tasas, crear_grafico_tendencia
df = cargar_datos()
print(df.head())
```

## Fase 3: Páginas básicas

**Objetivo**: Crear estructura de las 7 páginas con contenido funcional

| Tarea | Responsable           | Archivo                                      | Descripción                                       | Dependencias | Tiempo estimado |
| ----- | --------------------- | -------------------------------------------- | ------------------------------------------------- | ------------ | --------------- |
| 3.1   | Sebastián (@asebasg)  | `Inicio.py`                                  | Portada - Hero, resumen ejecutivo, métricas clave | Fase 2       | 1 hora          |
| 3.2   | Sebastián (@asebasg)  | `1_1_Definicion_del_problema_y_objetivos.py` | Definición - Contexto, problema, objetivos SMART  | Ninguna      | 30 min          |
| 3.3   | Ricardo (@ricardo778) | `2_2_Recoleccion_de_datos.py`                | Recolección - Fuente, metadatos, calidad          | Fase 2       | 30 min          |
| 3.4   | Juan (@Juanes-crypto) | `3_3_Exploracion_inicial.py`                 | EDA - Stats descriptivas, distribuciones          | Fase 2       | 1 hora          |
| 3.5   | Ricardo (@ricardo778) | `4_4_Limpieza_y_preparacion.py`              | Limpieza - Transformaciones aplicadas             | Fase 2       | 40 min          |
| 3.6   | Juan (@Juanes-crypto) | `5_5_Analisis_y_Hallazgos.py`                | Análisis - Insights, correlaciones, rankings      | Fase 2       | 1.5 horas       |
| 3.7   | Sebastián (@asebasg)  | `6_6_Storytelling_y_Visualizacion.py`        | Storytelling - Narrativa visual + hallazgos clave | Fase 2, 3.6  | 1.5 horas       |
| 3.8   | Sebastián (@asebasg)  | `7_7_Aplicacion_IA_Generativa.py`            | IA (opcional) - Chatbot con Gemini                | Fase 2       | 30 min          |

**Criterio de Completitud**: Todas las páginas cargan sin errores y muestran contenido real.

## Fase 4: Refinamiento y calidad

**Objetivo**: Pulir detalles, validar coherencia y preparar entrega

| Tarea | Responsable                                   | Archivo          | Descripción                                                                               | Dependencias | Tiempo estimado |
| ----- | --------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------- | ------------ | --------------- |
| 4.1   | Sebastián (@asebasg)                          | Todo el proyecto | Revisar coherencia narrativa - Verificar que las páginas cuenten una historia lógica      | Fase 3       | 30 min          |
| 4.2   | Sebastián (@asebasg)                          | Todo el proyecto | Validar todas las visualizaciones - Comprobar que gráficos sean correctos y profesionales | Fase 3       | 30 min          |
| 4.3   | TODOS (@asebasg, @Juanes-crypto, @ricardo778) | Todo el proyecto | Agregar comentarios al código - Documentar funciones complejas                            | Fase 3       | 30 min          |
| 4.4   | Sebastián (@asebasg)                          | README.md        | Crear README.md profesional - Instrucciones de instalación y uso                          | Fase 3       | 30 min          |
| 4.5   | Sebastián (@asebasg)                          | Todo el proyecto | Pruebas de navegación - Verificar flujo completo de la app                                | 4.1–4.4      | 20 min          |
| 4.6   | Ricardo (@ricardo778)                         | utils/           | Optimizar tiempos de carga - Verificar que caché funcione correctamente                   | 4.5          | 20 min          |
| 4.7   | Sebastián (@asebasg)                          | Git              | Merge final a `develop` - Integrar ramas de Ricardo y Juan                                | Fase 3       | 20 min          |

**Criterio de Completitud**: Aplicación lista para presentar al profesor

---

## Distribución detallada por integrante

### 👨‍💼 SEBASTIÁN (LÍDER - FRONTEND & COORDINACIÓN) - @asebasg

**Rama Git**: `feature/dashboard-app`
**Tiempo Total Estimado**: 10-12 horas
**Responsabilidad**: Garantizar coherencia, calidad y narrativa
Archivos Asignados (13)

1. ✅ `.streamlit/config.toml` - Tema visual
2. ✅ `Inicio.py` - Portada profesional
3. ✅ `pages/1_1_Definicion_y_Objetivos.py` - Contexto del problema
4. ✅ `pages/6_6_Storytelling_y_Visualizacion.py` - Narrativa visual
5. ✅ `pages/7_7_IA_Generativa.py` - Chatbot (opcional)
6. ✅ `utils/visualizations.py` - Funciones de gráficos
7. ✅ `README.md` - Documentación
8. ✅ `requirements.txt` - Dependencias del proyecto
9. ✅ `static/datasets/` - Dataset del proyecto (archivo CSV)
10. ✅ `utils/__init__.py`
11. ✅ Revisión de coherencia narrativa (todas las páginas)
12. ✅ Validación de visualizaciones (todas las páginas)
13. ✅ Merge final y pruebas de integración

### Checklist de Sebastián

```markdown
□ Crear estructura de carpetas (mkdir -p)
□ Configurar tema en config.toml (colores, fuente)
□ Crear Inicio.py con métricas clave y resumen ejecutivo
□ Escribir página 1 con contexto del problema y objetivos SMART
□ Desarrollar utils/visualizations.py con 8 tipos de gráficos
□ Crear página 6 con storytelling visual (5-7 hallazgos clave)
□ (Opcional) Implementar chatbot con Gemini en página 7
□ Revisar que narrativa sea coherente en todas las páginas
□ Validar que todos los gráficos rendericen correctamente
□ Escribir README.md con instrucciones claras
□ Hacer merge de ramas de Ricardo y Juan
□ Ejecutar pruebas finales de navegación
```

---

### 🔧 RICARDO (DATA ENGINEER - BACKEND) - @ricardo778

**Rama Git**: `feature/ingenieria-datos`
**Tiempo Total Estimado**: 6-7 horas
**Responsabilidad**: Motor de datos, validación y calidad

Archivos Asignados (7)

1. ✅ `utils/__init__.py`
2. ✅ `utils/data_loader.py` - Carga con caché
3. ✅ `utils/preprocessing.py` - Transformaciones
4. ✅ `pages/2_2_Recoleccion_de_Datos.py` - Metadatos
5. ✅ `pages/4_4_Limpieza_y_Preparacion.py` - Transformaciones aplicadas

### Checklist de Ricardo

```markdown
□ Implementar data_loader.py con @st.cache_data
□ Crear verificar_duplicados() en data_loader.py
□ Desarrollar 6 funciones en preprocessing.py
□ Actualizar \***\*init\*\***.py con todos los imports
□ Commit inicial a develop
□ Crear página 2 con metadatos del dataset
□ Crear página 4 mostrando transformaciones
□ Validar que caché funcione correctamente
```

---

### 📊 JUAN (DATA SCIENTIST - ANÁLISIS)

**Rama Git**: feature/analisis-profundo
**Tiempo Total Estimado**: 6-7 horas
**Responsabilidad**: Estadísticas, insights y hallazgos

Archivos Asignados (4)

1. ✅ `utils/calculations.py` - Estadísticas avanzadas
2. ✅ `pages/3_3_Exploracion_Inicial.py` - EDA
3. ✅ `pages/5_5_Analisis_y_Hallazgos.py` - Insights principales

```markdown
□ Crear 7 funciones estadísticas en calculations.py:
  - calcular_correlacion()
  - calcular_tasa_crecimiento()
  - obtener_ranking_municipios()
  - calcular_estadisticas_descriptivas()
  - calcular_indice_riesgo()
□ Desarrollar página 3 con:
  - Estadísticas descriptivas
  - Distribuciones
  - Gráficos exploratorios
□ Desarrollar página 5 con:
  - 7 hallazgos clave (insights)
  - Correlación población vs. casos
  - Ranking top 10 municipios
  - Municipios pequeños en riesgo
  - Tasa de crecimiento por período
□ Documentar hallazgos en docs/Informe_Analisis_Suicidios.md
```

> **_Nota importante:_ Asegurarse que TODAS las tareas estén completadas para poder completar la asignación de cada integrante**

---

## Flujo de trabajo en Git

**Configuración inicial (Sebastian)**

```bash
# 1. Crear rama develop desde main
git checkout -b develop

# 2. Hacer commit de estructura base
git add .
git commit -m "feat: estructura base del proyecto"
git push origin develop
```

**Trabajo individual (cada integrante)**

```bash
# Ricardo
git checkout develop
git pull origin develop
git checkout -b feature/ingenieria-datos
# ... hacer cambios ...
git add .
git commit -m "feat: implementar motor de datos"
git push origin feature/ingenieria-datos

# Juan
git checkout develop
git pull origin develop
git checkout -b feature/analisis-profundo
# ... hacer cambios ...
git add .
git commit -m "feat: agregar análisis estadístico"
git push origin feature/analisis-profundo

# Sebastián
git checkout develop
git pull origin develop
git checkout -b feature/dashboard-app
# ... hacer cambios ...
git add .
git commit -m "feat: crear frontend y storytelling"
git push origin feature/dashboard-app
```

**Integración final (Sebastián)**

```bash
# 1. Merge de Ricardo
git checkout develop
git merge feature/ingenieria-datos
git push origin develop

# 2. Merge de Juan
git merge feature/analisis-profundo
git push origin develop

# 3. Merge de Sebastián
git merge feature/dashboard-app
git push origin develop

# 4. Pruebas finales
streamlit run Inicio.py
```

---

## Criterios de calidad

Asegurarse de cumplir todos estos criterios para entregar el proyecto, en caso de faltar alguno, hacer revisión exhaustiva para cumplir con el criterio

```markdown
□ La aplicación carga sin errores en < 3 segundos
□ Todas las páginas tienen contenido real (no placeholders)
□ Los gráficos son profesionales y legibles
□ La narrativa es coherente y cuenta una historia
□ El código tiene comentarios explicativos y usa buenas prácticas
□ No hay datos hardcodeados (todo desde funciones)
□ README.md explica cómo ejecutar el proyecto
□ No se versionaron archivos sensibles (secrets.toml)
□ Los hallazgos responden a las preguntas del informe
□ Las visualizaciones usan la paleta de colores definida
```

## Entregables finales

1. ✅ Aplicación Streamlit funcional
2. ✅ Código en repositorio Git (rama develop)
3. ✅ README.md con instrucciones
4. ✅ Documentación en docs/
5. ✅ Presentación oral (usar la app como demo)

---

### Aclaraciones

Esta es una guía completa del desarrollo del proyecto final de Ciencia de Datos, habilitado para su análisis exhaustivo por herramientas de inteligencia artificial. Todo lo necesario se detalla aquí. En caso de existir alguna duda, consultar con Sebastián (@asebasg), el líder del proyecto.
