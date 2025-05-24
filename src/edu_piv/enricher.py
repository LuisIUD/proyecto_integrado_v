import numpy as np
import pandas as pd


class Enricher:
    def __init__(self, logger):
        self.logger = logger

    def calcular_kpi(self, df=pd.DataFrame()):
        try:
            df = df.copy()
            df = df.sort_values('fecha')

            for col in df.columns:
                if col not in ["fecha", "ticker"]:
                    if df[col].dtype == 'object':
                        df[col] = pd.to_numeric(df[col].str.replace(',', '.', regex=False), errors='coerce')
                    else:
                        df[col] = pd.to_numeric(df[col], errors='coerce')

            # KPIs
            df['volatilidad'] = df['cerrar'].rolling(window=5).std().fillna(0)
            df['retorno_diario'] = df['cerrar'].pct_change().fillna(0)
            df['retorno_acumulado'] = (1 + df['retorno_diario']).cumprod() - 1
            df['media_movil_10'] = df['cerrar'].rolling(window=10).mean().fillna(method='bfill')
            df['desviacion_std_10'] = df['cerrar'].rolling(window=10).std().fillna(0)
            df['tasa_variacion'] = df['cerrar'].diff().fillna(0)

            self.logger.info('Enricher', 'calcular_kpi', 'Indicadores KPI agregados')
            return df
        except Exception as errores:
            self.logger.error('Enricher', 'calcular_kpi', f'Error al enriquecer el df: {errores}')
            return pd.DataFrame()

    def formatear_fechas(self, df, columna_fecha='fecha'):
            try:
                self.logger.info('Enricher', 'formatear_fechas', 'Iniciando formateo de fechas')
                df_resultado = df.copy()

                # Detectar si las fechas ya están en formato YYYY-MM-DD
                if df_resultado[columna_fecha].str.contains(r'\d{4}-\d{2}-\d{2}').all():
                    df_resultado['fecha_dt'] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')
                else:
                    # Aplicar lógica original de conversión desde '12 may 2024'
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

