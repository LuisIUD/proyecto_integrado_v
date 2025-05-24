import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import os

class Modeller:
    def __init__(self, logger):
        self.logger = logger
        self.model = None
        self.model_path = "src/edu_piv/static/models/model.pkl"
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def preparar_datos(self, df, ticker='GOOG'):
        try:
            df_filtrado = df[df['ticker'] == ticker].copy()
            columnas_kpi = [
                'retorno_log_diario',
                'media_movil_7d',
                'media_movil_30d',
                'volatilidad_7d',
                'volatilidad_30d'
            ]

            print("Columnas disponibles:", df_filtrado.columns.tolist())
            for col in columnas_kpi:
                if col not in df_filtrado.columns:
                    self.logger.error("Modeller", "preparar_datos", f"Falta columna: {col}")
                    print(f" Falta columna: {col}")
                    return None, None, False

            df_filtrado = df_filtrado.dropna(subset=columnas_kpi + ['cerrar'])
            X = df_filtrado[columnas_kpi]
            y = df_filtrado['cerrar']

            if X.empty or y.empty:
                self.logger.warning("Modeller", "preparar_datos", "X o y están vacíos después del dropna.")
                print(" Datos vacíos tras limpieza.")
                return None, None, False

            print(" Datos preparados correctamente.")
            print("X shape:", X.shape)
            print("y shape:", y.shape)
            return X, y, True

        except Exception as e:
            self.logger.error("Modeller", "preparar_datos", f"Error preparando datos: {str(e)}")
            print(f" Error preparando datos: {str(e)}")
            return None, None, False

    def entrenar(self, df, ticker='GOOG'):
        try:
            X, y, valido = self.preparar_datos(df, ticker)

            if not valido:
                self.logger.error("Modeller", "entrenar", "Datos insuficientes o inválidos para entrenamiento.")
                print("X Entrenamiento cancelado: datos inválidos.")
                return False

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)

            score = self.model.score(X_test, y_test)
            print(f" Modelo entrenado. Score (R²): {score:.4f}")
            self.logger.info("Modeller", "entrenar", f"Modelo entrenado con score R2: {score:.4f}")

            print("Guardando modelo en:", self.model_path)
            joblib.dump(self.model, self.model_path)
            print(" Modelo guardado exitosamente.")
            return True

        except Exception as e:
            self.logger.error("Modeller", "entrenar", f"Error durante entrenamiento: {str(e)}")
            print(f" Error durante entrenamiento: {str(e)}")
            return False
