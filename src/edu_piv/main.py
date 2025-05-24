from logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller  # Asegúrate que el archivo se llama modeller.py
import pandas as pd
import os


def main():
    logger = Logger()

    # Paso 1: Recolección de datos
    collector = Collector(logger)
    df_crudo = collector.recolectar('GOOG', '2020-01-01', '2023-12-31')
    if df_crudo.empty:
        logger.error("Main", "main", "No se recolectaron datos.")
        return

    # Paso 2: Enriquecimiento
    enricher = Enricher(logger)
    df_enriquecido = enricher.formatear_fechas(df_crudo)
    df_enriquecido = enricher.cruzar_con_ixic(df_enriquecido)
    df_enriquecido = enricher.calcular_kpis(df_enriquecido)
    df_enriquecido = enricher.establecer_indice_temporal(df_enriquecido)

    if df_enriquecido.empty:
        logger.error("Main", "main", "El DataFrame enriquecido está vacío.")
        return

    # Guardar datos enriquecidos
    path_guardado = os.path.join(os.path.dirname(__file__), 'static', 'data', 'df_enriquecido.csv')
    os.makedirs(os.path.dirname(path_guardado), exist_ok=True)
    df_enriquecido.to_csv(path_guardado, index=False)
    logger.info("Main", "main", f"Datos enriquecidos guardados en {path_guardado}")

    # Paso 3: Modelado
    modeller = Modeller(logger)
    entrenado = modeller.entrenar(df_enriquecido, ticker='GOOG')

    if not entrenado:
        logger.error("Main", "main", "Falló el entrenamiento del modelo.")
        return

    # Paso 4: Predicción
    prediccion, fecha = modeller.predecir(df_enriquecido, ticker='GOOG')
    if prediccion is not None:
        logger.info("Main", "main", f"Predicción para {fecha}: {prediccion:.2f}")
    else:
        logger.error("Main", "main", "No se pudo realizar la predicción.")


if __name__ == "__main__":
    main()
