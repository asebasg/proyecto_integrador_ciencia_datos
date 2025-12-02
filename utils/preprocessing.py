"""
preprocessing.py: Transformaciones y preparación de datos

Funciones para calcular tasas, filtrar, agrupar y transformar el dataset.
"""

import pandas as pd
import numpy as np


def calcular_tasas(df: pd.DataFrame, tasa_base: int = 100000) -> pd.DataFrame:
    """
    Calcula la tasa de suicidio por cada X habitantes (default: 100,000).
    
    La tasa normalizada permite comparar municipios de diferente tamaño.
    Ejemplo: Un municipio con 1000 hab y 5 casos tiene tasa de 500 por 100k,
            mayor que uno con 100k hab y 10 casos (tasa de 10 por 100k).
    
    Args:
        df (pd.DataFrame): Dataset con columnas 'NumeroCasos' y 'NumeroPoblacionObjetivo'
        tasa_base (int): Base para el cálculo (ej: 100000 = por cada 100k habitantes)
        
    Returns:
        pd.DataFrame: Dataset con columna adicional 'TasaPor100k'
        
    Ejemplo de uso:
        df_con_tasas = calcular_tasas(df)
        print(df_con_tasas[['NombreMunicipio', 'TasaPor100k']].head())
    """
    df_copia = df.copy()
    
    # Evitar división por cero (población = 0 o NaN)
    df_copia['TasaPor100k'] = np.where(
        df_copia['NumeroPoblacionObjetivo'] > 0,
        (df_copia['NumeroCasos'] / df_copia['NumeroPoblacionObjetivo']) * tasa_base,
        0
    )
    
    # Redondear a 2 decimales
    df_copia['TasaPor100k'] = df_copia['TasaPor100k'].round(2)
    
    return df_copia


def filtrar_por_region(df: pd.DataFrame, regiones: list) -> pd.DataFrame:
    """
    Filtra el dataset por una o varias regiones.
    
    Args:
        df (pd.DataFrame): Dataset completo
        regiones (list): Lista de nombres de regiones (ej: ['Valle de Aburrá', 'Oriente'])
                        Si la lista está vacía, retorna el dataset completo.
        
    Returns:
        pd.DataFrame: Dataset filtrado (copia independiente)
        
    Ejemplo de uso:
        # Filtrar solo Valle de Aburrá
        df_valle = filtrar_por_region(df, ['Valle de Aburrá'])
        
        # Filtrar múltiples regiones
        df_top3 = filtrar_por_region(df, ['Valle de Aburrá', 'Oriente', 'Suroeste'])
    """
    if not regiones:
        return df.copy()
    
    return df[df['NombreRegion'].isin(regiones)].copy()


def filtrar_por_anio(df: pd.DataFrame, anio_inicio: int, anio_fin: int) -> pd.DataFrame:
    """
    Filtra el dataset por rango de años.
    
    Args:
        df (pd.DataFrame): Dataset completo
        anio_inicio (int): Año inicial (inclusivo)
        anio_fin (int): Año final (inclusivo)
        
    Returns:
        pd.DataFrame: Dataset filtrado
        
    Ejemplo de uso:
        # Filtrar década 2010-2019
        df_decada = filtrar_por_anio(df, 2010, 2019)
    """
    return df[(df['Anio'] >= anio_inicio) & (df['Anio'] <= anio_fin)].copy()


def agrupar_por_anio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa casos y población por año (suma total departamental).
    
    Args:
        df (pd.DataFrame): Dataset completo
        
    Returns:
        pd.DataFrame: Dataset agrupado con columnas:
            - Anio: Año
            - TotalCasos: Suma de casos en ese año
            - PoblacionTotal: Suma de población de todos los municipios
            - TasaPor100k: Tasa calculada a nivel departamental
            
    Ejemplo de uso:
        df_anual = agrupar_por_anio(df)
        print(df_anual[['Anio', 'TotalCasos', 'TasaPor100k']])
    """
    agrupado = df.groupby('Anio').agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'sum'
    }).reset_index()
    
    agrupado.columns = ['Anio', 'TotalCasos', 'PoblacionTotal']
    
    # Calcular tasa departamental
    agrupado['TasaPor100k'] = (
        (agrupado['TotalCasos'] / agrupado['PoblacionTotal']) * 100000
    ).round(2)
    
    return agrupado


def agrupar_por_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa casos y población por región (suma total histórica).
    
    Args:
        df (pd.DataFrame): Dataset completo
        
    Returns:
        pd.DataFrame: Dataset agrupado con columnas:
            - NombreRegion: Nombre de la región
            - TotalCasos: Suma de casos históricos (2005-2024)
            - PoblacionPromedio: Promedio de población
            - TasaPor100k: Tasa calculada
            - PorcentajeCasos: % del total departamental
            
    Ejemplo de uso:
        df_regional = agrupar_por_region(df)
        print(df_regional[['NombreRegion', 'TotalCasos', 'PorcentajeCasos']])
    """
    agrupado = df.groupby('NombreRegion').agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'mean'  # Promedio para evitar duplicar población
    }).reset_index()
    
    agrupado.columns = ['NombreRegion', 'TotalCasos', 'PoblacionPromedio']
    
    # Calcular tasa
    agrupado['TasaPor100k'] = (
        (agrupado['TotalCasos'] / agrupado['PoblacionPromedio']) * 100000
    ).round(2)
    
    # Calcular porcentaje del total
    total_casos = agrupado['TotalCasos'].sum()
    agrupado['PorcentajeCasos'] = (
        (agrupado['TotalCasos'] / total_casos) * 100
    ).round(1)
    
    # Ordenar por casos descendente
    agrupado = agrupado.sort_values('TotalCasos', ascending=False)
    
    return agrupado


def identificar_municipios_alto_riesgo(
    df: pd.DataFrame,
    poblacion_max: int = 20000,
    percentil_tasa: int = 75
) -> pd.DataFrame:
    """
    Identifica municipios pequeños con tasas de suicidio altas.
    
    Esta función es crítica para identificar municipios vulnerables que,
    a pesar de tener poblaciones pequeñas, presentan tasas desproporcionadamente
    altas comparadas con el promedio departamental.
    
    Args:
        df (pd.DataFrame): Dataset completo (debe tener datos de población y casos)
        poblacion_max (int): Población máxima para considerar "municipio pequeño"
                            Default: 20,000 habitantes
        percentil_tasa (int): Percentil de tasa para filtrar
                             Default: 75 (top 25% de tasas más altas)
        
    Returns:
        pd.DataFrame: DataFrame con municipios pequeños de alto riesgo, ordenados
                     por tasa descendente. Columnas:
                     - Municipio: Nombre del municipio
                     - Region: Región a la que pertenece
                     - CasosHistoricos: Suma de casos 2005-2024
                     - PoblacionPromedio: Población promedio
                     - TasaPromedioPor100k: Tasa promedio histórica
                     
    Ejemplo de uso:
        # Identificar municipios < 20k hab con tasas altas
        municipios_riesgo = identificar_municipios_alto_riesgo(df)
        print(f"Municipios en riesgo: {len(municipios_riesgo)}")
        
        # Personalizar umbrales
        municipios_criticos = identificar_municipios_alto_riesgo(
            df, 
            poblacion_max=10000,  # Más pequeños
            percentil_tasa=90     # Solo top 10%
        )
    """
    # Asegurar que exista la columna de tasa
    if 'TasaPor100k' not in df.columns:
        df = calcular_tasas(df)
    
    # Calcular umbral de tasa (percentil especificado)
    umbral_tasa = df['TasaPor100k'].quantile(percentil_tasa / 100)
    
    # Filtrar municipios pequeños con tasas altas
    municipios_riesgo = df[
        (df['NumeroPoblacionObjetivo'] <= poblacion_max) &
        (df['TasaPor100k'] >= umbral_tasa) &
        (df['NumeroCasos'] > 0)  # Excluir casos cero (sin eventos)
    ].copy()
    
    # Si no hay municipios que cumplan los criterios, retornar DataFrame vacío
    if municipios_riesgo.empty:
        return pd.DataFrame(columns=[
            'Municipio', 'Region', 'CasosHistoricos', 
            'PoblacionPromedio', 'TasaPromedioPor100k'
        ])
    
    # Agrupar por municipio (sumar casos históricos)
    resultado = municipios_riesgo.groupby(['NombreMunicipio', 'NombreRegion']).agg({
        'NumeroCasos': 'sum',
        'NumeroPoblacionObjetivo': 'mean',
        'TasaPor100k': 'mean'
    }).reset_index()
    
    resultado.columns = [
        'Municipio', 'Region', 'CasosHistoricos', 
        'PoblacionPromedio', 'TasaPromedioPor100k'
    ]
    
    # Formatear (manejar NaN antes de convertir a int)
    resultado['PoblacionPromedio'] = resultado['PoblacionPromedio'].fillna(0).astype(int)
    resultado['TasaPromedioPor100k'] = resultado['TasaPromedioPor100k'].round(2)
    
    # Ordenar por tasa descendente (más riesgosos primero)
    resultado = resultado.sort_values('TasaPromedioPor100k', ascending=False)
    
    return resultado.reset_index(drop=True)


def crear_resumen_temporal(df: pd.DataFrame, periodos: list) -> pd.DataFrame:
    """
    Crea resumen de casos por períodos personalizados.
    
    Args:
        df (pd.DataFrame): Dataset completo
        periodos (list): Lista de tuplas (inicio, fin, nombre)
                         Ejemplo: [(2005, 2014, '2005-2014'), 
                                   (2015, 2019, '2015-2019'),
                                   (2020, 2024, '2020-2024')]
        
    Returns:
        pd.DataFrame: Resumen con columnas:
            - Periodo: Nombre del período
            - TotalCasos: Suma de casos en el período
            - CasosPromedioAnual: Promedio de casos por año
            - TasaPor100k: Tasa promedio del período
            
    Ejemplo de uso:
        periodos = [
            (2005, 2009, '2005-2009'),
            (2010, 2014, '2010-2014'),
            (2015, 2019, '2015-2019'),
            (2020, 2024, '2020-2024')
        ]
        resumen = crear_resumen_temporal(df, periodos)
        print(resumen)
    """
    resumenes = []
    
    for inicio, fin, nombre in periodos:
        df_periodo = filtrar_por_anio(df, inicio, fin)
        
        total_casos = df_periodo['NumeroCasos'].sum()
        poblacion_promedio = df_periodo['NumeroPoblacionObjetivo'].mean()
        tasa = (total_casos / poblacion_promedio) * 100000 if poblacion_promedio > 0 else 0
        casos_promedio_anual = total_casos / (fin - inicio + 1)
        
        resumenes.append({
            'Periodo': nombre,
            'TotalCasos': int(total_casos),
            'CasosPromedioAnual': round(casos_promedio_anual, 1),
            'TasaPor100k': round(tasa, 2)
        })
    
    return pd.DataFrame(resumenes)


#  Función auxiliar: Validar datos para las tasas
def validar_datos_para_tasas(df: pd.DataFrame) -> tuple:
    """
    Valida que el dataset tenga las columnas necesarias para calcular tasas.
    
    Args:
        df (pd.DataFrame): Dataset a validar
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
        
    Ejemplo de uso:
        valido, mensaje = validar_datos_para_tasas(df)
        if not valido:
            st.error(mensaje)
            st.stop()
    """
    columnas_requeridas = ['NumeroCasos', 'NumeroPoblacionObjetivo']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        return False, f"Columnas faltantes: {', '.join(columnas_faltantes)}"
    
    if df['NumeroPoblacionObjetivo'].isna().all():
        return False, "Todos los valores de población son nulos"
    
    if (df['NumeroPoblacionObjetivo'] <= 0).all():
        return False, "Todos los valores de población son ≤ 0"
    
    return True, "Dataset válido para cálculo de tasas"
