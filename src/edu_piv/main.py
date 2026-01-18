import pandas as pd
from datetime import datetime
from collector import Collector
from enricher import Enricher
from modeller import Modeller
from custom_logger import Logger

"""
Pipeline ETL orquestador.
Responsable de coordinar los distintos componentes del flujo de datos
en un entorno automatizado mediante CI/CD.
"""

def main():
    logger = Logger("GOOGAnalysis")

    print("Iniciando pipeline")
    logger.info("Main", "main", "Pipeline iniciado")

    # Paso 1: Recolección de datos
    collector = Collector(logger)
    df_data = collector.collector_data(["GOOG", "IXIC"])
    print("Datos recolectados")

    # Paso 2: Enriquecimiento
    enricher = Enricher(logger)
    df_data = enricher.formatear_fechas(df_data)
    print("Fechas formateadas")

    df_data = enricher.calcular_kpi(df_data)
    print("KPIs calculados")

    # Guardar CSV enriquecido solo para GOOG
    df_data[df_data["ticker"] == "GOOG"].to_csv("src/edu_piv/static/data/goog_datos_enriquecidos.csv", index=False)
    print("CSV enriquecido guardado")

    df_data = enricher.enriquecer_con_macro(df_data)
    print("Datos macroeconómicos añadidos")

    df_data = enricher.establecer_fecha_como_indice(df_data)
    print("Índice de fecha establecido")


    # Paso 3: Modelado
    print("Iniciando entrenamiento del modelo...")
    model = Modeller(logger)
    model.entrenar(df_data)
    print("Entrenamiento completado y modelo guardado")

    # Paso 4: Predicción
    print("Iniciando predicción...")
    y_pred, fecha_pred = model.predecir(df_data)

    if fecha_pred is None or y_pred is None:
        logger.error("Main", "main", "No se pudo generar la predicción.")
        print("No se pudo generar la predicción.")
        return

    # Asegurar que fecha_pred sea datetime.date
    if isinstance(fecha_pred, str):
        try:
            fecha_pred = datetime.strptime(fecha_pred, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Main", "main", f"Formato de fecha no válido: {fecha_pred}")
            print(f"Formato de fecha no válido: {fecha_pred}")
            return
    elif isinstance(fecha_pred, datetime):
        fecha_pred = fecha_pred.date()

    print(f" Predicción del precio de cierre para {fecha_pred}: {y_pred:.2f}")

    # Guardar la predicción
    pred_df = pd.DataFrame([{
        'fecha': fecha_pred,
        'prediccion': y_pred,
        'year': fecha_pred.year,
        'month': fecha_pred.month,
        'day': fecha_pred.day
    }])
    pred_df.to_csv("src/edu_piv/static/data/prediccion.csv", index=False)

    logger.info("Main", "main", "Pipeline finalizado")
    print("Pipeline finalizado")

if __name__ == "__main__":
    main()
