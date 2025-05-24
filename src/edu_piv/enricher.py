import numpy as np
import pandas as pd

class Enricher:
    def __init__(self, logger):
        self.logger = logger

    def calcular_kpi(self, df=pd.DataFrame()):
        try:
            df = df.copy()
            df = df.sort_values('fecha')

            cols_numericas = [col for col in df.columns if col not in ["fecha", "ticker"]]

            for col in cols_numericas:
                if df[col].dtype == 'object':
                    df[col] = (
                        df[col]
                        .str.replace('.', '', regex=False)
                        .str.replace(',', '.', regex=False)
                    )
                df[col] = pd.to_numeric(df[col], errors='coerce')

            if 'cerrar' in df.columns:
                df['retorno_log_diario'] = np.log(df['cerrar'] / df['cerrar'].shift(1)).fillna(0)
                df['media_movil_7d'] = df['cerrar'].rolling(window=7).mean().fillna(method='bfill')
                df['media_movil_30d'] = df['cerrar'].rolling(window=30).mean().fillna(method='bfill')
                df['volatilidad_7d'] = df['retorno_log_diario'].rolling(window=7).std().fillna(0)
                df['volatilidad_30d'] = df['retorno_log_diario'].rolling(window=30).std().fillna(0)
                self.logger.info('Enricher', 'calcular_kpi', 'Indicadores KPI agregados')
            else:
                self.logger.warning('Enricher', 'calcular_kpi', "Columna 'cerrar' no encontrada para KPIs")

            return df

        except Exception as errores:
            self.logger.error('Enricher', 'calcular_kpi', f'Error al enriquecer el df: {errores}')
            return pd.DataFrame()

    def formatear_fechas(self, df, columna_fecha='fecha'):
        try:
            self.logger.info('Enricher', 'formatear_fechas', 'Iniciando formateo de fechas')
            df_resultado = df.copy()

            if df_resultado[columna_fecha].str.contains(r'\d{4}-\d{2}-\d{2}').all():
                df_resultado['fecha_dt'] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')
            else:
                meses = {
                    'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06',
                    'jul': '07', 'ago': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
                }

                def convertir_fecha(fecha_str):
                    if pd.isna(fecha_str) or not isinstance(fecha_str, str):
                        return None
                    fecha_str = fecha_str.strip('"').strip()
                    partes = fecha_str.split()
                    if len(partes) != 3:
                        return None
                    dia, mes_abr, año = partes
                    mes_abr = mes_abr.lower()
                    if mes_abr in meses:
                        dia = dia.zfill(2)
                        return f"{año}-{meses[mes_abr]}-{dia}"
                    return None

                df_resultado[columna_fecha] = df_resultado[columna_fecha].apply(convertir_fecha)
                df_resultado['fecha_dt'] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')

            return self.completar_columnas(df_resultado, columna_fecha)

        except Exception as e:
            self.logger.error('Enricher', 'formatear_fechas', f'Error al formatear fechas: {str(e)}')
            return df

    def completar_columnas(self, df, columna_fecha):
        try:
            df['year'] = df['fecha_dt'].dt.year.astype('Int64')
            df['month'] = df['fecha_dt'].dt.month.astype('Int64')
            df['day'] = df['fecha_dt'].dt.day.astype('Int64')
            df['year_month'] = df['fecha_dt'].dt.strftime('%Y-%m')
            df.drop('fecha_dt', axis=1, inplace=True)
            self.logger.info('Enricher', 'completar_columnas', 'Columnas year, month, day y year_month agregadas')
            return df

        except Exception as e:
            self.logger.error('Enricher', 'completar_columnas', f'Error al completar columnas: {str(e)}')
            if 'fecha_dt' in df.columns:
                df.drop('fecha_dt', axis=1, inplace=True)
            return df

    def establecer_fecha_como_indice(self, df, columna_fecha='fecha'):
        try:
            df_resultado = df.copy()

            if columna_fecha in df_resultado.columns:
                df_resultado[columna_fecha] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')
                df_resultado = df_resultado.dropna(subset=[columna_fecha])
                df_resultado.set_index(columna_fecha, inplace=True)
                df_resultado.sort_index(inplace=True)

                # Verificación extra
                if not isinstance(df_resultado.index[-1], pd.Timestamp):
                    self.logger.warning('Enricher', 'establecer_fecha_como_indice', 'El índice final no es un Timestamp')

                self.logger.info('Enricher', 'establecer_fecha_como_indice', 'Fecha establecida como índice')

            else:
                self.logger.warning('Enricher', 'establecer_fecha_como_indice', f'Columna {columna_fecha} no encontrada')

            return df_resultado

        except Exception as e:
            self.logger.error('Enricher', 'establecer_fecha_como_indice', f'Error al establecer fecha como índice: {str(e)}')
            return df

