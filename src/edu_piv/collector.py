import requests
import pandas as pd
from bs4 import BeautifulSoup
from edu_piv.custom_logger import Logger
import os

class Collector:
    def __init__(self, logger):
        self.logger = logger
        self.urls = {
            'GOOG': 'https://es.finance.yahoo.com/quote/GOOG/history/',
            'IXIC': 'https://es.finance.yahoo.com/quote/%5EIXIC/history'
        }
        os.makedirs('src/edu_piv/static/data', exist_ok=True)

    def _scrape_yahoo_table(self, url, ticker):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.logger.error("Collector", "_scrape_yahoo_table", f"Error {response.status_code} para {ticker}")
                return pd.DataFrame()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None:
                self.logger.error("Collector", "_scrape_yahoo_table", f"Tabla no encontrada para {ticker}")
                return pd.DataFrame()

            headers_raw = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []
            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(headers_raw):
                    rows.append(columns)

            df = pd.DataFrame(rows, columns=headers_raw)

            # Renombrar columnas según Yahoo en español
            df.rename(columns={
                'Fecha': 'fecha',
                'Abrir': 'abrir',
                'Máx.': 'max',
                'Mín.': 'min',
                'Cerrar*': 'cerrar',
                'Cierre ajustado**': 'cierre_ajustado',
                'Volumen': 'volumen'
            }, inplace=True)

            # Limpiar y estandarizar todos los nombres
            df.columns = [col.strip().lower().replace(' ', '_').replace('*', '').replace('**', '') for col in df.columns]

            # Corregir encabezados rotos si vienen de forma incorrecta
            df.rename(columns={
                'cerrarprecio_de_cierre_ajustado_para_splits.': 'cerrar',
                'cierre_ajustadoprecio_de_cierre_ajustado_para_splits_y_distribuciones_de_dividendos_o_plusvalías.': 'cierre_ajustado'
            }, inplace=True)

            # Validar columnas mínimas requeridas
            columnas_requeridas = ['fecha', 'abrir', 'max', 'min', 'cerrar', 'cierre_ajustado', 'volumen']
            faltantes = [col for col in columnas_requeridas if col not in df.columns]
            if faltantes:
                self.logger.error("Collector", "_scrape_yahoo_table", f"Faltan columnas requeridas: {faltantes}")
                return pd.DataFrame()

            df['ticker'] = ticker

            # Limpiar y convertir números
            df = self._limpiar_numeros(df)

            # Guardar CSV individual
            output_path = f"src/edu_piv/static/data/{ticker.lower()}_datos.csv"
            df.to_csv(output_path, index=False)
            self.logger.info("Collector", "_scrape_yahoo_table", f"Datos guardados en {output_path}")

            return df

        except Exception as e:
            self.logger.error("Collector", "_scrape_yahoo_table", f"Error para {ticker}: {e}")
            return pd.DataFrame()

    def _limpiar_numeros(self, df):
        columnas_numericas = ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado', 'volumen']
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('.', '', regex=False)  # elimina puntos de miles
                df[col] = df[col].str.replace(',', '.', regex=False)             # cambia coma decimal a punto
                df[col] = pd.to_numeric(df[col], errors='coerce')                # convierte a float
        return df

    def collector_data(self):
        df_list = []
        for ticker, url in self.urls.items():
            df = self._scrape_yahoo_table(url, ticker)
            if not df.empty:
                df_list.append(df)

        if not df_list:
            self.logger.warning("Collector", "collector_data", "No se pudieron recolectar datos.")
            return pd.DataFrame()

        df_all = pd.concat(df_list)
        self.logger.info("Collector", "collector_data", f"Datos recolectados para tickers: {list(self.urls.keys())}")
        return df_all
