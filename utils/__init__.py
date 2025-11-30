"""
Módulo utils - Funciones utilitarias para el proyecto de análisis de suicidios en Antioquia

Este módulo proporciona funciones para:
- Carga y validación de datos
- Preprocesamiento y transformación
- Cálculos estadísticos
- Visualizaciones

Asignado a Ricardo (@ricardo778)
"""

# Importar funciones de data_loader
from .data_loader import cargar_datos, verificar_duplicados

# Importar funciones de preprocessing
from .preprocessing import (
    calcular_tasas,
    filtrar_por_municipio,
    agrupar_por_año,
    agrupar_por_municipio,
    crear_categorias_riesgo,
    limpiar_datos_faltantes
)

# Lista de todas las funciones disponibles
__all__ = [
    # Data loader
    'cargar_datos',
    'verificar_duplicados',
    
    # Preprocessing
    'calcular_tasas',
    'filtrar_por_municipio', 
    'agrupar_por_año',
    'agrupar_por_municipio',
    'crear_categorias_riesgo',
    'limpiar_datos_faltantes'
]