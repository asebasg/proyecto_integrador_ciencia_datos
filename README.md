# 📊 Análisis de Suicidios en Antioquia (2005-2024)

<div align="center">

**Proyecto Integrador de Ciencia de Datos**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Academic-green)](LICENSE)

Análisis y Desarrollo de Software (ADSO) - 2025
📍 Centro de Tecnología de la Manufactura Avanzada, Medellín, Antioquia

</div>

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Características](#-características)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Metodología](#-metodología)
- [Equipo](#-equipo)
- [Licencia](#-licencia)

---

## 🎯 Descripción del Proyecto

Este proyecto realiza un **análisis epidemiológico integral** de los casos de suicidio en el departamento de Antioquia, Colombia, durante el período 2005-2024. Utilizando técnicas de ciencia de datos, identificamos patrones espaciotemporales, grupos de alto riesgo y tendencias evolutivas para generar recomendaciones basadas en evidencia.

### Objetivos Principales

1. **Caracterizar tendencia temporal** de casos entre 2005-2024
2. **Identificar concentración geográfica** por regiones y municipios
3. **Detectar municipios de alto riesgo** con tasas desproporcionadas
4. **Analizar correlaciones** entre variables sociodemográficas
5. **Desarrollar dashboard interactivo** para exploración de datos

### Fuente de Datos

- **Entidad:** Secretaría de Salud y Protección Social de Antioquia
- **Cobertura:** 125 municipios, 9 regiones
- **Período:** 2005-2024 (20 años)
- **Registros:** 2,500 registros × 10 variables

---

## ✨ Características

### Análisis Implementado

- ✅ **Análisis Exploratorio (EDA):** Estadísticas descriptivas, distribuciones, outliers
- ✅ **Análisis Temporal:** Tendencias, tasas de crecimiento, períodos críticos
- ✅ **Análisis Geográfico:** Concentración regional, mapas de calor
- ✅ **Análisis Estadístico:** Correlaciones (r=0.9973), rankings, índices de riesgo
- ✅ **Visualizaciones Interactivas:** 20+ gráficos con Plotly
- ✅ **Storytelling Visual:** Narrativa basada en datos con 7 hallazgos clave

### Tecnologías

- **Backend:** Python 3.9+
- **Frontend:** Streamlit 1.31.0
- **Análisis:** Pandas, NumPy, SciPy
- **Visualización:** Plotly, Matplotlib, Seaborn
- **Control de Versiones:** Git + GitHub

---

## 💻 Requisitos del Sistema

### Software

- Python 3.9 o superior
- pip (gestor de paquetes)
- Git (opcional, para clonar repositorio)

### Hardware Mínimo

- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Almacenamiento:** 500 MB libres
- **Procesador:** Dual-core 2.0 GHz o superior

---

## 🚀 Instalación

### Opción 1: Instalación Rápida (Recomendada)

```bash
# 1. Clonar el repositorio
git clone https://github.com/asebasg/proyecto_integrador_ciencia_datos.git
cd proyecto_integrador_ciencia_datos

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar entorno virtual:
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import streamlit; print('✅ Streamlit instalado correctamente')"
```

### Opción 2: Instalación Manual

```bash
# Si no tienes Git, descarga el ZIP desde GitHub y extrae
cd proyecto_integrador_ciencia_datos

# Instalar dependencias una por una
pip install streamlit==1.31.0
pip install pandas==2.1.4
pip install numpy==1.26.3
pip install plotly==5.18.0
pip install scipy==1.11.4
pip install matplotlib==3.8.2
pip install seaborn==0.13.1
```

### Verificación de Instalación

```bash
# Ejecutar script de verificación
python -c "from utils import cargar_datos; print('✅ Imports correctos')"
```

---

## 📖 Uso

### Ejecutar la Aplicación

```bash
# Desde la raíz del proyecto
streamlit run Inicio.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Navegación

La aplicación está organizada en **7 páginas accesibles desde el menú lateral** (☰):

1. **📋 Definición y Objetivos** - Contexto del problema, objetivos SMART
2. **📊 Recolección de Datos** - Fuente, metadatos, calidad de datos
3. **🔍 Exploración Inicial** - EDA completo con visualizaciones
4. **🧹 Limpieza y Preparación** - Transformaciones aplicadas
5. **📈 Análisis y Hallazgos** - Respuestas a preguntas de investigación
6. **📢 Storytelling y Visualización** - Narrativa visual con 7 hallazgos clave
7. **🤖 IA Generativa** (opcional) - Chatbot interactivo con Gemini

### Exploración de Datos

- **Filtros interactivos:** Selecciona regiones, años, municipios
- **Gráficos interactivos:** Hover, zoom, pan en todas las visualizaciones
- **Descarga de datos:** Exporta tablas en formato CSV
- **Responsive:** Funciona en desktop, tablet y móvil

---

## 📁 Estructura del Proyecto

```
proyecto_integrador_ciencia_datos/
│
├── Inicio.py                           # Portada principal (Sebastián)
│
├── pages/                              # Páginas de la aplicación
│   ├── 1_📋_Definicion_y_Objetivos.py        # Contexto (Sebastián)
│   ├── 2_📊_Recoleccion_de_Datos.py          # Fuentes (Ricardo)
│   ├── 3_🔍_Exploracion_Inicial.py           # EDA (Juan)
│   ├── 4_🧹_Limpieza_y_Preparacion.py        # Transformaciones (Ricardo)
│   ├── 5_📈_Analisis_y_Hallazgos.py          # Estadísticas (Juan)
│   ├── 6_📢_Storytelling_y_Visualizacion.py  # Narrativa (Sebastián)
│   └── 7_🤖_IA_Generativa.py                 # Chatbot (Sebastián, opcional)
│
├── utils/                              # Módulos reutilizables
│   ├── __init__.py                     # Inicializador del paquete
│   ├── data_loader.py                  # Carga y caché de datos (Ricardo)
│   ├── preprocessing.py                # Transformaciones (Ricardo)
│   ├── calculations.py                 # Estadísticas avanzadas (Juan)
│   └── visualizations.py               # Gráficos reutilizables (Sebastián)
│
├── static/                             # Archivos estáticos
│   ├── datasets/
│   │   └── suicidios_antioquia.csv    # Dataset principal
│   └── images/                         # Logos, íconos (si aplica)
│
├── docs/                               # Documentación
│   └── Informe_Analisis_Suicidios.md  # Informe técnico previo
│
├── .streamlit/                         # Configuración de Streamlit
│   ├── config.toml                     # Tema visual
│   └── secrets.toml                    # API keys (NO versionar)
│
├── .gitignore                          # Archivos excluidos de Git
├── requirements.txt                    # Dependencias del proyecto
└── README.md                           # Este archivo
```

### Responsabilidades por Integrante

| Integrante    | Rol                       | Archivos Asignados                                                 |
| ------------- | ------------------------- | ------------------------------------------------------------------ |
| **Sebastián** | Líder - Frontend          | `Inicio.py`, `pages/1,6,7`, `utils/visualizations.py`, `README.md` |
| **Ricardo**   | Data Engineer - Backend   | `pages/2,4`, `utils/data_loader.py`, `utils/preprocessing.py`      |
| **Juan**      | Data Scientist - Análisis | `pages/3,5`, `utils/calculations.py`, `docs/`                      |

---

## 🔬 Metodología

El proyecto sigue el **ciclo completo de ciencia de datos**:

### 1. Definición del Problema

- Identificación de stakeholders
- Objetivos SMART
- Preguntas de investigación

### 2. Recolección de Datos

- Extracción de fuentes oficiales
- Validación de calidad
- Documentación de metadatos

### 3. Exploración (EDA)

- Estadísticas descriptivas
- Identificación de patrones
- Detección de anomalías

### 4. Limpieza y Preparación

- Transformación de tipos de datos
- Cálculo de tasas normalizadas
- Creación de features derivadas

### 5. Análisis Estadístico

- Correlaciones (Pearson)
- Rankings por criterios
- Índices de riesgo combinados

### 6. Visualización y Comunicación

- 20+ gráficos interactivos
- Storytelling basado en datos
- Recomendaciones accionables

### 7. Despliegue

- Aplicación web con Streamlit
- Documentación completa
- Control de versiones con Git

---

## 📊 Hallazgos Principales

### 🔴 Crisis en Crecimiento

- **+79%** incremento en casos (2005-2024)
- Aceleración crítica post-2015
- Pico histórico en 2023: **586 casos**

### 🏙️ Concentración Urbana

- **60%** de casos en Valle de Aburrá
- Medellín: **40.3%** del total departamental
- Top 3 regiones: **79%** de casos

### ⚠️ Municipios Pequeños en Riesgo

- Poblaciones < 20k habitantes con **tasas desproporcionadas**
- Requieren intervención prioritaria
- Factores: aislamiento geográfico, falta de servicios

### 📈 Correlación Poblacional

- **r = 0.9973** (población vs. casos absolutos)
- Correlación casi perfecta
- Validación de hipótesis principal

---

## 👥 Equipo

| Nombre           | Rol                                    | Responsabilidades                           | GitHub                                 |
| ---------------- | -------------------------------------- | ------------------------------------------- | -------------------------------------- |
| **Sebastián**    | Líder del Proyecto / Analista Frontend | Coordinación, visualizaciones, storytelling | [@asebasg](https://github.com/asebasg) |
| **Ricardo**      | Ingeniero de Datos                     | Motor de datos, limpieza, validaciones      | -                                      |
| **Juan Esteban** | Científico de Datos                    | Estadísticas, análisis profundo, hallazgos  | -                                      |

### Institución

- **Universidad:** [Nombre de la Universidad]
- **Curso:** Proyecto Integrador de Ciencia de Datos
- **Fecha:** Diciembre 2024

---

## 🔒 Consideraciones Éticas

Este proyecto maneja datos sensibles de salud pública. Se han tomado las siguientes precauciones:

- ✅ **Datos agregados:** Sin información personal identificable
- ✅ **Propósito académico:** Análisis con fines educativos y de investigación
- ✅ **Fuente oficial:** Datos públicos de entidad gubernamental
- ✅ **Enfoque respetuoso:** Tratamiento digno de tema sensible
- ✅ **Disclaimer:** Los hallazgos NO sustituyen análisis de profesionales de salud pública

### Aviso Importante

> ⚠️ **Este análisis tiene fines estrictamente académicos.** Para diseño de políticas públicas
> o intervenciones de salud mental, consulte a profesionales especializados y autoridades
> competentes de salud pública.

---

## 📝 Licencia

Este proyecto es de uso **académico** y está disponible bajo licencia MIT modificada:

- ✅ **Permitido:** Uso educativo, fork, modificación para aprendizaje
- ❌ **Restricciones:** Uso comercial sin autorización, reproducción de datos sin citar fuente
- 📄 **Citar como:**
  ```
  Sebastián, Ricardo, Juan. (2024). Análisis de Suicidios en Antioquia (2005-2024).
  Proyecto Integrador de Ciencia de Datos. Universidad [Nombre].
  ```

---

## 🤝 Contribuciones

Este es un proyecto académico cerrado, pero se aceptan:

- 🐛 **Reportes de bugs:** Usa Issues de GitHub
- 💡 **Sugerencias:** Contacta al equipo
- 📚 **Mejoras de documentación:** Pull requests bienvenidos

---

## 📞 Contacto

Para consultas sobre el proyecto:

- **Email del equipo:** [correo@universidad.edu]
- **Repositorio:** https://github.com/asebasg/proyecto_integrador_ciencia_datos
- **Issues:** https://github.com/asebasg/proyecto_integrador_ciencia_datos/issues

---

## 📚 Referencias

1. Secretaría de Salud y Protección Social de Antioquia. (2024). _Registros de Mortalidad por Causas Externas_.
2. Organización Mundial de la Salud (OMS). (2023). _Prevención del Suicidio: Un Imperativo Global_.
3. DANE - Departamento Administrativo Nacional de Estadística. (2024). _Proyecciones de Población Municipal_.

---

## 🔄 Historial de Versiones

### v1.0.0 (Diciembre 2024) - Release Inicial

- ✅ 7 páginas funcionales completas
- ✅ 20+ visualizaciones interactivas
- ✅ Análisis estadístico completo
- ✅ Documentación integral
- ✅ Storytelling con 7 hallazgos clave

---

<div align="center">

**Hecho con ❤️ por el equipo de Ciencia de Datos**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**[⬆ Volver al inicio](#-análisis-de-suicidios-en-antioquia-2005-2024)**

</div>
