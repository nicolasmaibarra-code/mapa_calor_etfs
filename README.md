<img width="1273" height="502" alt="image" src="https://github.com/user-attachments/assets/9a18143d-d08a-43f9-979b-8e2c407c765f" /># Monitor de Rendimientos de Mercado

Aplicación web interactiva desarrollada con **Streamlit** para visualizar y comparar el rendimiento porcentual de activos financieros (ETFs y acciones) en un período definido. Sin bases de datos externas, sin complejidad innecesaria.

---

## Demo

> <img width="1273" height="502" alt="image" src="https://github.com/user-attachments/assets/2f44ff74-8de4-434d-8245-64d2bedc0dff" />


---

## Funcionalidades

- **Mapa de calor interactivo** — Visualización con Plotly para identificar de un vistazo los activos con mejor y peor desempeño.
- **Entrada dinámica de activos** — Tickers predefinidos o ingreso manual de cualquier símbolo compatible con Yahoo Finance (ej: `AAPL`, `MSFT`, `BTC-USD`).
- **Rango de fechas flexible** — Selector de calendario para definir el período exacto de análisis.
- **Caché de datos** — Uso de `st.cache_data` para evitar descargas redundantes y mejorar la velocidad.
- **Diseño responsivo** — Compatible con navegadores de escritorio y móviles.

---

## Requisitos

- Python 3.10 o superior

| Librería | Uso |
|---|---|
| `streamlit` | Interfaz web |
| `yfinance` | Datos de mercado vía Yahoo Finance |
| `pandas` | Procesamiento y limpieza de datos |
| `plotly` | Generación del mapa de calor |

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo

# 2. (Recomendado) Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run mapa_calor_etfs.py
```

---

## Estructura del repositorio

```
.
├── mapa_calor_etfs.py   # Script principal: lógica de datos e interfaz
└── requirements.txt     # Dependencias para despliegue local o en Streamlit Cloud
```

---

## Notas técnicas

- El rendimiento se calcula **punta a punta**: precio de cierre del primer día disponible vs. último día del rango seleccionado.
- Si se selecciona un solo activo, la app ajusta la visualización para evitar errores de dimensiones en la matriz de Plotly y muestra un indicador métrico adicional.

---

## Referencias

- [Documentación de Streamlit](https://docs.streamlit.io)
- [yfinance — Yahoo Finance API](https://github.com/ranaroussi/yfinance)
- [Plotly Python Open Source Graphing Library](https://plotly.com/python/)
