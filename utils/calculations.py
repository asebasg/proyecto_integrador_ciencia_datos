"""
calculations.py: Métricas y estadísticas avanzadas

PROPÓSITO:
    Funciones especializadas para análisis estadístico profundo,
    incluyendo correlaciones, rankings y métricas de riesgo.

DEPENDENCIAS:
    - pandas: Manipulación de datos
    - numpy: Operaciones numéricas
    - scipy.stats: Pruebas estadísticas
    
TRAZABILIDAD:
    - Usado por: pages/5_Analisis_y_Hallazgos.py, pages/6_Storytelling.py
    - Depende de: utils/data_loader.py, utils/preprocessing.py
    - Importado desde: utils/__init__.py
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Optional, Tuple, Dict

# Función 1: Correlación de Pearson
def calcular_correlacion(
    df: pd.DataFrame, 
    col1: str, 
    col2: str,
    metodo: str = 'pearson'
) -> dict:
    """
    Calcula coeficiente de correlación entre dos columnas numéricas.
    
    PROPÓSITO:
        Determinar si existe relación lineal (Pearson) o monotónica (Spearman)
        entre dos variables. Esencial para validar hipótesis como:
        "¿La población de un municipio correlaciona con el número de casos?"
    
    ALGORITMO:
        1. Eliminar valores nulos de ambas columnas
        2. Calcular coeficiente según método especificado
        3. Calcular p-value para significancia estadística
        4. Interpretar fuerza de la correlación
    
    Args:
        df (pd.DataFrame): Dataset con datos a correlacionar
        col1 (str): Nombre de la primera columna (ej: 'NumeroPoblacionObjetivo')
        col2 (str): Nombre de la segunda columna (ej: 'NumeroCasos')
        metodo (str): 'pearson' (lineal) o 'spearman' (monotónica)
        
    Returns:
        dict: Diccionario con claves:
            - coeficiente (float): Valor de correlación (-1 a 1)
            - p_value (float): Significancia estadística (< 0.05 = significativo)
            - interpretacion (str): Descripción cualitativa
            - significativo (bool): True si p < 0.05
            
    Raises:
        ValueError: Si las columnas no existen o no son numéricas
        
    Ejemplo de uso:
        >>> from utils import cargar_datos, calcular_correlacion
        >>> df = cargar_datos()
        >>> resultado = calcular_correlacion(df, 'NumeroPoblacionObjetivo', 'NumeroCasos')
        >>> print(f"r = {resultado['coeficiente']:.4f}, p = {resultado['p_value']:.6f}")
        >>> print(resultado['interpretacion'])
        
    TRAZABILIDAD:
        - Usado en: pages/5_Analisis_y_Hallazgos.py (Hallazgo 4)
        - Usado en: pages/6_Storytelling.py (Sección de correlación poblacional)
    """
    # Validar que las columnas existan
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Columnas no encontradas: {col1}, {col2}")
    
    # Validar que sean numéricas
    if not pd.api.types.is_numeric_dtype(df[col1]) or not pd.api.types.is_numeric_dtype(df[col2]):
        raise ValueError(f"Las columnas deben ser numéricas: {col1}, {col2}")
    
    # Eliminar valores nulos (correlación requiere pares completos)
    datos_limpios = df[[col1, col2]].dropna()
    
    if len(datos_limpios) < 2:
        raise ValueError(f"Insuficientes datos válidos (se requieren al menos 2 pares)")
    
    # Calcular correlación según método
    if metodo == 'pearson':
        coef, p_value = stats.pearsonr(datos_limpios[col1], datos_limpios[col2])
    elif metodo == 'spearman':
        coef, p_value = stats.spearmanr(datos_limpios[col1], datos_limpios[col2])
    else:
        raise ValueError(f"Método no válido: {metodo}. Use 'pearson' o 'spearman'")
    
    # Interpretar fuerza de la correlación (según criterios de Cohen)
    abs_coef = abs(coef)
    if abs_coef >= 0.9:
        fuerza = "muy fuerte"
    elif abs_coef >= 0.7:
        fuerza = "fuerte"
    elif abs_coef >= 0.5:
        fuerza = "moderada"
    elif abs_coef >= 0.3:
        fuerza = "débil"
    else:
        fuerza = "muy débil o nula"
    
    direccion = "positiva" if coef > 0 else "negativa"
    
    return {
        'coeficiente': round(coef, 4),
        'p_value': round(p_value, 6),
        'interpretacion': f"Correlación {fuerza} {direccion}",
        'significativo': p_value < 0.05,
        'n_observaciones': len(datos_limpios)
    }


# Función 2: Tasa de crecimiento
def calcular_tasa_crecimiento(
    df: pd.DataFrame, 
    grupo: Optional[str] = None
) -> pd.DataFrame:
    """
    Calcula tasa de crecimiento anual de casos.
    
    PROPÓSITO:
        Identificar períodos de aceleración o desaceleración en los casos.
        Permite responder: "¿Cuánto crecieron los casos entre 2005 y 2024?"
    
    ALGORITMO:
        1. Ordenar datos por grupo (si aplica) y año
        2. Agrupar casos por año (o por grupo-año)
        3. Calcular diferencia absoluta con año anterior
        4. Calcular porcentaje de cambio (growth rate)
    
    Args:
        df (pd.DataFrame): Dataset con columnas 'Anio' y 'NumeroCasos'
        grupo (str, optional): Columna para agrupar (ej: 'NombreRegion')
                              Si es None, calcula a nivel departamental.
        
    Returns:
        pd.DataFrame: Dataset con columnas:
            - [Grupo] (si aplica): Nombre del grupo
            - Anio: Año
            - Casos: Total de casos en ese año
            - CrecimientoAbsoluto: Diferencia con año anterior
            - CrecimientoPorcentual: % de cambio
            
    Ejemplo de uso:
        >>> # Crecimiento departamental (todos los municipios)
        >>> df_crecimiento = calcular_tasa_crecimiento(df)
        >>> print(df_crecimiento[['Anio', 'Casos', 'CrecimientoPorcentual']])
        
        >>> # Crecimiento por región
        >>> df_crecimiento_regional = calcular_tasa_crecimiento(df, grupo='NombreRegion')
        >>> print(df_crecimiento_regional.head(10))
        
    TRAZABILIDAD:
        - Usado en: pages/5_Analisis_y_Hallazgos.py (Análisis temporal)
        - Usado en: pages/6_Storytelling.py (Hallazgo 1: Crisis en aceleración)
    """
    if grupo:
        # Cálculo por grupo (ej: por región)
        df_ordenado = df.sort_values([grupo, 'Anio'])
        
        # Agrupar por grupo y año
        df_agrupado = df.groupby([grupo, 'Anio'])['NumeroCasos'].sum().reset_index()
        df_agrupado.columns = [grupo, 'Anio', 'Casos']
        
        # Calcular diferencias dentro de cada grupo
        df_agrupado['CrecimientoAbsoluto'] = df_agrupado.groupby(grupo)['Casos'].diff()
        df_agrupado['CrecimientoPorcentual'] = (
            df_agrupado.groupby(grupo)['Casos'].pct_change() * 100
        ).round(2)
        
    else:
        # Cálculo departamental (todos los municipios)
        df_agrupado = df.groupby('Anio')['NumeroCasos'].sum().reset_index()
        df_agrupado.columns = ['Anio', 'Casos']
        
        # Calcular diferencias
        df_agrupado['CrecimientoAbsoluto'] = df_agrupado['Casos'].diff()
        df_agrupado['CrecimientoPorcentual'] = (
            df_agrupado['Casos'].pct_change() * 100
        ).round(2)
    
    return df_agrupado

# Función 3: Ranking de municipios
def obtener_ranking_municipios(
    df: pd.DataFrame,
    criterio: str = 'casos',
    top_n: int = 10,
    ascendente: bool = False
) -> pd.DataFrame:
    """
    Genera ranking de municipios según diferentes criterios.
    
    PROPÓSITO:
        Identificar municipios prioritarios según casos absolutos, tasas
        o población. Permite focalizar intervenciones de salud pública.
    
    ALGORITMO:
        1. Agrupar datos por municipio (suma casos históricos)
        2. Calcular tasa por 100k habitantes
        3. Seleccionar criterio de ordenamiento
        4. Ordenar y tomar top N
        5. Agregar columna de posición (ranking)
    
    Args:
        df (pd.DataFrame): Dataset con datos de municipios
        criterio (str): Criterio de ranking:
                       - 'casos': Número total de casos históricos
                       - 'tasa': Tasa por 100k habitantes
                       - 'poblacion': Tamaño poblacional
        top_n (int): Número de municipios a retornar (default: 10)
        ascendente (bool): False = mayores primero, True = menores primero
        
    Returns:
        pd.DataFrame: Ranking con columnas:
            - Posicion: 1, 2, 3, ..., N
            - Municipio: Nombre del municipio
            - Región: Región a la que pertenece
            - CasosHistóricos: Suma de casos 2005-2024
            - PoblaciónPromedio: Población promedio
            - TasaPor100k: Tasa calculada
            
    Ejemplo de uso:
        >>> # Top 10 municipios con más casos absolutos
        >>> ranking_casos = obtener_ranking_municipios(df, criterio='casos', top_n=10)
        >>> print(ranking_casos)
        
        >>> # Top 5 municipios con mayores tasas
        >>> ranking_tasas = obtener_ranking_municipios(df, criterio='tasa', top_n=5)
        >>> print(ranking_tasas)
        
    TRAZABILIDAD:
        - Usado en: pages/3_Exploracion_Inicial.py (Top municipios)
        - Usado en: pages/5_Analisis_y_Hallazgos.py (Ranking detallado)
        - Usado en: pages/6_Storytelling.py (Hallazgo 7: Top 10 críticos)
    """
    # Agrupar por municipio (casos históricos)
    municipios = df.groupby(['NombreMunicipio', 'NombreRegion']).agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'mean'  # Promedio para evitar sumar población repetida
    }).reset_index()
    
    # Calcular tasa por 100k habitantes
    municipios['TasaPor100k'] = np.where(
        municipios['NumeroPoblacionObjetivo'] > 0,
        (municipios['NumeroCasos'] / municipios['NumeroPoblacionObjetivo']) * 100000,
        0
    ).round(2)
    
    # Seleccionar columna de ordenamiento según criterio
    if criterio == 'casos':
        col_orden = 'NumeroCasos'
    elif criterio == 'tasa':
        col_orden = 'TasaPor100k'
    elif criterio == 'poblacion':
        col_orden = 'NumeroPoblacionObjetivo'
    else:
        raise ValueError(f"Criterio no válido: {criterio}. Use 'casos', 'tasa' o 'poblacion'")
    
    # Ordenar y seleccionar top N
    ranking = municipios.sort_values(col_orden, ascending=ascendente).head(top_n)
    
    # Agregar columna de posición (1, 2, 3, ...)
    ranking.insert(0, 'Posicion', range(1, len(ranking) + 1))
    
    # Renombrar columnas para presentación
    ranking.columns = [
        'Posición', 'Municipio', 'Región', 
        'CasosHistóricos', 'PoblaciónPromedio', 'TasaPor100k'
    ]
    
    # Formatear población como entero
    ranking['PoblaciónPromedio'] = ranking['PoblaciónPromedio'].astype(int)
    
    return ranking.reset_index(drop=True)


# Función 4: Estadísticas descriptivas
def calcular_estadisticas_descriptivas(
    df: pd.DataFrame, 
    columna: str
) -> dict:
    """
    Calcula estadísticas descriptivas completas de una columna numérica.
    
    PROPÓSITO:
        Proporcionar resumen estadístico detallado para análisis exploratorio.
        Incluye medidas de tendencia central, dispersión y distribución.
    
    ALGORITMO:
        1. Extraer columna y eliminar valores nulos
        2. Calcular medidas de tendencia central (media, mediana, moda)
        3. Calcular medidas de dispersión (desv. std, rango, IQR)
        4. Calcular cuartiles y extremos
        5. Contar valores únicos y nulos
    
    Args:
        df (pd.DataFrame): Dataset con la columna a analizar
        columna (str): Nombre de la columna numérica
        
    Returns:
        dict: Diccionario con estadísticas:
            - media: Promedio aritmético
            - mediana: Valor central
            - desv_estandar: Dispersión de datos
            - minimo: Valor más bajo
            - maximo: Valor más alto
            - q1: Primer cuartil (25%)
            - q3: Tercer cuartil (75%)
            - rango_intercuartil: Q3 - Q1
            - total: Suma total (si aplica)
            - valores_unicos: Conteo de valores distintos
            - valores_nulos: Conteo de NaN
            
    Ejemplo de uso:
        >>> stats_casos = calcular_estadisticas_descriptivas(df, 'NumeroCasos')
        >>> print(f"Media: {stats_casos['media']:.2f}")
        >>> print(f"Mediana: {stats_casos['mediana']:.2f}")
        >>> print(f"Desv. Est.: {stats_casos['desv_estandar']:.2f}")
        
    TRAZABILIDAD:
        - Usado en: pages/3_Exploracion_Inicial.py (Resumen estadístico)
        - Usado en: pages/5_Analisis_y_Hallazgos.py (Análisis descriptivo)
    """
    if columna not in df.columns:
        raise ValueError(f"Columna no encontrada: {columna}")
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise ValueError(f"La columna '{columna}' no es numérica")
    
    serie = df[columna].dropna()
    
    if len(serie) == 0:
        raise ValueError(f"La columna '{columna}' no tiene valores válidos")
    
    # Calcular estadísticas
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    
    return {
        'columna': columna,
        'media': round(serie.mean(), 2),
        'mediana': round(serie.median(), 2),
        'desv_estandar': round(serie.std(), 2),
        'minimo': round(serie.min(), 2),
        'maximo': round(serie.max(), 2),
        'q1': round(q1, 2),
        'q3': round(q3, 2),
        'rango_intercuartil': round(q3 - q1, 2),
        'total': int(serie.sum()) if serie.dtype in ['int64', 'int32', 'int16'] else round(serie.sum(), 2),
        'valores_unicos': serie.nunique(),
        'valores_nulos': df[columna].isna().sum(),
        'n_observaciones': len(serie)
    }


# Función 5: Índice de riesgo combinado
def calcular_indice_riesgo(
    df: pd.DataFrame,
    peso_tasa: float = 0.6,
    peso_crecimiento: float = 0.4
) -> pd.DataFrame:
    """
    Calcula un índice de riesgo combinado (tasa actual + tendencia de crecimiento).
    
    PROPÓSITO:
        Combinar dos dimensiones del riesgo: (1) tasa actual de suicidio
        y (2) tendencia de crecimiento reciente. Municipios con tasas altas
        Y crecimiento acelerado son los más prioritarios.
    
    ALGORITMO:
        1. Filtrar últimos 3 años para tendencia reciente
        2. Calcular tasa promedio reciente por municipio
        3. Calcular crecimiento (primer vs último año del período)
        4. Normalizar ambos valores a escala 0-100
        5. Calcular índice ponderado: tasa*0.6 + crecimiento*0.4
        6. Ordenar por índice descendente (mayor riesgo primero)
    
    Args:
        df (pd.DataFrame): Dataset con casos por municipio y año
        peso_tasa (float): Peso de la tasa actual (0-1, default: 0.6)
        peso_crecimiento (float): Peso del crecimiento reciente (0-1, default: 0.4)
        
    Returns:
        pd.DataFrame: Municipios con columnas:
            - Municipio: Nombre del municipio
            - TasaReciente: Tasa promedio últimos 3 años
            - CrecimientoPorcentual: % de cambio en período reciente
            - IndiceRiesgo: Índice combinado (0-100)
            
    Raises:
        ValueError: Si los pesos no suman 1.0
        
    Ejemplo de uso:
        >>> # Índice con pesos por defecto (60% tasa, 40% crecimiento)
        >>> df_riesgo = calcular_indice_riesgo(df)
        >>> print(df_riesgo.head(10))
        
        >>> # Índice priorizando tasa actual (80% tasa, 20% crecimiento)
        >>> df_riesgo_tasa = calcular_indice_riesgo(df, peso_tasa=0.8, peso_crecimiento=0.2)
        
    TRAZABILIDAD:
        - Usado en: pages/5_Analisis_y_Hallazgos.py (Índice de riesgo)
        - Conceptualizado para: Priorización de recursos de salud pública
    """
    # Validar pesos
    if abs(peso_tasa + peso_crecimiento - 1.0) > 0.001:
        raise ValueError(f"Los pesos deben sumar 1.0 (actual: {peso_tasa + peso_crecimiento})")
    
    # Filtrar últimos 3 años para tendencia reciente
    anio_max = df['Anio'].max()
    df_reciente = df[df['Anio'] >= anio_max - 2].copy()
    
    if df_reciente.empty:
        raise ValueError("No hay suficientes datos recientes (últimos 3 años)")
    
    # Calcular tasa promedio reciente por municipio
    tasas = df_reciente.groupby('NombreMunicipio').apply(
        lambda x: ((x['NumeroCasos'].sum() / x['NumeroPoblacionObjetivo'].mean()) * 100000)
        if x['NumeroPoblacionObjetivo'].mean() > 0 else 0
    ).reset_index()
    tasas.columns = ['Municipio', 'TasaReciente']
    
    # Calcular crecimiento (comparar primero vs último año del período reciente)
    crecimiento = df_reciente.groupby(['NombreMunicipio', 'Anio'])['NumeroCasos'].sum().reset_index()
    
    # Para cada municipio, calcular cambio porcentual
    def calcular_cambio(grupo):
        if len(grupo) < 2:
            return 0
        inicial = grupo.iloc[0]['NumeroCasos']
        final = grupo.iloc[-1]['NumeroCasos']
        if inicial == 0:
            return 0
        return ((final - inicial) / inicial) * 100
    
    crecimiento_pct = crecimiento.groupby('NombreMunicipio').apply(calcular_cambio).reset_index()
    crecimiento_pct.columns = ['Municipio', 'CrecimientoPorcentual']
    
    # Unir tasas y crecimiento
    riesgo = tasas.merge(crecimiento_pct, on='Municipio')
    
    # Normalizar valores a escala 0-100 (min-max scaling)
    def normalizar_minmax(serie):
        if serie.max() == serie.min():
            return pd.Series([50] * len(serie))
        return ((serie - serie.min()) / (serie.max() - serie.min())) * 100
    
    riesgo['TasaNormalizada'] = normalizar_minmax(riesgo['TasaReciente'])
    riesgo['CrecimientoNormalizado'] = normalizar_minmax(riesgo['CrecimientoPorcentual'])
    
    # Calcular índice combinado (ponderado)
    riesgo['IndiceRiesgo'] = (
        riesgo['TasaNormalizada'] * peso_tasa +
        riesgo['CrecimientoNormalizado'] * peso_crecimiento
    ).round(1)
    
    # Ordenar por índice descendente (mayor riesgo primero)
    riesgo = riesgo.sort_values('IndiceRiesgo', ascending=False)
    
    # Retornar columnas relevantes
    return riesgo[['Municipio', 'TasaReciente', 'CrecimientoPorcentual', 'IndiceRiesgo']].round(2).reset_index(drop=True)


# Función auxiliar: Resumen rápido de correlaciones
def matriz_correlaciones(
    df: pd.DataFrame,
    columnas: list
) -> pd.DataFrame:
    """
    Genera matriz de correlaciones entre múltiples columnas.
    
    PROPÓSITO:
        Facilitar análisis exploratorio mostrando todas las correlaciones
        entre variables numéricas de interés de una vez.
    
    Args:
        df (pd.DataFrame): Dataset con las columnas a correlacionar
        columnas (list): Lista de nombres de columnas numéricas
        
    Returns:
        pd.DataFrame: Matriz de correlaciones (valores entre -1 y 1)
        
    Ejemplo de uso:
        >>> cols = ['NumeroCasos', 'NumeroPoblacionObjetivo', 'Tasa_x_100k']
        >>> matriz = matriz_correlaciones(df, cols)
        >>> print(matriz)
        
    TRAZABILIDAD:
        - Usado en: pages/3_Exploracion_Inicial.py (EDA avanzado)
    """
    # Validar que todas las columnas existan
    columnas_faltantes = [col for col in columnas if col not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Columnas no encontradas: {columnas_faltantes}")
    
    # Calcular matriz de correlaciones
    matriz = df[columnas].corr(method='pearson').round(4)
    
    return matriz
