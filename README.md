# 📈 Análisis Financiero con Machine Learning y Visualización Interactiva

Este proyecto implementa un pipeline completo para la recolección, procesamiento, modelado y visualización de datos financieros utilizando Python y Power BI. El objetivo es analizar el comportamiento de acciones como GOOG (Google) y el índice NASDAQ (IXIC), generar KPIs relevantes y construir un dashboard interactivo que permita comprender los patrones de mercado y ayudar en la toma de decisiones.

---

## 🧠 Estructura del Proyecto


.
├── data/                     # Datos crudos y enriquecidos
├── src/
│   ├── main.py               # Script principal que ejecuta el pipeline completo
│   ├── collector.py          # Clase Collector para obtener datos desde Yahoo Finance
│   ├── enricher.py           # Clase Enricher para calcular KPIs y enriquecer los datos
│   └── modeller.py           # Clase Modeller para entrenamiento y evaluación de modelos
├── dashboard/
│   └── dashboard_financiero_KPIs.pbix  # Dashboard de Power BI con KPIs interactivos
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
⚙️ Pipeline del Proyecto
1. Recolección de datos
Descarga de datos financieros históricos usando yfinance

Activos utilizados: GOOG y IXIC

2. Enriquecimiento y Cálculo de KPIs
Calcula los siguientes indicadores:

Tasa de variación

Media móvil (7 y 30 días)

Volatilidad (7 y 30 días)

Retorno acumulado

Retorno logarítmico diario

Desviación estándar (10 días)

3. Modelado
Predicción de tendencias o valores futuros con modelos de Machine Learning (en progreso o configurado en modeller.py).

4. Visualización (Power BI)
Dashboard interactivo con gráficos de evolución temporal para cada KPI.

📊 Dashboard Interactivo
El dashboard está implementado en Power BI e incluye:

Gráficos de línea para cada KPI

Interactividad por fecha

Visualización clara y organizada de:

Media móvil

Volatilidad

Retorno logarítmico

Cierre ajustado

Tasa de variación

📁 Archivo del dashboard:
dashboard/dashboard_financiero_KPIs.pbix

🧪 Requisitos
Instala las dependencias con:

pip install -r requirements.txt
▶️ Ejecución del Pipeline
Para correr todo el flujo desde consola:


python src/main.py
Esto generará un archivo enriquecido en data/ con los KPIs listos para cargar en Power BI.

✅ Estado del Proyecto
 Recolección de datos

 Cálculo de KPIs

 Integración con IXIC

 Visualización Power BI

 Modelado avanzado