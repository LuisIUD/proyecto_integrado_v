from logger import Logger
from collector import Collector
import pandas as pd

def main():
    logger = Logger()
    logger.info("Inicializando clase Logger")
    collector = Collector(logger=logger)
    df = collector.collector_data()

    if df.empty:
        print("⚠️ No se descargaron datos. Revisa los logs.")
    else:
        print("✅ Datos descargados exitosamente.")
        df.to_csv("src/edu_piv/static/data/goog_data.csv", index=False)

if __name__ == "__main__":
    main()
