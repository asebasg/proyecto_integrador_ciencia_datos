"""
visualizations.py: Gráficos Reutilizables con Plotly
====================================================
Responsable: Sebastián (Líder - Frontend)
Descripción: Funciones para crear visualizaciones interactivas profesionales
            usando Plotly. Cada función retorna un objeto go.Figure listo
            para mostrar con st.plotly_chart().

PALETA DE COLORES (sincronizada con config.toml):
- Primario: #1e3a8a (azul oscuro) - Seriedad
- Secundario: #fb923c (naranja) - Alertas/énfasis
- Terciario: #10b981 (verde) - Positivo
- Fondo: #f1f5f9 (gris claro)
- Texto: #1f2937 (gris oscuro)
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List

#  Constantes para paletas de colores
COLORES = {
    'primario': '#1e3a8a',      # Azul oscuro (serio, profesional)
    'secundario': '#fb923c',    # Naranja (alertas, datos críticos)
    'terciario': '#10b981',     # Verde (positivo, mejoras)
    'fondo': '#f1f5f9',         # Gris claro (fondos)
    'texto': '#1f2937'          # Gris oscuro (legibilidad)
}

#  Paleta para regiones
COLORES_REGIONES = {
    '#1e3a8a',  # Azul oscuro
    '#3b82f6',  # Azul medio
    '#60a5fa',  # Azul claro
    '#fb923c',  # Naranja
    '#10b981',  # Verde
    '#f59e0b',  # Amarillo
    '#ef4444',  # Rojo
    '#8b5cf6',  # Morado
    '#ec4899'   # Rosa
}

#  Función 1: Gráfico de línea (tendencias)
def crear_grafico_tendencia(
    df: pd.DataFrame,
    x: str = 'Anio',  # Year column
    y: str = 'TotalCasos',
    titulo: str = 'Tendencia Temporal de Casos',
    etiqueta_y: str = 'Número de Casos',
    mostrar_media: bool = True,
    color_linea: str = None
) -> go.Figure:
    """
    Crea un gráfico de línea para visualizar tendencias temporales.
    Ideal para mostrar evoluciones de casos año tras año.

    Argumentos:
        df: DataFrame con datos temporales
        x: Columna para eje X (Generalmente "Anio")
        y: Columna para eje Y (variable a graficar)
        titulo: Título del gráfico
        etiqueta_y: Etiqueta del eje Y
        mostrar_media: Si True, muestra la línea horizontal del promedio
        color_linea: Color personalizado (opcional, usa primario por defecto)
    Returns:
        go.Figure: Gráfico interactivo de Plotly
        
    Uso:
        fig = crear_grafico_tendencia(df_anual, y='TotalCasos')
        st.plotly_chart(fig, use_container_width=True)
    """
    color = color_linea or COLORES['primario']

    fig = go.Figure()

    # Linea principal con marcadores
    fig.add_trace(go.Scatter(
        x=df[x],
        y=df[y],
        mode='lines+markers',
        name='Casos',
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color),
        hovertemplate='<b>Año:</b> %{x}<br><b>Casos:</b> %{y:,.0f}<extra></extra>'
    ))

    # Linea de promedio (opcional)
    if mostrar_media:
        promedio = df[y].mean()
        fig.add_hline(
            y=promedio,
            line_dash='dash',
            line_color=COLORES['secundario'],
            line_width=2,
            annotation_text=f'Promedio: {promedio:.1f}',
            annotation_position='right',
            annotation_font_size=12
        )
    
    # Configuracion del layout
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=18)),
        xaxis_title=x,
        yaxis_title=etiqueta_y,
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=False
    )

    return fig

# Función 2: Crear gráfico de barras
def crear_grafico_barras_regiones(
    df: pd.DataFrame,
    columna_region: str = 'NombreRegion',
    columna_valor: str = 'TotalCasos',
    titulo: str = 'Distribución de Casos por Región',
    orientacion: str = 'vertical'
) -> go.Figure:
    """
    Crea gráfico de barras para comparar regiones.
    Las barras se colorean en gradiente según el valor.
    
    Args:
        df: DataFrame con datos por región (ya agrupado)
        columna_region: Nombre de la columna con regiones
        columna_valor: Nombre de la columna con valores
        titulo: Título del gráfico
        orientacion: 'vertical' (barras verticales) o 'horizontal'
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        df_regiones = agrupar_por_region(df)
        fig = crear_grafico_barras_regiones(df_regiones)
        st.plotly_chart(fig, use_container_width=True)
    """
    # Ordenar por valor descendente
    df_ordenado = df.sort_values(columna_valor, ascending=(orientacion == 'horizontal'))
    
    if orientacion == 'horizontal':
        fig = go.Figure(data=[
            go.Bar(
                y=df_ordenado[columna_region],
                x=df_ordenado[columna_valor],
                orientation='h',
                text=df_ordenado[columna_valor],
                texttemplate='%{text:,.0f}',
                textposition='outside',
                marker=dict(
                    color=df_ordenado[columna_valor],
                    colorscale='Blues',
                    showscale=False
                ),
                hovertemplate='<b>%{y}</b><br>Casos: %{x:,.0f}<extra></extra>'
            )
        ])
        fig.update_layout(
            xaxis_title=columna_valor,
            yaxis_title='',
            height=500
        )
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=df_ordenado[columna_region],
                y=df_ordenado[columna_valor],
                text=df_ordenado[columna_valor],
                texttemplate='%{text:,.0f}',
                textposition='outside',
                marker=dict(
                    color=df_ordenado[columna_valor],
                    colorscale='Blues',
                    showscale=False
                ),
                hovertemplate='<b>%{x}</b><br>Casos: %{y:,.0f}<extra></extra>'
            )
        ])
        fig.update_layout(
            xaxis_title='',
            yaxis_title=columna_valor,
            xaxis_tickangle=-45,
            height=500
        )
    
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=18)),
        template='plotly_white',
        showlegend=False
    )
    
    return fig

#  Función 3: Gráfico de pie/dona (porcentajes)

def crear_grafico_pie(
    df: pd.DataFrame,
    columna_categoria: str = 'NombreRegion',
    columna_valor: str = 'TotalCasos',
    titulo: str = 'Distribución Porcentual por Región',
    tipo: str = 'dona'
) -> go.Figure:
    """
    Crea gráfico circular (pie o dona) para mostrar proporciones.
    
    Args:
        df: DataFrame con datos categóricos
        columna_categoria: Columna con categorías (ej: regiones)
        columna_valor: Columna con valores numéricos
        titulo: Título del gráfico
        tipo: 'pie' (círculo completo) o 'dona' (con agujero)
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        df_regiones = agrupar_por_region(df)
        fig = crear_grafico_pie(df_regiones, tipo='dona')
        st.plotly_chart(fig, use_container_width=True)
    """
    hole_size = 0.4 if tipo == 'dona' else 0
    
    fig = px.pie(
        df,
        values=columna_valor,
        names=columna_categoria,
        title=titulo,
        color_discrete_sequence=COLORES_REGIONES,
        hole=hole_size
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Casos: %{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(x=0.5, xanchor='center', font=dict(size=18)),
        height=500
    )
    
    return fig

#  Función 4: Heatmap (mapa de calor)
def crear_heatmap_region_anio(
    df: pd.DataFrame,
    titulo: str = 'Mapa de Calor: Casos por Región y Año'
) -> go.Figure:
    """
    Crea mapa de calor (heatmap) para visualizar patrones en dos dimensiones.
    Ideal para ver cómo evolucionan los casos por región a lo largo del tiempo.
    
    Args:
        df: DataFrame con columnas 'NombreRegion', 'Anio', 'NumeroCasos'
        titulo: Título del gráfico
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        fig = crear_heatmap_region_anio(df)
        st.plotly_chart(fig, use_container_width=True)
    """
    # Crear pivot table para el heatmap
    pivot = df.pivot_table(
        values='NumeroCasos',
        index='NombreRegion',
        columns='Anio',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Blues',
        hovertemplate='<b>Región:</b> %{y}<br><b>Año:</b> %{x}<br><b>Casos:</b> %{z:,.0f}<extra></extra>',
        colorbar=dict(title='Casos')
    ))
    
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=18)),
        xaxis_title='Año',
        yaxis_title='Región',
        template='plotly_white',
        height=600
    )
    
    return fig

#  Función 5: Ranking horizontal (top N)
def crear_ranking_horizontal(
    df: pd.DataFrame,
    columna_etiqueta: str,
    columna_valor: str,
    titulo: str = 'Top 10 Municipios',
    top_n: int = 10,
    color_escala: str = 'Reds'
) -> go.Figure:
    """
    Crea gráfico de barras horizontal para rankings (Top N).
    El #1 aparece arriba, ideal para comparaciones.
    
    Args:
        df: DataFrame con datos (debe estar ordenado)
        columna_etiqueta: Columna con nombres (ej: 'Municipio')
        columna_valor: Columna con valores (ej: 'CasosHistóricos')
        titulo: Título del gráfico
        top_n: Número de elementos a mostrar
        color_escala: Escala de colores de Plotly
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        ranking = obtener_ranking_municipios(df, criterio='casos', top_n=10)
        fig = crear_ranking_horizontal(ranking, 'Municipio', 'CasosHistóricos')
        st.plotly_chart(fig, use_container_width=True)
    """
    # Tomar top N y ordenar ascendente (para que #1 quede arriba)
    df_top = df.head(top_n).sort_values(columna_valor, ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=df_top[columna_etiqueta],
            x=df_top[columna_valor],
            orientation='h',
            text=df_top[columna_valor],
            texttemplate='%{text:,.0f}',
            textposition='outside',
            marker=dict(
                color=df_top[columna_valor],
                colorscale=color_escala,
                showscale=False
            ),
            hovertemplate='<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=18)),
        xaxis_title=columna_valor,
        yaxis_title='',
        template='plotly_white',
        height=500
    )
    
    return fig

#  Función 6: Gráfico de dispersión (correlación)
def crear_grafico_dispersion(
    df: pd.DataFrame,
    x: str,
    y: str,
    titulo: str = 'Gráfico de Dispersión',
    etiqueta_x: str = None,
    etiqueta_y: str = None,
    color_por: str = None,
    mostrar_tendencia: bool = True
) -> go.Figure:
    """
    Crea gráfico de dispersión (scatter) para analizar correlaciones.
    Muestra relación entre dos variables numéricas.
    
    Args:
        df: DataFrame con datos
        x: Columna para eje X
        y: Columna para eje Y
        titulo: Título del gráfico
        etiqueta_x: Etiqueta personalizada eje X (opcional)
        etiqueta_y: Etiqueta personalizada eje Y (opcional)
        color_por: Columna categórica para colorear puntos (opcional)
        mostrar_tendencia: Si True, agrega línea de tendencia
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        fig = crear_grafico_dispersion(
            df, 
            x='NumeroPoblacionObjetivo', 
            y='NumeroCasos',
            titulo='Correlación: Población vs. Casos',
            mostrar_tendencia=True
        )
        st.plotly_chart(fig, use_container_width=True)
    """
    etiqueta_x = etiqueta_x or x
    etiqueta_y = etiqueta_y or y
    
    if color_por:
        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color_por,
            title=titulo,
            labels={x: etiqueta_x, y: etiqueta_y},
            trendline='ols' if mostrar_tendencia else None,
            color_discrete_sequence=COLORES_REGIONES
        )
    else:
        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=titulo,
            labels={x: etiqueta_x, y: etiqueta_y},
            trendline='ols' if mostrar_tendencia else None
        )
        fig.update_traces(marker=dict(color=COLORES['primario'], size=8))
    
    fig.update_layout(
        title=dict(x=0.5, xanchor='center', font=dict(size=18)),
        template='plotly_white',
        height=500
    )
    
    return fig

#  Función 7: Gráfico de líneas múltiples
def crear_grafico_lineas_multiples(
    df: pd.DataFrame,
    x: str,
    y: str,
    grupo: str,
    titulo: str = 'Comparación de Tendencias',
    etiqueta_y: str = 'Valor'
) -> go.Figure:
    """
    Crea gráfico con múltiples líneas para comparar grupos.
    Útil para comparar evolución de varias regiones simultáneamente.
    
    Args:
        df: DataFrame con datos
        x: Columna para eje X (generalmente 'Anio')
        y: Columna para eje Y (variable a comparar)
        grupo: Columna para agrupar (ej: 'NombreRegion')
        titulo: Título del gráfico
        etiqueta_y: Etiqueta del eje Y
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        # Comparar evolución de top 5 regiones
        top_regiones = ['Valle de Aburrá', 'Oriente', 'Suroeste', 'Urabá', 'Nordeste']
        df_filtrado = df[df['NombreRegion'].isin(top_regiones)]
        df_agrupado = df_filtrado.groupby(['Anio', 'NombreRegion'])['NumeroCasos'].sum().reset_index()
        fig = crear_grafico_lineas_multiples(df_agrupado, 'Anio', 'NumeroCasos', 'NombreRegion')
        st.plotly_chart(fig, use_container_width=True)
    """
    fig = px.line(
        df,
        x=x,
        y=y,
        color=grupo,
        title=titulo,
        labels={y: etiqueta_y},
        color_discrete_sequence=COLORES_REGIONES,
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=7)
    )
    
    fig.update_layout(
        title=dict(x=0.5, xanchor='center', font=dict(size=18)),
        xaxis_title=x,
        yaxis_title=etiqueta_y,
        template='plotly_white',
        height=500,
        hovermode='x unified',
        legend=dict(
            title=grupo,
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        )
    )
    
    return fig

#  Función 8: Gráfico de barras agrupadas (comparación de períodos)
def crear_barras_agrupadas(
    df: pd.DataFrame,
    columna_categoria: str,
    columnas_valores: List[str],
    titulo: str = 'Comparación por Períodos',
    etiquetas_valores: List[str] = None
) -> go.Figure:
    """
    Crea gráfico de barras agrupadas para comparar múltiples métricas.
    Ideal para comparar diferentes períodos lado a lado.
    
    Args:
        df: DataFrame con datos
        columna_categoria: Columna con categorías (ej: 'Periodo')
        columnas_valores: Lista de columnas con valores a comparar
        titulo: Título del gráfico
        etiquetas_valores: Etiquetas personalizadas (opcional)
        
    Returns:
        go.Figure: Gráfico interactivo
        
    Uso:
        # Comparar casos y tasas por período
        fig = crear_barras_agrupadas(
            df_periodos,
            'Periodo',
            ['TotalCasos', 'TasaPor100k'],
            etiquetas_valores=['Casos Totales', 'Tasa por 100k']
        )
        st.plotly_chart(fig, use_container_width=True)
    """
    etiquetas = etiquetas_valores or columnas_valores
    
    fig = go.Figure()
    
    colores = [COLORES['primario'], COLORES['secundario'], COLORES['terciario']]
    
    for i, (col, etiqueta) in enumerate(zip(columnas_valores, etiquetas)):
        fig.add_trace(go.Bar(
            x=df[columna_categoria],
            y=df[col],
            name=etiqueta,
            text=df[col],
            texttemplate='%{text:,.1f}',
            textposition='outside',
            marker_color=colores[i % len(colores)],
            hovertemplate='<b>%{x}</b><br>' + etiqueta + ': %{y:,.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=titulo, x=0.5, xanchor='center', font=dict(size=18)),
        xaxis_title='',
        yaxis_title='Valor',
        template='plotly_white',
        height=500,
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig

#  Métricas visuales (KPIs)
def crear_metrica_kpi(
    valor: float,
    titulo: str,
    prefijo: str = '',
    sufijo: str = '',
    comparacion: Optional[float] = None,
    comparacion_texto: str = 'vs. período anterior'
) -> dict:
    """
    Prepara datos para mostrar una métrica KPI visual en Streamlit.
    NO retorna un gráfico, sino un dict con valores formateados.
    
    Args:
        valor: Valor principal del KPI
        titulo: Título de la métrica
        prefijo: Texto antes del valor (ej: '$')
        sufijo: Texto después del valor (ej: '%', 'casos')
        comparacion: Valor de comparación (opcional)
        comparacion_texto: Texto descriptivo de la comparación
        
    Returns:
        dict: Datos formateados para st.metric()
        
    Uso:
        kpi = crear_metrica_kpi(7916, 'Total de Casos', comparacion=7330, comparacion_texto='vs. 2005-2019')
        st.metric(
            label=kpi['titulo'],
            value=kpi['valor'],
            delta=kpi['delta'],
            delta_color=kpi['color']
        )
    """
    valor_formateado = f"{prefijo}{valor:,.0f}{sufijo}"
    
    if comparacion is not None:
        delta = valor - comparacion
        delta_pct = (delta / comparacion * 100) if comparacion != 0 else 0
        delta_texto = f"{delta:+,.0f} ({delta_pct:+.1f}%) {comparacion_texto}"
        color = 'inverse'  # Rojo para aumentos (negativo en casos de suicidio)
    else:
        delta_texto = None
        color = 'off'
    
    return {
        'titulo': titulo,
        'valor': valor_formateado,
        'delta': delta_texto,
        'color': color
    }
