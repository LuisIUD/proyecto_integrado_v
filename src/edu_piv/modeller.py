import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from logger import Logger

class Modeller:
    def __init__(self, logger):
        self.logger = logger
        self.model_dir = "src/edu_piv/static/models/"
        self.model_path = os.path.join(self.model_dir, "model.pkl")
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def preparar_df(self, df, ticker='GOOG'):
        try:
            self.logger.debug("Modeller", "preparar_df", f"Columnas recibidas: {df.columns.tolist()}")
            df = df[df['ticker'] == ticker].copy()
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            df = df.dropna(subset=['fecha'])
            df = df.sort_values(by='fecha').reset_index(drop=True)

            # Seleccionar solo columnas numéricas para entrenamiento
            df_numerico = df.select_dtypes(include=[np.number])
            self.logger.debug("Modeller", "preparar_df", f"Columnas numéricas: {df_numerico.columns.tolist()}")
            self.logger.debug("Modeller", "preparar_df", f"Shape de df_numerico antes de objetivo: {df_numerico.shape}")

            if 'cerrar' not in df_numerico.columns:
                self.logger.error("Modeller", "preparar_df", "'cerrar' no está en columnas numéricas")
                return pd.DataFrame(), pd.Series(), False, None

            # Crear variable objetivo: precio de cierre del día siguiente
            df_numerico['objetivo'] = df_numerico['cerrar'].shift(-1)
            df_numerico.dropna(inplace=True)

            if df_numerico.empty:
                self.logger.warning("Modeller", "preparar_df", "El DataFrame quedó vacío tras preparar variables.")
                return pd.DataFrame(), pd.Series(), False, None

            self.logger.debug("Modeller", "preparar_df", f"Shape final de df_numerico: {df_numerico.shape}")

            X = df_numerico.drop(columns=['objetivo'])
            y = df_numerico['objetivo']
            return X, y, True, df

        except Exception as e:
            self.logger.error("Modeller", "preparar_df", f"Error preparando dataset: {e}")
            return pd.DataFrame(), pd.Series(), False, None

    def entrenar_df(self, df):
        try:
            X, y, ok, _ = self.preparar_df(df)
            if not ok:
                return False

            self.logger.debug("Modeller", "entrenar_df", f"Shape de X: {X.shape}, Shape de y: {y.shape}")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            self.logger.info("Modeller", "entrenar_df", f"Modelo entrenado con RMSE: {rmse:.4f}")

            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)

            return True
        except Exception as e:
            self.logger.error("Modeller", "entrenar_df", f"Error entrenando modelo: {e}")
            return False

    def predecir_df(self, df):
        try:
            X, _, ok, df_ordenado = self.preparar_df(df)
            if not ok:
                return df, False, 0, "", 0

            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)

            ultima_fila = X.tail(1)
            prediccion = model.predict(ultima_fila)[0]
            fecha_prediccion = df_ordenado['fecha'].iloc[-1]
            fila = df_ordenado.shape[0] - 1

            self.logger.info("Modeller", "predecir_df", f"Predicción realizada: {prediccion:.4f}")
            return df, True, prediccion, fecha_prediccion.strftime('%Y-%m-%d'), fila

        except Exception as e:
            self.logger.error("Modeller", "predecir_df", f"Error en predicción: {e}")
            return df, False, 0, "", 0
