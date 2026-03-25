import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Heatmap de ETFs", layout="wide")

st.title("Monitor de Rendimientos de Mercado")

# --- Barra Lateral ---
st.sidebar.header("Configuración")

default_tickers = ['ICLN', 'TAN', 'QCLN', 'PBW', 'FAN', 'ACES', 'SPY']
opciones_sugeridas = ['QQQ', 'DIA', 'ARKK', 'MELI']

# Entrada manual de tickers
entrada_manual = st.sidebar.text_input("Agregar otros tickers (separados por coma)", "").upper()
tickers_manuales = [t.strip() for t in entrada_manual.split(",") if t.strip()]

# Combinar y limpiar duplicados
opciones_completas = sorted(list(set(default_tickers + opciones_sugeridas + tickers_manuales)))

tickers = st.sidebar.multiselect(
    "Seleccioná los activos", 
    options=opciones_completas, 
    default=default_tickers
)

col1, col2 = st.sidebar.columns(2)
with col1:
    fecha_inicio = st.date_input("Inicio", datetime.now() - timedelta(days=365))
with col2:
    fecha_fin = st.date_input("Fin", datetime.now())

# --- Obtención de Datos ---
@st.cache_data(ttl=3600)
def obtener_datos(lista_tickers, inicio, fin):
    if not lista_tickers:
        return None
    
    try:
        # Descarga de datos
        datos = yf.download(lista_tickers, start=inicio, end=fin, progress=False)
        if datos.empty:
            return None
        
        # Extraer precios de cierre
        precios = datos['Close']
        
        # Manejo específico para un solo ticker (yfinance devuelve Series en ese caso)
        if len(lista_tickers) == 1:
            if isinstance(precios, pd.Series):
                precios = precios.to_frame()
                precios.columns = lista_tickers

        rendimientos = {}
        for t in lista_tickers:
            if t in precios.columns:
                serie = precios[t].dropna()
                if len(serie) > 1:
                    # Rendimiento punta a punta
                    ret = (serie.iloc[-1] / serie.iloc[0]) - 1
                    rendimientos[t] = ret
            
        return pd.DataFrame.from_dict(rendimientos, orient='index', columns=['Rendimiento']).sort_values(by='Rendimiento', ascending=False)
    except Exception as e:
        st.error(f"Error al procesar datos: {e}")
        return None

# --- Visualización ---
if tickers:
    df_ret = obtener_datos(tickers, fecha_inicio, fecha_fin)
    
    if df_ret is not None and not df_ret.empty:
        st.subheader(f"Variación porcentual ({fecha_inicio} a {fecha_fin})")
        
        # Mapa de calor con Plotly (mucho más estético e interactivo)
        # Transponemos para que los nombres queden en el eje X
        fig = px.imshow(
            [df_ret['Rendimiento']], 
            x=df_ret.index,
            y=[""],
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            aspect="auto",
            text_auto=".2%",
            labels=dict(x="Activo", color="Rendimiento")
        )

        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(title="Rendimiento", tickformat=".0%"),
            xaxis=dict(side="bottom")
        )

        st.plotly_chart(fig, use_container_width=True)

        # Si hay un solo ticker, agregamos un indicador visual extra
        if len(df_ret) == 1:
            ticker_sel = df_ret.index[0]
            valor = df_ret.iloc[0,0]
            st.metric(label=f"Activo: {ticker_sel}", value=f"{valor:.2%}")

    else:
        st.warning("No se encontraron datos para la selección actual.")
else:
    st.info("Seleccioná activos en la barra lateral.")