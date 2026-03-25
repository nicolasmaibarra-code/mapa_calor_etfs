Monitor de Rendimientos de Mercado
Esta aplicación web interactiva, desarrollada con Streamlit, permite visualizar y analizar el rendimiento porcentual de diferentes activos financieros (ETFs y acciones) en un periodo de tiempo determinado. El objetivo es ofrecer una interfaz limpia y asertiva para comparar variaciones de precio sin la complejidad de gestionar bases de datos externas.

Funcionalidades
Mapa de calor interactivo: Visualización dinámica mediante Plotly que permite identificar rápidamente los activos con mejor y peor desempeño.

Entrada dinámica de activos: Permite seleccionar tickers predefinidos o ingresar manualmente cualquier símbolo compatible con Yahoo Finance (ej: AAPL, MSFT, BTC-USD).

Rango de fechas flexible: Selector de calendario para definir el periodo exacto de análisis.

Optimización de carga: Implementación de caché de datos (st.cache_data) para evitar descargas redundantes y mejorar la velocidad de respuesta.

Diseño Responsivo: La interfaz se adapta a navegadores de escritorio (Windows) y dispositivos móviles (iOS).

Requisitos previos
Para ejecutar este proyecto localmente, necesitás tener instalado Python 3.10 o superior. Las dependencias principales son:

streamlit: Para la interfaz web.

yfinance: Para la obtención de datos de mercado en tiempo real.

pandas: Para el procesamiento y limpieza de datos.

plotly: Para la generación del mapa de calor interactivo.

Instalación y ejecución
Cloná el repositorio:

Bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
Instalá las dependencias:
Corré el siguiente comando en tu terminal (recomendado usar un entorno virtual):

Bash
pip install -r requirements.txt
Iniciá la aplicación:

Bash
streamlit run mapa_calor_etfs.py
Estructura del repositorio
mapa_calor_etfs.py: Script principal que contiene la lógica de extracción de datos y la interfaz de usuario.

requirements.txt: Listado de librerías de Python necesarias para el despliegue en Streamlit Cloud u otros servidores.

Notas técnicas
El cálculo de rendimiento es "punta a punta", comparando el precio de cierre de la primera fecha disponible contra el de la última fecha del rango seleccionado.

En caso de seleccionar un solo activo, la aplicación ajusta la visualización para evitar errores de dimensiones en la matriz de Plotly y muestra un indicador métrico adicional.

Fuentes y recursos
Documentación de Streamlit

Yahoo Finance API (yfinance)

Plotly Python Open Source Graphing Library
