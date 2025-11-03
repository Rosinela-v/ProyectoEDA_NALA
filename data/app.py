import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="NALA — De los Leus al Euro",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - Estilo elegante inspirado en nala.es
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #2C5530;
        text-align: center;
        font-weight: 300;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', sans-serif;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #4A7C59;
        font-weight: 400;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #E8E8E8;
        padding-bottom: 0.5rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E8E8E8;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stPlotlyChart {
        border-radius: 8px;
        margin: 1rem 0;
    }
    .info-box {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4A7C59;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header">NALA — De los Leus al Euro</div>', unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #6B7280; margin-bottom: 3rem;'>Análisis comparativo de precios y accesibilidad entre mercados</div>", unsafe_allow_html=True)

# Parámetros de conversión
TIPO_CAMBIO = 5.03  # 1 EUR = 5.03 LEI

# Función para clasificar gamas
def clasificar_gama(precio, pais):
    if pais == "España":
        return "Baja" if precio <= 8 else "Media" if precio <= 15 else "Alta"
    else:  # Rumanía
        limite_baja = 8 * TIPO_CAMBIO
        limite_media = 15 * TIPO_CAMBIO
        return "Baja" if precio <= limite_baja else "Media" if precio <= limite_media else "Alta"

# Cargar datos reales
@st.cache_data
def load_data():
    try:
        # Cargar tus archivos CSV reales
        df_es = pd.read_csv('./nala_es.csv')
        df_ro = pd.read_csv('./nala_ro.csv')
        
        # Limpiar datos como en tu notebook
        def limpiar_datos(df, pais, keywords_pack):
            df_clean = df.copy()
            df_clean["gramos/ml"] = df_clean["gramos/ml"].fillna(0).astype(int)
            
            if "categoria" in df_clean.columns:
                df_clean = df_clean[df_clean["categoria"] != "Otro"]
            
            # Filtrar packs y sets
            for keyword in keywords_pack:
                df_clean = df_clean[~df_clean["nombre"].str.contains(keyword, case=False, na=False)]
            
            df_clean['país'] = pais
            return df_clean

        keywords_es = ["pack", "set", "rutina"]
        keywords_ro = ["pachet", "pack", "set", "rutina"]

        df_es_clean = limpiar_datos(df_es, "España", keywords_es)
        df_ro_clean = limpiar_datos(df_ro, "Rumania", keywords_ro)

        # Combinar datasets
        df_combined = pd.concat([df_es_clean, df_ro_clean], ignore_index=True)
        
        # Limpieza final
        keywords_combinadas = ["pack", "set", "rutina", "pachet", "kit", "combo"]
        for keyword in keywords_combinadas:
            df_combined = df_combined[~df_combined["nombre"].str.contains(keyword, case=False, na=False)]
        
        return df_combined
        
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        # Datos de ejemplo como fallback
        return pd.DataFrame({
            'país': ['España', 'España', 'Rumania', 'Rumania'],
            'categoria_general': ['Rostro', 'Corporal', 'Rostro', 'Corporal'],
            'precio': [15.90, 8.50, 79.90, 45.50],
            'nombre': ['Crema Facial', 'Gel de Ducha', 'Crema Facial', 'Gel de Ducha']
        })

# Cargar datos
df_es_ro = load_data()

# Verificar que tenemos las columnas necesarias
required_columns = ['país', 'precio']
missing_columns = [col for col in required_columns if col not in df_es_ro.columns]

if missing_columns:
    st.error(f"Faltan columnas necesarias: {missing_columns}")
    st.stop()

# Aplicar transformaciones
df_es_ro["gama"] = df_es_ro.apply(lambda row: clasificar_gama(row["precio"], row["país"]), axis=1)
df_es_ro['precio_eur'] = df_es_ro.apply(
    lambda row: row['precio'] if row['país'] == 'España' else row['precio'] / TIPO_CAMBIO, 
    axis=1
)

# Sidebar elegante
with st.sidebar:
    st.markdown("### 🔍 Filtros de Análisis")
    st.markdown("---")
    
    paises_seleccionados = st.multiselect(
        "Países:",
        options=df_es_ro['país'].unique(),
        default=df_es_ro['país'].unique()
    )
    
    # Solo mostrar selector de categorías si la columna existe
    if 'categoria_general' in df_es_ro.columns:
        categorias_seleccionadas = st.multiselect(
            "Categorías:",
            options=df_es_ro['categoria_general'].unique(),
            default=df_es_ro['categoria_general'].unique()
        )
    else:
        categorias_seleccionadas = ['Todos']
    
    st.markdown("---")
    st.markdown("### 💱 Información Cambiaria")
    st.info(f"**Tipo de cambio:** 1 EURO = {TIPO_CAMBIO} LEI")

# Filtrar datos
df_filtrado = df_es_ro[df_es_ro['país'].isin(paises_seleccionados)]

if 'categoria_general' in df_es_ro.columns:
    df_filtrado = df_filtrado[df_filtrado['categoria_general'].isin(categorias_seleccionadas)]

# MÉTRICAS PRINCIPALES
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_productos = len(df_filtrado)
    st.metric(
        label="📦 Productos Totales",
        value=f"{total_productos:,}",
        delta=None
    )

with col2:
    precio_medio_eur = df_filtrado['precio_eur'].mean()
    st.metric(
        label="💰 Precio Medio",
        value=f"€{precio_medio_eur:.2f}",
        delta=None
    )

with col3:
    productos_es = len(df_filtrado[df_filtrado['país'] == 'España'])
    st.metric(
        label="🇪🇸 España",
        value=f"{productos_es:,}",
        delta=None
    )

with col4:
    productos_ro = len(df_filtrado[df_filtrado['país'] == 'Rumania'])
    st.metric(
        label="🇷🇴 Rumanía", 
        value=f"{productos_ro:,}",
        delta=None
    )

# GRÁFICA 1: VISIÓN GLOBAL - Sunburst
st.markdown('<div class="sub-header">🌍 Visión Global del Portfolio NALA</div>', unsafe_allow_html=True)

# Verificar que tenemos las columnas necesarias para el sunburst
sunburst_columns = ['país', 'gama', 'precio_eur']
if all(col in df_filtrado.columns for col in sunburst_columns):
    if 'categoria_general' in df_filtrado.columns:
        path = ['país', 'categoria_general', 'gama']
    else:
        path = ['país', 'gama']
    
    fig_sunburst = px.sunburst(
        df_filtrado,
        path=path,
        values='precio_eur',
        color='precio_eur',
        color_continuous_scale='RdYlBu_r',
        title='<b>VISIÓN GLOBAL NALA</b><br>Distribución del Portfolio por País, Categoría y Gama de Precio<br><sub>Precios convertidos a EUR (1€ = 5.03 LEI)</sub>',
        height=700
    )
    
    fig_sunburst.update_layout(
        template='plotly_white',
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_sunburst, use_container_width=True)
else:
    st.warning("No hay suficientes datos para generar el gráfico Sunburst")

# GRÁFICA 2: DISTRIBUCIÓN DE PRECIOS
st.markdown('<div class="sub-header">📊 Distribución de Precios</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Histograma comparativo
    fig_hist = px.histogram(
        df_filtrado, 
        x='precio', 
        color='país', 
        nbins=30,
        title='Distribución de Precios - España vs Rumanía',
        barmode='overlay',
        opacity=0.7
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # Boxplot comparativo con precios en EUR para ambos países
    fig_box = px.box(
        df_filtrado, 
        x='país', 
        y='precio_eur',  # Usar precio_eur en lugar de precio
        title='Comparación de Precios por País (EUR)',
        color='país',
        labels={'precio_eur': 'Precio (EUR)', 'país': 'País'}
    )
    
    # Agregar anotación con el tipo de cambio
    fig_box.add_annotation(
        x=0.5, y=1.05,
        xref="paper", yref="paper",
        text=f"💱 Tipo de cambio: 1 EUR = {TIPO_CAMBIO} LEI",
        showarrow=False,
        font=dict(size=12, color="#6B7280"),
        bgcolor="white",
        bordercolor="#E8E8E8",
        borderwidth=1,
        borderpad=4
    )
    
    st.plotly_chart(fig_box, use_container_width=True)

# GRÁFICA 3: DISTRIBUCIÓN POR CATEGORÍAS (si existe la columna)
if 'categoria_general' in df_filtrado.columns:
    st.markdown('<div class="sub-header">📈 Análisis por Categorías</div>', unsafe_allow_html=True)
    
    # Histograma por categorías
    fig_distribucion = px.histogram(
        df_filtrado,
        x='precio',
        color='país',
        facet_col='categoria_general',
        nbins=20,
        title='📊 Distribución de Precios por Categoría General - España vs Rumanía',
        barmode='overlay',
        opacity=0.7
    )
    
    fig_distribucion.update_layout(
        height=600,
        showlegend=True,
        xaxis_title="Precio",
        yaxis_title="Frecuencia"
    )
    
    st.plotly_chart(fig_distribucion, use_container_width=True)

# GRÁFICA 4: VIOLIN PLOT POR CATEGORÍA (si existe la columna)
if 'categoria_general' in df_filtrado.columns:
    st.markdown('<div class="sub-header">🎻 Distribución Detallada por Categoría</div>', unsafe_allow_html=True)
    
    fig_violin = px.violin(
        df_filtrado,
        x='categoria_general',
        y='precio',
        color='país',
        box=True,
        points=False,
        title='Distribución de Precios por Categoría General'
    )
    
    st.plotly_chart(fig_violin, use_container_width=True)

# GRÁFICA 5: ANÁLISIS DE ACCESIBILIDAD
st.markdown('<div class="sub-header">💝 Análisis de Accesibilidad</div>', unsafe_allow_html=True)

# Cálculos de accesibilidad
precio_mediano_es = df_filtrado[df_filtrado['país'] == 'España']['precio_eur'].median()
precio_mediano_ro = df_filtrado[df_filtrado['país'] == 'Rumania']['precio_eur'].median()

# Salarios mínimos (datos de referencia)
salario_min_es = 1184  # España en EUR
salario_min_ro = 4050  # Rumanía en LEI

# Productos comprables con un salario mínimo
productos_comprables_es = salario_min_es / precio_mediano_es if precio_mediano_es > 0 else 0
productos_comprables_ro = (salario_min_ro / TIPO_CAMBIO) / precio_mediano_ro if precio_mediano_ro > 0 else 0

accesibilidad_data = pd.DataFrame({
    'País': ['España', 'Rumanía'],
    'Productos_comprables': [productos_comprables_es, productos_comprables_ro]
})

fig_accesibilidad = px.bar(
    accesibilidad_data,
    x='País',
    y='Productos_comprables',
    title='Accesibilidad Nala - Productos comprables con un salario mínimo',
    labels={'Productos_comprables': 'Número de productos', 'País': ''},
    color='País',
    text_auto='.0f',
)

fig_accesibilidad.update_layout(
    showlegend=False,
    template='plotly_white',
    yaxis_title='Número de productos'
)

st.plotly_chart(fig_accesibilidad, use_container_width=True)

# GRÁFICA 6: PRECIO PROMEDIO POR CATEGORÍA EN EUR (si existe la columna)
if 'categoria_general' in df_filtrado.columns:
    st.markdown('<div class="sub-header">💎 Precio Promedio por Categoría (EUR)</div>', unsafe_allow_html=True)
    
    # Calcular promedios en EUR
    precio_categoria_eur = df_filtrado.groupby(['categoria_general', 'país'])['precio_eur'].agg(['mean', 'count']).round(2)
    precio_categoria_eur = precio_categoria_eur.reset_index()
    
    fig_bar = px.bar(
        precio_categoria_eur,
        x='categoria_general',
        y='mean',
        color='país',
        barmode='group',
        title='Precio Promedio por Categoría General<br><sub>Comparación directa en EUR - Precios convertidos</sub>',
        labels={'mean': 'Precio Promedio (EUR)', 'categoria_general': 'Categoría General'},
        color_discrete_sequence=['#2C5530', '#4A7C59'],
        hover_data=['count']
    )
    
    fig_bar.update_traces(
        texttemplate='%{y:.2f}€',
        textposition='outside'
    )
    
    fig_bar.update_layout(
        template='plotly_white',
        xaxis_tickangle=-45,
        showlegend=True,
        yaxis_title='Precio Promedio (EUR)'
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

# RESUMEN EJECUTIVO
st.markdown("---")
st.markdown('<div class="sub-header">📋 Resumen Ejecutivo</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🔍 Métodología:**
    - Análisis comparativo España vs Rumanía
    - Precios convertidos a EUR (1€ = 5.03 LEI)
    - Clasificación por gamas: Baja (≤8€), Media (≤15€), Alta (>15€)
    - Datos normalizados para comparación directa
    """)

with col2:
    st.success("""
    **💡 Insights Clave:**
    - Distribución de portfolio por categorías
    - Comparativa de estructuras de precios
    - Análisis de accesibilidad por mercado
    - Identificación de diferencias estratégicas
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 0.9rem; padding: 2rem 0;'>"
    "NALA — Cosmética | "
    "Análisis de Mercados España-Rumanía | 2025"
    "</div>", 
    unsafe_allow_html=True
)