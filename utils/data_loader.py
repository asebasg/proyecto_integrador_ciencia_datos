"""
data_loader.py: Carga y caché de datos

Funciones para cargar el CSV principal con optimización de memoria
mediante caché de Streamlit (@st.cache_data).
"""

import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data  # Caché automático - los datos se cargan 1 sola vez
def cargar_datos(ruta: str = "static/datasets/suicidios_antioquia.csv") -> pd.DataFrame:
    """
    Carga el dataset principal con validaciones y optimizaciones.
    
    Args:
        ruta (str): Ruta relativa al archivo CSV
        
    Returns:
        pd.DataFrame: Dataset limpio y validado
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el dataset está vacío o tiene columnas faltantes
        
    Ejemplo de uso:
        df = cargar_datos()
        print(f"Cargados {len(df)} registros")
    """
    #  Verificar que el archivo existe
    archivo = Path(ruta)
    if not archivo.exists():
        raise FileNotFoundError(
            f"❌ No se encontró el archivo: {ruta}\n"
            f"Verifica que la estructura de carpetas sea correcta."
        )
    
    #  Cargar CSV con optimizaciones
    try:
        df = pd.read_csv(
            ruta,
            encoding='utf-8',  # Asegurar compatibilidad con tildes
            dtype={
                'CodigoMunicipio': 'int32',    # Optimización de memoria
                'CodigoRegion': 'int8',        # Regiones: 1-9
                'Anio': 'int16',               # Años: 2005-2024
                'NumeroCasos': 'int16'         # Casos: 0-246
            }
        )
        
        #  Convertir columnas categóricas (ahorra memoria)
        df['NombreRegion'] = df['NombreRegion'].astype('category')
        df['NombreMunicipio'] = df['NombreMunicipio'].astype('category')
        df['CausaMortalidad'] = df['CausaMortalidad'].astype('category')
        df['TipoPoblacionObjetivo'] = df['TipoPoblacionObjetivo'].astype('category')
        
        #  Limpiar columna de población (eliminar comas y convertir a int)
        if df['NumeroPoblacionObjetivo'].dtype == 'object':
            df['NumeroPoblacionObjetivo'] = (
                df['NumeroPoblacionObjetivo']
                .str.replace(',', '', regex=False)
                .astype('int32')
            )
        
        #  Validaciones de integridad
        
        # Validación 1: Dataset no vacío
        if df.empty:
            raise ValueError("❌ El dataset está vacío")
        
        # Validación 2: Columnas requeridas
        columnas_requeridas = [
            'NombreMunicipio', 'CodigoMunicipio', 'NombreRegion',
            'Anio', 'NumeroCasos', 'NumeroPoblacionObjetivo'
        ]
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if columnas_faltantes:
            raise ValueError(f"❌ Columnas faltantes: {columnas_faltantes}")
        
        # Validación 3: Rango de años
        if (df['Anio'] < 2005).any() or (df['Anio'] > 2024).any():
            st.warning("⚠️ Advertencia: Se encontraron años fuera del rango esperado (2005-2024)")
        
        # Validación 4: Casos negativos
        if (df['NumeroCasos'] < 0).any():
            raise ValueError("❌ Error crítico: Existen casos negativos en los datos")
        
        # Validación 5: Población cero o negativa
        if (df['NumeroPoblacionObjetivo'] <= 0).any():
            registros_invalidos = df[df['NumeroPoblacionObjetivo'] <= 0].shape[0]
            st.warning(
                f"⚠️ Advertencia: {registros_invalidos} registros tienen población ≤ 0. "
                f"Esto puede afectar el cálculo de tasas."
            )
        
        # Validación 6: Valores nulos críticos
        nulos_casos = df['NumeroCasos'].isna().sum()
        nulos_poblacion = df['NumeroPoblacionObjetivo'].isna().sum()
        
        if nulos_casos > 0 or nulos_poblacion > 0:
            st.warning(
                f"⚠️ Valores nulos encontrados: "
                f"Casos={nulos_casos}, Población={nulos_poblacion}"
            )
        
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError("❌ El archivo CSV está vacío o corrupto")
    except pd.errors.ParserError as e:
        raise ValueError(f"❌ Error al parsear CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"❌ Error inesperado al cargar datos: {str(e)}")

@st.cache_data
def obtener_metadatos(df: pd.DataFrame) -> dict:
    """
    Extrae metadatos estadísticos del dataset para mostrar en páginas.
    
    Args:
        df (pd.DataFrame): Dataset cargado
        
    Returns:
        dict: Diccionario con estadísticas principales:
            - total_registros: Número total de filas
            - total_municipios: Municipios únicos
            - total_regiones: Regiones únicas
            - anio_inicio: Año mínimo
            - anio_fin: Año máximo
            - total_casos: Suma de casos históricos
            - poblacion_total: Suma de población
            - casos_promedio_anual: Promedio de casos por año
            - memoria_mb: Memoria usada por el DataFrame
            
    Ejemplo de uso:
        meta = obtener_metadatos(df)
        print(f"Total de casos: {meta['total_casos']:,}")
    """
    return {
        'total_registros': len(df),
        'total_municipios': df['NombreMunicipio'].nunique(),
        'total_regiones': df['NombreRegion'].nunique(),
        'anio_inicio': int(df['Anio'].min()),
        'anio_fin': int(df['Anio'].max()),
        'total_casos': int(df['NumeroCasos'].sum()),
        'poblacion_total': int(df['NumeroPoblacionObjetivo'].sum()),
        'casos_promedio_anual': round(df.groupby('Anio')['NumeroCasos'].sum().mean(), 1),
        'memoria_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2)
    }


def verificar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica registros duplicados por municipio-año.
    
    En un dataset bien estructurado, NO debería haber duplicados
    (cada combinación municipio-año debe ser única).
    
    Args:
        df (pd.DataFrame): Dataset a verificar
        
    Returns:
        pd.DataFrame: DataFrame con registros duplicados (vacío si no hay).
                     Ordenado por CodigoMunicipio y Anio.
                     
    Efectos secundarios:
        Muestra advertencia en Streamlit si encuentra duplicados.
        
    Ejemplo de uso:
        duplicados = verificar_duplicados(df)
        if not duplicados.empty:
            st.dataframe(duplicados)
    """
    # Identificar duplicados (keep=False marca TODOS los duplicados, no solo el segundo)
    duplicados = df[df.duplicated(subset=['CodigoMunicipio', 'Anio'], keep=False)]
    
    if not duplicados.empty:
        num_grupos = duplicados.groupby(['CodigoMunicipio', 'Anio']).ngroups
        st.warning(
            f"⚠️ Se encontraron {len(duplicados)} registros duplicados "
            f"correspondientes a {num_grupos} combinaciones municipio-año únicas.\n\n"
            f"**Recomendación:** Revisar y consolidar estos registros antes del análisis."
        )
    
    return duplicados.sort_values(['CodigoMunicipio', 'Anio'])


def limpiar_cache():
    """
    Limpia el caché de Streamlit para forzar recarga de datos.
    
    ⚠️ ADVERTENCIA: Usar solo en desarrollo. Borrará todos los datos cacheados
    y la próxima ejecución será más lenta.
    
    Ejemplo de uso:
        if st.button("🔄 Recargar datos"):
            limpiar_cache()
            st.rerun()
    """
    st.cache_data.clear()
    st.success("✅ Caché limpiado. Los datos se recargarán en la próxima ejecución.")


#  Función auxiliar: Resúmen rápido
def resumen_dataset(df: pd.DataFrame) -> None:
    """
    Muestra un resumen visual rápido del dataset en Streamlit.
    Útil para debugging o páginas de diagnóstico.
    
    Args:
        df (pd.DataFrame): Dataset a resumir
        
    Ejemplo de uso:
        df = cargar_datos()
        resumen_dataset(df)
    """
    meta = obtener_metadatos(df)
    
    st.markdown("### 📊 Resumen del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros", f"{meta['total_registros']:,}")
    
    with col2:
        st.metric("Municipios", f"{meta['total_municipios']}")
    
    with col3:
        st.metric("Casos Totales", f"{meta['total_casos']:,}")
    
    with col4:
        st.metric("Memoria", f"{meta['memoria_mb']:.2f} MB")
    
    st.markdown(f"""
    - **Período:** {meta['anio_inicio']} - {meta['anio_fin']} ({meta['anio_fin'] - meta['anio_inicio'] + 1} años)
    - **Regiones:** {meta['total_regiones']}
    - **Promedio anual:** {meta['casos_promedio_anual']:.1f} casos/año
    """)
