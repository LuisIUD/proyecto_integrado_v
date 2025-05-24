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

    def preparar_df(self, df):
        try:
            df = df.copy()
            # Seleccionar solo columnas numéricas
            df = df.select_dtypes(include=[np.number])
            
            # Crear variable objetivo: precio de cierre del día siguiente
            df['objetivo'] = df['cerrar'].shift(-1)
            
            # Eliminar filas con valores nulos
            df.dropna(inplace=True)

            if df.empty:
                self.logger.warning("Modeller", "preparar_df", "El DataFrame quedó vacío tras preparar variables.")
                return pd.DataFrame(), pd.Series(), False

            X = df.drop(columns=['objetivo'])
            y = df['objetivo']
            return X, y, True

        except Exception as e:
            self.logger.error("Modeller", "preparar_df", f"Error preparando dataset: {e}")
            return pd.DataFrame(), pd.Series(), False

    def entrenar_df(self, df):
        try:
            X, y, ok = self.preparar_df(df)
            if not ok:
                return False

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            # Usamos RMSE porque penaliza más los errores grandes,
            # lo cual es importante al predecir precios financieros donde los valores extremos tienen alto impacto.
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
            X, _, ok = self.preparar_df(df)
            if not ok:
                return df, False, 0, "", 0

            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)

            ultima_fila = X.tail(1)
            prediccion = model.predict(ultima_fila)[0]
            fecha_prediccion = df.index[-1] if isinstance(df.index, pd.DatetimeIndex) else df['fecha'].iloc[-1]
            fila = df.shape[0] - 1

            self.logger.info("Modeller", "predecir_df", f"Predicción realizada: {prediccion:.4f}")
            return df, True, prediccion, fecha_prediccion, fila

        except Exception as e:
            self.logger.error("Modeller", "predecir_df", f"Error en predicción: {e}")
            return df, False, 0, "", 0
