from collector import Collector
from enricher import Enricher
from modeller import Modeller

def main():
    print("Iniciando pipeline")
    logger = Logger()  # <- ¡CORREGIDO!

    # Recolectar datos
    collector = Collector(logger)
    df_raw = collector.collector_data()
    print("Datos recolectados")

    # Enriquecer datos
    enricher = Enricher(logger)
    df_fechas = enricher.formatear_fechas(df_raw)
    print("Fechas formateadas")

    df_kpis = enricher.calcular_kpi(df_fechas)
    print("KPIs calculados")

    df_enriquecido = enricher.enriquecer_con_macro(df_kpis)
    print("Datos macroeconómicos añadidos")

    df_final = enricher.establecer_fecha_como_indice(df_enriquecido)
    print("Índice de fecha establecido")

    # Entrenar modelo
    modeller = Modeller(logger)
    modeller.entrenar(df_final)
    print("Entrenamiento completado y modelo guardado")

    # Predecir
    prediccion, fecha = modeller.predecir(df_final)
    print(f"Predicción para la próxima fecha ({fecha}): {prediccion:.2f}")

    # Agregar predicción al DataFrame
    df_final = df_final.copy()
    df_final.loc[fecha] = None  # Crear nueva fila con fecha predicha
    df_final.at[fecha, 'prediccion_cerrar'] = prediccion
    print("Predicción agregada al DataFrame")

    # (Opcional) Guardar el DataFrame enriquecido con predicción
    df_final.to_csv("src/edu_piv/static/data/enriquecido_con_prediccion.csv")
    print("DataFrame final guardado")

if __name__ == "__main__":
    main()
