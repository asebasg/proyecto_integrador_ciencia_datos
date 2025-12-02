"""
Página 7: IA Generativa con Gemini
===================================
Responsable: Sebastián (Líder)
Fecha: Diciembre 2024

PROPÓSITO:
    Asistente inteligente basado en Gemini para análisis de datos,
    respuestas a preguntas sobre el proyecto, sugerencias de mejoras
    y generación de reportes automáticos.

DEPENDENCIAS:
    - streamlit: Framework de la aplicación
    - google.generativeai: API de Gemini
    - utils.data_loader: obtener_metadatos()

TRAZABILIDAD:
    - Flujo: Página 6 (Storytelling) → **Página 7 (IA)** → Fin
    - Contexto: Utiliza hallazgos de páginas anteriores
    - API Key: Almacenada en .streamlit/secrets.toml

CARACTERÍSTICAS:
    ✅ 4 modos de interacción (Q&A, Análisis, Storytelling, Explicación)
    ✅ Historial de conversación con session_state
    ✅ Contexto automático del proyecto
    ✅ Diseño llamativo y profesional
    ✅ Privacidad: No envía datos sensibles (PII)
"""

import streamlit as st
import google.generativeai as genai
from utils import obtener_metadatos, cargar_datos

#  Configuración de página
st.set_page_config(
    page_title="IA Generativa - Gemini",
    page_icon="🤖",
    layout="wide"
)

#  Configuración de Gemini
def configurar_gemini():
    """
    Configura la API de Gemini con la clave almacenada en secrets.toml
    
    Returns:
        model: Modelo de Gemini configurado o None si falla
    """
    try:
        # Obtener API key desde secrets
        api_key = st.secrets.get("gemini_api_key", None)
        
        if not api_key:
            st.error("❌ No se encontró la API key de Gemini en secrets.toml")
            st.info("""
            💡 **Cómo configurar:**
            1. Crear archivo `.streamlit/secrets.toml`
            2. Agregar: `gemini_api_key = "TU_API_KEY_AQUÍ"`
            3. Obtener API key en: https://aistudio.google.com/api-keys
            """)
            return None
        
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Crear modelo
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        return model
        
    except Exception as e:
        st.error(f"❌ Error al configurar Gemini: {str(e)}")
        return None

def obtener_prompt_sistema(modo_seleccionado):
    """
    Retorna el prompt del sistema según el modo seleccionado
    """
    prompts = {
        "💬 Pregunta general": """
        Eres un asistente experto en análisis de datos de salud pública.
        Tu rol es responder preguntas sobre el proyecto de análisis de suicidios
        en Antioquia de forma clara, precisa y basada en los datos disponibles.
        
        INSTRUCCIONES:
        - Responde de forma concisa pero completa
        - Usa datos y números cuando sea relevante
        - Si no tienes información suficiente, indícalo claramente
        - Sugiere análisis adicionales cuando sea apropiado
        - Mantén un tono profesional pero accesible
        """,
        
        "🔍 Análisis profundo": """
        Eres un científico de datos senior especializado en análisis exploratorio (EDA).
        Tu rol es sugerir análisis, técnicas estadísticas y features que puedan
        mejorar la comprensión de los datos de suicidios en Antioquia.
        
        INSTRUCCIONES:
        - Sugiere análisis específicos y accionables
        - Recomienda técnicas estadísticas apropiadas
        - Propón features derivadas útiles
        - Justifica cada sugerencia con su beneficio analítico
        - Prioriza análisis factibles con los datos disponibles
        """,
        
        "📊 Explicación de métricas": """
        Eres un profesor de estadística que explica conceptos complejos de forma simple.
        Tu rol es interpretar métricas estadísticas (correlaciones, p-values, tasas)
        y explicar su significado en el contexto del proyecto.
        
        INSTRUCCIONES:
        - Explica conceptos sin jerga innecesaria
        - Usa analogías cuando sea útil
        - Relaciona las métricas con el contexto del proyecto
        - Indica la implicación práctica de cada métrica
        - Incluye ejemplos concretos cuando sea posible
        """,
        
        "📄 Generación de reportes": """
        Eres un analista de datos especializado en comunicación de resultados.
        Tu rol es generar resúmenes ejecutivos, conclusiones y recomendaciones
        basadas en los hallazgos del proyecto de suicidios en Antioquia.
        
        INSTRUCCIONES:
        - Escribe de forma clara y estructurada
        - Prioriza los hallazgos más importantes
        - Incluye recomendaciones accionables
        - Usa formato apropiado (listas, secciones)
        - Adapta el tono según la audiencia (técnica o ejecutiva)
        """
    }
    
    return prompts.get(modo_seleccionado, prompts["💬 Pregunta general"])

#  Inicializar session state
if 'historial_chat' not in st.session_state:
    st.session_state.historial_chat = []

if 'contexto_proyecto' not in st.session_state:
    # Cargar contexto una sola vez
    try:
        df = cargar_datos()
        meta = obtener_metadatos(df)
        
        st.session_state.contexto_proyecto = f"""
CONTEXTO DEL PROYECTO DE ANÁLISIS:

Proyecto: Análisis de Suicidios en Antioquia (2005-2024)
Fuente: Secretaría de Salud y Protección Social de Antioquia

DATOS PRINCIPALES:
- Total de registros: {meta['total_registros']:,}
- Municipios analizados: {meta['total_municipios']}
- Regiones: {meta['total_regiones']}
- Período: {meta['anio_inicio']}-{meta['anio_fin']} ({meta['anio_fin'] - meta['anio_inicio'] + 1} años)
- Total de casos históricos: {meta['total_casos']:,}
- Casos promedio anual: {meta['casos_promedio_anual']:.1f}

HALLAZGOS CLAVE:
1. Incremento del 79% en casos durante el período analizado
2. Valle de Aburrá concentra el 60% de todos los casos
3. Medellín representa el 40.3% del total departamental
4. Correlación casi perfecta (r=0.9973) entre población y casos absolutos
5. Municipios pequeños (< 20k habitantes) presentan tasas desproporcionadas
6. Aceleración crítica en el período 2020-2024

OBJETIVO DEL ANÁLISIS:
Identificar patrones espaciotemporales, grupos de alto riesgo y generar
recomendaciones basadas en evidencia para políticas de salud pública.
"""
    except:
        st.session_state.contexto_proyecto = "Proyecto de análisis de datos de salud pública."
    
# Título
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; font-size: 2.8rem; margin: 0;'>
        🪄 Asistente IA con Gemini ✨
    </h1>
    <p style='color: #e0e7ff; font-size: 1.2rem; margin-top: 0.5rem;'>
        Análisis inteligente impulsado por Google Gemini
    </p>
</div>
""", unsafe_allow_html=True)

# Verificar configuración
model = configurar_gemini()
if model is None:
    st.stop()

# Introducción
st.markdown("""
<div style='padding-left: 50px; padding-right: 50px;'>
    <p style='font-size: 1.05rem; line-height: 1.3;'>
        Soy tu asistente de IA especializado en análisis de datos. Puedo ayudarte con:
        análisis exploratorio, interpretación de métricas, generación de reportes y
        sugerencias de mejoras para tu proyecto. <br>
    </p>
    <p style='text-align: center; font-size: 1.2rem;'>¡Inicia la conversación!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Modo de interacción y chat input
col_modo, col_spacer = st.columns([1, 3])
with col_modo:
    modo = st.selectbox(
        "Modo:",
        options=["💬 Pregunta general", "🔍 Análisis profundo", "📊 Explicación de métricas", "📄 Generación de reportes"],
        index=0,
        label_visibility="collapsed"
    )

pregunta_usuario = st.text_area(
    "💭 Tu pregunta:",
    height=100,
    placeholder="Ejemplo: ¿Cuáles son las principales tendencias en los datos?"
)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    consultar = st.button("🚀 Enviar", type="primary", use_container_width=True)
with col_btn2:
    limpiar_chat = st.button("🗑️ Limpiar", use_container_width=True)

# Limpiar historial
if limpiar_chat:
    st.session_state.historial_chat = []
    st.success("✅ Historial limpiado")
    st.rerun()

# Procesar consulta
if consultar:
    if not pregunta_usuario.strip():
        st.warning("⚠️ Escribe una pregunta")
    else:
        with st.spinner("✨ Gemini está pensando..."):
            try:
                prompt_sistema = obtener_prompt_sistema(modo)
                prompt = f"{prompt_sistema}\n\n{st.session_state.contexto_proyecto}\n\nPREGUNTA: {pregunta_usuario}"
                response = model.generate_content(prompt)
                
                st.session_state.historial_chat.append({'role': 'usuario', 'content': pregunta_usuario})
                st.session_state.historial_chat.append({'role': 'asistente', 'content': response.text})
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Mostrar historial
if st.session_state.historial_chat:
    st.markdown("---")
    st.markdown("""
        <h4 style='background-color: #dbeafe; padding: 1.5rem; margin-bottom: 1rem; border-radius: 10px; border-left: 5px solid #3b82f6;'> 💬 Conversación </h4>
        """, unsafe_allow_html=True)
    
    for mensaje in reversed(st.session_state.historial_chat):
        if mensaje['role'] == 'usuario':
            st.markdown(f"""
            <div style='background-color: #f1f5f9; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <strong>👤 Tú:</strong> {mensaje['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color: #dbeafe; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <strong>✨ Gemini:</strong><br>{mensaje['content']}
            </div>
            """, unsafe_allow_html=True)

#  Preguntas frecuentes
st.markdown("---")
st.markdown("### ❓ Preguntas Frecuentes")

with st.expander("¿Qué tan precisa es Gemini?"):
    st.markdown("✅ Herramienta de exploración y sugerencias\n\n❌ NO como fuente única sin verificación")

with st.expander("¿Se envían datos sensibles?"):
    st.markdown("**No.** Solo estadísticas agregadas y metadatos. NO se envían datos individuales.")

with st.expander("¿Cómo mejorar respuestas?"):
    st.markdown("1. Sé específico\n2. Elige el modo correcto\n3. Haz preguntas de seguimiento")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
    <p><strong>Página 7 de 7</strong> <br> Fin del Análisis</p>
    <p style='font-size: 0.85rem; margin-top: 1rem;'>
        🔒 Tus datos siempre estarán protegidos
    </p>
</div>
""", unsafe_allow_html=True)