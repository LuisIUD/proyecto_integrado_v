# main.py (corregido)
from custom_logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller

def main():
    print("Iniciando pipeline")

    # Inicializar componentes
    logger = Logger()  # ← CORREGIDO
    collector = Collector(logger)
    enricher = Enricher(logger)
    modeller = Modeller(logger)

    # Recolección de datos
    df = collector.collector_data()
    if df.empty:
        print("No se pudieron recolectar datos.")
        return
    print("Datos recolectados")

    # Enriquecimiento
    df = enricher.formatear_fechas(df)
    print("Fechas formateadas")

    df = enricher.calcular_kpi(df)
    print("KPIs calculados")

    df_enriquecido = enricher.enriquecer_con_macro(df)
    print("Datos macroeconómicos añadidos")

    df_enriquecido = enricher.establecer_fecha_como_indice(df_enriquecido)
    print("Índice de fecha establecido")

    # Entrenamiento
    print("Iniciando entrenamiento del modelo...")
    modeller.entrenar(df_enriquecido)
    print("Entrenamiento completado y modelo guardado")

    # Predicción
    prediccion, fecha_pred = modeller.predecir(df_enriquecido)
    if prediccion is not None and fecha_pred is not None:
        print(f" Predicción del precio de cierre para {fecha_pred}: {prediccion:.2f}")

        # Crear nueva fila con la predicción
        import pandas as pd
        nueva_fila = {
            'abrir': None,
            'max': None,
            'min': None,
            'cerrar': None,
            'cierre_ajustado': None,
            'volumen': None,
            'ticker': 'GOOG',
            'year': fecha_pred.year,
            'month': fecha_pred.month,
            'day': fecha_pred.day,
            'year_month': fecha_pred.strftime('%Y-%m'),
            'retorno_log_diario': None,
            'media_movil_7d': None,
            'media_movil_30d': None,
            'volatilidad_7d': None,
            'volatilidad_30d': None,
            'ixic_cerrar': None,
            'prediccion_modelo': prediccion
        }

        fila_pred = pd.DataFrame([nueva_fila], index=[fecha_pred])
        df_enriquecido = pd.concat([df_enriquecido, fila_pred])
        df_enriquecido.sort_index(inplace=True)

        df_enriquecido.to_csv("src/edu_piv/static/data/df_enriquecido_con_prediccion.csv")
        print("Archivo con predicción guardado en: src/edu_piv/static/data/df_enriquecido_con_prediccion.csv")
    else:
        print(" No se pudo realizar la predicción.")

if __name__ == "__main__":
    main()
