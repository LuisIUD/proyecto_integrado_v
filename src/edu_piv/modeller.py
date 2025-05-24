import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from logger import Logger


class Modeller:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.model = None

        base_path = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_path, 'static', 'models')
        os.makedirs(models_dir, exist_ok=True)
        self.model_path = os.path.join(models_dir, 'model.pkl')

    def preparar_datos(self, df: pd.DataFrame, ticker: str = 'GOOG'):
        try:
            df = df[df['ticker'] == ticker].copy()
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            df = df.dropna(subset=['fecha']).sort_values(by='fecha').reset_index(drop=True)

            features = [
                'retorno_log_diario',
                'media_movil_7d',
                'media_movil_30d',
                'volatilidad_7d',
                'volatilidad_30d'
            ]

            if not all(col in df.columns for col in features + ['cerrar']):
                self.logger.error("Modeller", "preparar_datos", "Faltan columnas necesarias.")
                return pd.DataFrame(), pd.Series(), False

            X = df[features]
            y = df['cerrar']
            return X, y, True

        except Exception as e:
            self.logger.error("Modeller", "preparar_datos", f"Error preparando datos: {e}")
            return pd.DataFrame(), pd.Series(), False

    def entrenar(self, df: pd.DataFrame, ticker: str = 'GOOG'):
        try:
            X, y, valido = self.preparar_datos(df, ticker)
            if not valido or X.empty or y.empty:
                self.logger.error("Modeller", "entrenar", "Datos insuficientes o inválidos para entrenamiento.")
                return False

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)

            preds = self.model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)

            joblib.dump(self.model, self.model_path)
            self.logger.info("Modeller", "entrenar", f"Modelo guardado en {self.model_path}")
            self.logger.info("Modeller", "entrenar", f"RMSE: {rmse:.4f}, MAE: {mae:.4f}")
            return True

        except Exception as e:
            self.logger.error("Modeller", "entrenar", f"Error en entrenamiento: {e}")
            return False

    def predecir(self, df: pd.DataFrame, ticker: str = 'GOOG'):
        try:
            if self.model is None:
                self.model = joblib.load(self.model_path)
                self.logger.info("Modeller", "predecir", f"Modelo cargado desde {self.model_path}")

            features = [
                'retorno_log_diario',
                'media_movil_7d',
                'media_movil_30d',
                'volatilidad_7d',
                'volatilidad_30d'
            ]

            df_ticker = df[df['ticker'] == ticker].copy()
            X_new = df_ticker[features].tail(1)

            pred = self.model.predict(X_new)[0]
            fecha = df_ticker['fecha'].max().strftime('%Y-%m-%d')

            self.logger.info("Modeller", "predecir", f"Predicción: {pred:.4f} para fecha: {fecha}")
            return pred, fecha

        except Exception as e:
            self.logger.error("Modeller", "predecir", f"Error en predicción: {e}")
            return None, ""
