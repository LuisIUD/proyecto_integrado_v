from logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller
import pandas as pd

if __name__ == "__main__":
    # Inicializar logger
    logger = Logger()

    # Recolección de datos
    collector = Collector(logger)
    df = collector.collector_data()

    if df.empty:
        logger.error("main", "__main__", "No se pudo recolectar data")
    else:
        # Enriquecimiento de datos
        enricher = Enricher(logger)
        df = enricher.formatear_fechas(df)
        df = enricher.calcular_kpi(df)
        df = enricher.establecer_fecha_como_indice(df)

        if df.empty:
            logger.error("main", "__main__", "Error al enriquecer los datos")
        else:
            # Entrenamiento y predicción
            modeller = Modeller(logger)

            entrenado = modeller.entrenar_df(df)
            if entrenado:
                df, ok, valor_predicho, fecha_pred, fila = modeller.predecir_df(df)

                if ok:
                    print(f"\n📈 Predicción del precio de cierre del próximo día ({fecha_pred}): ${valor_predicho:.2f}")
                else:
                    print("\n❌ Falló la predicción")
            else:
                print("\n❌ Falló el entrenamiento del modelo")

            # Guardar datos enriquecidos opcionalmente
            df.to_csv("src/edu_piv/static/data/datos_enriquecidos.csv", index=True)
