"""
Este archivo convierte la carpeta utils/ en un paquete Python,
permitiendo imports limpios como:
    from utils import cargar_datos
    from utils import crear_grafico_tendencia
"""

# Versión del módulo
__version__ = "1.0.0"

#  Imports de data_loader.py
from .data_loader import (
    cargar_datos,           # ✅ Función principal de carga
    obtener_metadatos,      # ✅ AGREGADO - Extrae estadísticas del dataset
    verificar_duplicados,   # ✅ AGREGADO - Identifica registros duplicados
    limpiar_cache          # ✅ Función auxiliar
)

#  Imports de preprocessing.py
from .preprocessing import (
    calcular_tasas,
    filtrar_por_region,
    filtrar_por_anio,
    agrupar_por_anio,
    agrupar_por_region,
    identificar_municipios_alto_riesgo,
    crear_resumen_temporal
)

# Imports de calculations.py (Juan)
from .calculations import (
    calcular_correlacion,
    calcular_tasa_crecimiento,
    obtener_ranking_municipios,
    calcular_estadisticas_descriptivas,
    calcular_indice_riesgo
)

#  Imports de visualizations.py (Sebastián)
from .visualizations import (
    crear_grafico_tendencia,
    crear_grafico_barras_regiones,
    crear_grafico_pie,
    crear_heatmap_region_anio,
    crear_ranking_horizontal,
    crear_grafico_dispersion,
    crear_grafico_lineas_multiples,
    crear_barras_agrupadas,        
    crear_metrica_kpi              
)

#  Definir que se importa con "from utils import *"
__all__ = [
    # Data Loader
    'cargar_datos',
    'obtener_metadatos',
    'verificar_duplicados',
    'limpiar_cache',
    
    # Preprocessing
    'calcular_tasas',
    'filtrar_por_region',
    'filtrar_por_anio',
    'agrupar_por_anio',
    'agrupar_por_region',
    'identificar_municipios_alto_riesgo',
    'crear_resumen_temporal',
    
    # Calculations
    'calcular_correlacion',
    'calcular_tasa_crecimiento',
    'obtener_ranking_municipios',
    'calcular_estadisticas_descriptivas',
    'calcular_indice_riesgo',
    
    # Visualizations
    'crear_grafico_tendencia',
    'crear_grafico_barras_regiones',
    'crear_grafico_pie',
    'crear_heatmap_region_anio',
    'crear_ranking_horizontal',
    'crear_grafico_dispersion',
    'crear_grafico_lineas_multiples',
    'crear_barras_agrupadas',
    'crear_metrica_kpi'
]
