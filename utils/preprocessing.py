# Asignado a Ricardo (@ricardo778)
from .data_loader import cargar_datos, verificar_duplicados
from .preprocessing import (
    calcular_tasas, 
    filtrar_por_municipio, 
    agrupar_por_año, 
    agrupar_por_municipio,
    crear_categorias_riesgo,
    limpiar_datos_faltantes
)

__all__ = [
    'cargar_datos',
    'verificar_duplicados',
    'calcular_tasas',
    'filtrar_por_municipio', 
    'agrupar_por_año',
    'agrupar_por_municipio',
    'crear_categorias_riesgo',
    'limpiar_datos_faltantes'
]