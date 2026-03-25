import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Heatmap de ETFs", layout="wide")

st.title("Mapa de Calor de Rendimientos")

# --- Barra Lateral (Inputs) ---
st.sidebar.header("Configuración")

# Selección de tickers (puedes poner los que quieras por defecto)
# Tickers que aparecerán marcados por defecto
default_tickers = ['ICLN', 'TAN', 'QCLN', 'PBW', 'FAN', 'ACES', 'SPY']

# Tickers sugeridos adicionales
opciones_sugeridas = ['QQQ', 'DIA', 'ARKK', 'MELI']

# Campo para ingresar tickers manualmente (ej: AAPL, MSFT)
entrada_manual = st.sidebar.text_input("Agregar otros tickers (separados por coma)", "").upper()
tickers_manuales = [t.strip() for t in entrada_manual.split(",") if t.strip()]

# Combinar las listas y eliminar duplicados
opciones_completas = sorted(list(set(default_tickers + opciones_sugeridas + tickers_manuales)))

# El multiselect ahora incluye las opciones manuales ingresadas
tickers = st.sidebar.multiselect(
    "Seleccioná los tickers", 
    options=opciones_completas, 
    default=default_tickers
)

# Selección de fechas
col1, col2 = st.sidebar.columns(2)
with col1:
    fecha_inicio = st.date_input("Inicio", datetime.now() - timedelta(days=365))
with col2:
    fecha_fin = st.date_input("Fin", datetime.now())

# --- Lógica de Datos ---
@st.cache_data(ttl=3600) # Guarda los datos por 1 hora para no saturar la API
def obtener_datos(lista_tickers, inicio, fin):
    if not lista_tickers:
        return None
    
    # Descarga masiva para ser más eficiente
    datos = yf.download(lista_tickers, start=inicio, end=fin, progress=False)
    if datos.empty:
        return None
    
    # Si es un solo ticker, yfinance devuelve un formato distinto, normalizamos
    precios = datos['Close']
    if len(lista_tickers) == 1:
        precios = precios.to_frame()
        precios.columns = lista_tickers

    # Cálculo de rendimientos totales en el periodo
    rendimientos = {}
    for t in lista_tickers:
        serie = precios[t].dropna()
        if len(serie) > 1:
            ret = (serie.iloc[-1] / serie.iloc[0]) - 1
            rendimientos[t] = ret
            
    return pd.DataFrame.from_dict(rendimientos, orient='index', columns=['Rendimiento'])

# --- Visualización ---
if tickers:
    df_ret = obtener_datos(tickers, fecha_inicio, fecha_fin)
    
    if df_ret is not None:
        st.subheader(f"Rendimientos del {fecha_inicio} al {fecha_fin}")
        
        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, len(tickers) * 0.5 + 2))
        sns.heatmap(
            df_ret, 
            annot=True, 
            fmt=".2%", 
            cmap='RdYlGn', 
            center=0, 
            cbar_kws={'label': 'Rendimiento %'},
            ax=ax
        )
        ax.set_title("Variación Porcentual")
        
        # Mostrar en Streamlit
        st.pyplot(fig)
        
        # Tabla de datos crudos opcional
        with st.expander("Ver tabla de datos"):
            st.write(df_ret)
    else:
        st.warning("No se encontraron datos para los tickers o fechas seleccionadas.")
else:
    st.info("Seleccioná al menos un ticker en la barra lateral para empezar.")
