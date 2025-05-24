from logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller


def main():
    logger = Logger()
    collector = Collector(logger)
    enricher = Enricher(logger)
    modeller = Modeller(logger)

    print("Iniciando pipeline")

    # 1. Recolección de datos
    df_crudo = collector.collector_data()
    if df_crudo.empty:
        logger.error("Main", "main", "No se pudieron recolectar datos. Proceso detenido.")
        print("Recolección fallida")
        return
    print("Datos recolectados")

    # 2. Formatear fechas
    df_crudo = enricher.formatear_fechas(df_crudo)
    print("Fechas formateadas")

    # 3. Calcular indicadores KPI
    df_crudo = enricher.calcular_kpi(df_crudo)
    print("KPIs calculados")

    # 4. Enriquecer con datos macroeconómicos (IXIC)
    df_enriquecido = enricher.enriquecer_con_macro(df_crudo)
    print("Datos macroeconómicos añadidos")

    # 5. Establecer la columna fecha como índice
    df_enriquecido = enricher.establecer_fecha_como_indice(df_enriquecido)
    print("Índice de fecha establecido")

    # 6. Entrenar modelo
    print("Iniciando entrenamiento del modelo...")
    entrenado = modeller.entrenar(df_enriquecido)
    if not entrenado:
        logger.error("Main", "main", "Entrenamiento fallido. Proceso detenido.")
        print("Entrenamiento fallido")
        return
    print("Entrenamiento completado y modelo guardado")

    # 7. Realizar predicción
    prediccion, fecha = modeller.predecir(df_enriquecido)
    if prediccion is not None:
        print(f"Predicción para {fecha}: {prediccion:.2f}")
    else:
        logger.error("Main", "main", "Error al realizar la predicción.")
        print("Error al predecir")


if __name__ == "__main__":
    main()
