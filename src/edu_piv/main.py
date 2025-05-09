import os
import pandas as pd
from logger import Logger
from collector import Collector
import sqlite3

def main():
    logger = Logger()
    logger.info('Main', 'main', 'Inicializando el proceso de descarga y almacenamiento.')

    # Instanciamos el colector para descargar los datos
    collector = Collector(logger=logger)
    df = collector.collertor_data()

    # Definir el path para CSV
    csv_path = "src/edu_piv/static/data/goog_data.csv"

    # Si ya existe el archivo CSV, leemos el histórico y agregamos los nuevos datos sin perder el histórico
    if os.path.exists(csv_path):
        df_historico = pd.read_csv(csv_path)
        df = pd.concat([df_historico, df], ignore_index=True)
        df.drop_duplicates(subset=['fecha'], inplace=True)  # Evita duplicados por fecha
        df.sort_values(by='fecha', inplace=True)
        logger.info('Main', 'main', 'Datos históricos preservados y nuevos datos agregados.')

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(csv_path, index=False)
    logger.info('Main', 'main', f'Datos guardados en {csv_path}.')

    # Opción de guardar en base de datos SQLite (opcional)
    db_path = 'src/edu_piv/static/data/historical.db'
    conn = sqlite3.connect(db_path)
    df.to_sql('historical_data', conn, if_exists='replace', index=False)
    conn.close()
    logger.info('Main', 'main', f'Datos guardados en SQLite en {db_path}.')

    print("Datos descargados y almacenados exitosamente.")

if __name__ == "__main__":
    main()
