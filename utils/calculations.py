import pandas as pd
import numpy as np
try:
    from scipy.stats import pearsonr
except Exception:
    pearsonr = None


def preparar_df(ruta_csv: str):
    """Carga y limpia el CSV esperado.

    Devuelve un DataFrame con columnas obligatorias: 'Poblacion', 'Casos'.
    """
    df = pd.read_csv(ruta_csv, encoding='latin1')
    df.columns = df.columns.str.strip()

    # Mejor intentar varias variantes comunes de nombres
    if 'NumeroPoblacionObjetivo' in df.columns:
        df['Poblacion'] = df['NumeroPoblacionObjetivo'].astype(str).str.replace(',', '', regex=False).astype(int)
    elif 'Poblacion' in df.columns:
        df['Poblacion'] = df['Poblacion'].astype(str).str.replace(',', '', regex=False).astype(int)
    else:
        raise ValueError("No se encontró una columna de población en el CSV")

    if 'NumeroCasos' in df.columns:
        df['Casos'] = df['NumeroCasos'].astype(int)
    elif 'Casos' in df.columns:
        df['Casos'] = df['Casos'].astype(int)
    else:
        raise ValueError("No se encontró una columna de casos en el CSV")

    # Normalizar nombres de municipio/región si existen
    for col in ['NombreMunicipio', 'Municipio', 'nombre_municipio']:
        if col in df.columns:
            df = df.rename(columns={col: 'NombreMunicipio'})
            break
    for col in ['NombreRegion', 'Region', 'nombre_region']:
        if col in df.columns:
            df = df.rename(columns={col: 'NombreRegion'})
            break

    # Tasa por 100k
    df = calcular_tasa_por_100k(df, casos_col='Casos', pop_col='Poblacion')
    return df


def calcular_tasa_por_100k(df: pd.DataFrame, casos_col: str = 'Casos', pop_col: str = 'Poblacion') -> pd.DataFrame:
    """Añade columna 'Tasa_x_100k' al DataFrame (float)."""
    df = df.copy()
    # evitar divisiones por cero
    df[pop_col] = df[pop_col].replace(0, np.nan)
    df['Tasa_x_100k'] = (df[casos_col] / df[pop_col]) * 100000
    return df


def calcular_estadisticas_descriptivas(df: pd.DataFrame, cols=None) -> pd.DataFrame:
    """Devuelve describe() para las columnas indicadas (por defecto numéricas)."""
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return df[cols].describe()


def calcular_correlacion(df: pd.DataFrame, x: str, y: str):
    """Calcula correlación de Pearson entre dos columnas, devuelve (r, pvalue)."""
    joined = df[[x, y]].dropna()
    if joined.shape[0] < 2:
        return np.nan, np.nan
    if pearsonr is not None:
        r, p = pearsonr(joined[x], joined[y])
        return float(r), float(p)
    # fallback simple correlation + p-value as nan
    r = np.corrcoef(joined[x], joined[y])[0, 1]
    return float(r), np.nan


def calcular_tasa_crecimiento(df: pd.DataFrame, group_col: str, value_col: str, period_col: str):
    """Calcula tasa de crecimiento porcentual por grupo entre periodos consecutivos.

    Devuelve DataFrame con columnas: group_col, period_col, value_col, pct_change
    """
    df2 = df[[group_col, period_col, value_col]].copy()
    df2 = df2.sort_values([group_col, period_col])
    df2['pct_change'] = df2.groupby(group_col)[value_col].pct_change().fillna(0)
    return df2


def obtener_ranking_municipios(df: pd.DataFrame, top_n: int = 10, casos_col: str = 'Casos', municipio_col: str = 'NombreMunicipio') -> pd.DataFrame:
    """Devuelve ranking agregado por municipio usando tasa x100k.

    Agrupa por municipio y calcula Casos, Poblacion y Tasa_x_100k agregada.
    """
    if 'Poblacion' not in df.columns:
        raise ValueError('Falta columna Poblacion')
    agg = df.groupby(municipio_col).agg(
        Casos_Total=(casos_col, 'sum'),
        Poblacion_Total=('Poblacion', 'sum')
    ).reset_index()
    agg['Tasa_x_100k'] = (agg['Casos_Total'] / agg['Poblacion_Total']) * 100000
    return agg.sort_values('Tasa_x_100k', ascending=False).head(top_n)


def calcular_indice_riesgo(df: pd.DataFrame, casos_col: str = 'Casos', pop_col: str = 'Poblacion') -> pd.Series:
    """Calcula un índice de riesgo simple: tasa normalizada (z-score) de la Tasa_x_100k."""
    df = df.copy()
    df = calcular_tasa_por_100k(df, casos_col=casos_col, pop_col=pop_col)
    tasas = df['Tasa_x_100k']
    z = (tasas - tasas.mean()) / tasas.std(ddof=0)
    return z
