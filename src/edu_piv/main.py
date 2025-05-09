from logger import Logger
from collector import Collector
import pandas as pd

def main():
    # Inicializar el logger
    logger = Logger()
    logger.info("Inicializando clase Logger")

    # Crear instancia del recolector de datos
    collector = Collector(logger=logger)

    # Descargar los datos
    df = collector.collector_data()

    # Verificar si se obtuvieron datos y guardarlos
    if df.empty:
        print("[ADVERTENCIA] No se descargaron datos. Revisa los logs.")
        logger.warning("No se descargaron datos. El DataFrame está vacío.")
    else:
        print("[OK] Datos descargados exitosamente.")
        logger.info("Datos descargados exitosamente. Guardando en CSV...")

        # Guardar los datos en CSV con ruta relativa
        df.to_csv("src/edu_piv/static/data/goog_data.csv", index=False)

        logger.info("Archivo CSV guardado correctamente.")

if __name__ == "__main__":
    main()
