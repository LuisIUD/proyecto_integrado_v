import numpy as np
import pandas as pd




class Enricher:
    def __init__(self,logger):
        self.logger = logger

    def calcular_kpi(self,df=pd.DataFrame()): #mínimo 5 KPI (tasa de variación, media móvil, volatilidad, retorno acumulado, desviación estándar, etc.).
        try:
          df = df.copy()
          # ordenar
          df = df.sort_values('fecha')
          for col in df.columns:
             if col != "fecha":
                df[col]= pd.to_numeric(df[col].str.replace(',', '.',regex=False),errors='coerce')
          # 1er indicador volatilidad (desviacion de los ult. 5 dias)
          df['volatilidad']=df['cerrar'].rolling(window=5).std().fillna(0)
          self.logger.info('Enricher','calcular_kpi','agregar indicadores KPI')
          return df
        except Exception as errores:
          self.logger.error(f'Enricher','calcular_kpi','Error al enriquecer el df{errores}')
          df=pd.DataFrame()
          return df

    def formatear_fechas(self, df, columna_fecha='fecha'):
        """
        Convierte el formato de fecha, de '07 abr 2004' o '07 may 2025' a 'yyyy-mm-dd'
        y agrega columnas year, month, day.
        """
        self.logger.info('Enricher', 'formatear_fechas', 'Iniciando formateo de fechas')
        df_resultado = df.copy()

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

        try:
            df_resultado[columna_fecha] = df_resultado[columna_fecha].apply(convertir_fecha)
            df_resultado['fecha_dt'] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')
            self.logger.info('Enricher', 'formatear_fechas', 'Extrayendo componentes de fecha')
            return self.completar_columnas(df_resultado, columna_fecha)

        except Exception as e:
            self.logger.error('Enricher', 'formatear_fechas', f'Error al formatear fechas: {str(e)}')
            return df

    def completar_columnas(self, df, columna_fecha):
        """
        Agrega las columnas year, month, day como enteros y year_month en formato yyyy-mm
        """
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
        """
        Establece la columna fecha como índice del DataFrame
        """
        try:
            df_resultado = df.copy()
            if columna_fecha in df_resultado.columns:
                df_resultado[columna_fecha] = pd.to_datetime(df_resultado[columna_fecha], errors='coerce')
                df_resultado.set_index(columna_fecha, inplace=True)
                self.logger.info('Enricher', 'establecer_fecha_como_indice', 'Fecha establecida como índice')
            else:
                self.logger.warning('Enricher', 'establecer_fecha_como_indice', f'Columna {columna_fecha} no encontrada')
            return df_resultado

        except Exception as e:
            self.logger.error('Enricher', 'establecer_fecha_como_indice', f'Error al establecer fecha como índice: {str(e)}')
            return df
