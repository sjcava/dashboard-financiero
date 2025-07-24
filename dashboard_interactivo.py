import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Configuración de la Página ---
st.set_page_config(layout="wide", page_title="Dashboard Financiero")

# --- Título del Dashboard ---
st.title("📊 Dashboard Financiero Interactivo")
st.markdown("Este dashboard consolida y presenta análisis financieros clave de forma interactiva.")

# --- Preparación de Datos ---
# Datos consolidados de tus scripts (Gemini.py, bubble-chart-ventas.py, Grafico_Trimestral_DS_V5.py)

# 1. Datos para el Resumen P&L (inspirado en Gemini.py)
pnl_data = {
    'Mes': ['Dic-24', 'Ene-25', 'Feb-25', 'Mar-25', 'Abr-25', 'May-25', 'Jun-25', 'Jul-25'],
    'Ventas': [228857, 210334, 224291, 234264, 222966, 239450, 279327, 145032],
    'Costo de Ventas': [np.nan, 115598, 124581, 136693, 131728, 137145, 157043, 83020],
    'Facturas Generadas': [np.nan, 10741, 12328, 12505, 12378, 13031, 13537, 6823],
    'Unidades Vendidas': [np.nan, 44936, 49605, 51391, 50173, 50364, 53817, 29884]
}
df_pnl = pd.DataFrame(pnl_data)
df_pnl['Utilidad Operativa'] = df_pnl['Ventas'] - df_pnl['Costo de Ventas']
df_pnl['% Utilidad Operativa'] = (df_pnl['Utilidad Operativa'] / df_pnl['Ventas']) * 100
df_pnl['Promedio Unidades por Factura'] = df_pnl['Unidades Vendidas'] / df_pnl['Facturas Generadas']
df_pnl['Crecimiento Ventas'] = df_pnl['Ventas'].pct_change() * 100

# 2. Datos para el Bubble Chart (inspirado en bubble-chart-ventas.py)
farmacia = [[1, 120873], [2, 130167], [3, 135107], [4, 138826], [5, 142470], [6, 150131], [7, 96736]]
miscelaneos = [[1, 58379], [2, 63710], [3, 65781], [4, 67468], [5, 77845], [6, 78124], [7, 33357]]
equipos_medicos = [[1, 19704], [2, 21705], [3, 23592], [4, 24156], [5, 27582], [6, 28743], [7, 14939]]

# 3. Datos para la Comparativa Anual (inspirado en Grafico_Trimestral_DS_V5.py)
comp_meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul"]
comp_data = {
    'Mes': comp_meses,
    '2024': [142891, 135770, 114702, 89007, 187180, 187065, 217887],
    '2024 MTD': [60503, 65440, 69809, 41953, 81763, 94854, 100339],
    '2025 MTD': [89108, 112908, 108825, 136043, 128450, 141758, 145032]
}
df_comp = pd.DataFrame(comp_data)
df_comp['Crecimiento %'] = ((df_comp['2025 MTD'] - df_comp['2024 MTD']) / df_comp['2024 MTD']) * 100

# --- KPIs Principales ---
st.header("KPIs Clave (Último Mes Registrado)")
last_month_data = df_pnl.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas", f"${last_month_data['Ventas']:,.0f}", f"{last_month_data['Crecimiento Ventas']:.1f}% vs mes anterior")
col2.metric("Utilidad Operativa", f"${last_month_data['Utilidad Operativa']:,.0f}")
col3.metric("Facturas Generadas", f"{last_month_data['Facturas Generadas']:,.0f}")
col4.metric("Unidades/Factura", f"{last_month_data['Promedio Unidades por Factura']:.2f}")

st.markdown("---")

# --- Funciones para generar gráficos ---

def plot_ventas_utilidad(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df_plot = df.dropna(subset=['Costo de Ventas'])
    
    fig.add_trace(go.Bar(x=df_plot['Mes'], y=df_plot['Ventas'], name='Ventas', marker_color='#1f77b4'), secondary_y=False)
    fig.add_trace(go.Bar(x=df_plot['Mes'], y=df_plot['Utilidad Operativa'], name='Utilidad Operativa', marker_color='#ff7f0e'), secondary_y=False)
    
    fig.add_trace(go.Scatter(x=df_plot['Mes'], y=df_plot['% Utilidad Operativa'], name='% Utilidad Operativa', marker_color='#d62728', mode='lines+markers'), secondary_y=True)
    
    fig.update_layout(title_text='Ventas y Utilidad Operativa', barmode='group', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title_text="Monto ($)", secondary_y=False)
    fig.update_yaxes(title_text="Porcentaje (%)", secondary_y=True)
    return fig

def plot_facturas_unidades(df):
    fig = go.Figure()
    df_plot = df.dropna(subset=['Facturas Generadas'])
    fig.add_trace(go.Bar(x=df_plot['Mes'], y=df_plot['Facturas Generadas'], name='Facturas Generadas', marker_color='#9467bd'))
    fig.add_trace(go.Scatter(x=df_plot['Mes'], y=df_plot['Unidades Vendidas'], name='Unidades Vendidas', marker_color='#006400', mode='lines+markers', yaxis='y2'))
    
    fig.update_layout(
        title_text='Facturas Generadas y Unidades Vendidas',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title='Cantidad Facturas'),
        yaxis2=dict(title='Cantidad Unidades', overlaying='y', side='right')
    )
    return fig

def plot_crecimiento_tendencia(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df_plot = df.dropna(subset=['Crecimiento Ventas'])
    
    fig.add_trace(go.Bar(x=df_plot['Mes'], y=df_plot['Crecimiento Ventas'], name='% Crecimiento Ventas', marker_color='#e377c2'), secondary_y=False)
    
    # Calcular línea de tendencia
    x_num = np.arange(len(df_plot['Mes']))
    z = np.polyfit(x_num, df_plot['Ventas'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(x=df_plot['Mes'], y=p(x_num), name='Tendencia Ventas', marker_color='black', mode='lines', line=dict(dash='dash')), secondary_y=True)
    
    fig.update_layout(title_text='Crecimiento y Tendencia de Ventas', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title_text="Crecimiento (%)", secondary_y=False)
    fig.update_yaxes(title_text="Tendencia ($)", secondary_y=True)
    return fig

def plot_promedio_unidades(df):
    fig = go.Figure()
    df_plot = df.dropna(subset=['Promedio Unidades por Factura'])
    fig.add_trace(go.Scatter(x=df_plot['Mes'], y=df_plot['Promedio Unidades por Factura'], name='Promedio Unidades/Factura', marker_color='#7f7f7f', mode='lines+markers'))
    fig.update_layout(title_text='Promedio de Unidades por Factura', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title_text="Unidades / Factura")
    return fig

def plot_bubble_categorias():
    fig = go.Figure()
    meses_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 7: 'Jul'}
    
    for cat_data, name, color in [(farmacia, 'Farmacia', 'blue'), (miscelaneos, 'Misceláneos', 'green'), (equipos_medicos, 'Equipos Médicos', 'red')]:
        meses_num = [d[0] for d in cat_data]
        meses_str = [meses_map[m] for m in meses_num]
        ventas = [d[1] for d in cat_data]
        
        fig.add_trace(go.Scatter(
            x=meses_str, y=ventas,
            name=name,
            mode='markers',
            marker=dict(
                size=[v / 5000 for v in ventas], # Escala de burbujas
                sizemin=4,
                color=color,
                showscale=False
            ),
            hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Ventas por Categoría (Bubble Chart)',
        xaxis_title='Mes',
        yaxis_title='Ventas ($)',
        legend_title='Categorías'
    )
    return fig

def plot_comparativa_anual(df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=df['Mes'], y=df['2024'], name='2024', marker_color='#1f77b4'))
    fig.add_trace(go.Bar(x=df['Mes'], y=df['2024 MTD'], name='2024 MTD', marker_color='#ff7f0e'))
    fig.add_trace(go.Bar(x=df['Mes'], y=df['2025 MTD'], name='2025 MTD', marker_color='#2ca02c',
                         text=[f'{c:.1f}%' for c in df['Crecimiento %']], textposition='outside'))
    
    fig.update_layout(
        barmode='group',
        title='Comparativa de Ventas 2025 vs 2024',
        xaxis_title='Mes',
        yaxis_title='Ventas ($)',
        legend_title='Periodo'
    )
    return fig

# --- Creación de Pestañas (Tabs) ---
tab1, tab2, tab3 = st.tabs(["Resumen P&L", "Ventas por Categoría", "Comparativa Anual"])

with tab1:
    st.header("Análisis del Estado de Resultados (P&L)")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_ventas_utilidad(df_pnl), use_container_width=True)
        st.plotly_chart(plot_crecimiento_tendencia(df_pnl), use_container_width=True)
    with col2:
        st.plotly_chart(plot_facturas_unidades(df_pnl), use_container_width=True)
        st.plotly_chart(plot_promedio_unidades(df_pnl), use_container_width=True)

with tab2:
    st.header("Análisis de Ventas por Categoría de Producto")
    st.plotly_chart(plot_bubble_categorias(), use_container_width=True)

with tab3:
    st.header("Análisis Comparativo de Ventas Anuales")
    st.plotly_chart(plot_comparativa_anual(df_comp), use_container_width=True)
