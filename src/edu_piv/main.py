from logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller
import pandas as pd

if __name__ == "__main__":
    logger = Logger()

    # Recolección de datos
    collector = Collector(logger)
    df = collector.collector_data()

    if df.empty:
        logger.error("main", "__main__", "No se pudo recolectar data")
    else:
        enricher = Enricher(logger)

        # 1. Formatear fechas
        df = enricher.formatear_fechas(df)
        print("[OK] Fechas formateadas")
        print("[DEBUG] Shape tras formatear fechas:", df.shape)

        # 2. Enriquecer datos cruzando GOOG con IXIC
        df = enricher.enriquecer_con_macro(df)
        print("[OK] Datos cruzados con IXIC")
        print("[DEBUG] Shape tras fusionar con IXIC:", df.shape)

        # 3. Filtrar solo datos de GOOG ya enriquecidos
        df = df[df['ticker'] == 'GOOG'].copy()

        # 4. Calcular KPIs (ya sobre GOOG + ixic_cerrar)
        df = enricher.calcular_kpi(df)
        print("[OK] KPIs calculados")
        print("[DEBUG] Shape tras calcular KPIs:", df.shape)

        # 5. Establecer índice temporal
        df = enricher.establecer_fecha_como_indice(df)
        print("[OK] Índice temporal establecido")
        print("[DEBUG] Shape tras establecer índice:", df.shape)

        if df.empty:
            logger.error("main", "__main__", "Error: El DataFrame quedó vacío tras el enriquecimiento")
        else:
            # 6. Entrenamiento y predicción
            modeller = Modeller(logger)
            entrenado = modeller.entrenar_df(df)

            if entrenado:
                df, ok, valor_predicho, fecha_pred, fila = modeller.predecir_df(df)
                if ok:
                    print(f"[RESULT] Predicción del precio de cierre del próximo día ({fecha_pred}): ${valor_predicho:.2f}")
                else:
                    print("[ERROR] Falló la predicción")
            else:
                print("[ERROR] Falló el entrenamiento del modelo")

            # 7. Guardar CSV con los datos enriquecidos finales
            df.to_csv("src/edu_piv/static/data/goog_datos_enriquecidos.csv", index=True)
            print("[OK] Datos enriquecidos guardados")

