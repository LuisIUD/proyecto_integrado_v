import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

class Modeller:
    def __init__(self, logger, modelo_path='src/edu_piv/static/models/model.pkl'):
        self.logger = logger
        self.modelo_path = modelo_path
        self.modelo = None

    def entrenar(self, df):
        try:
            self.logger.info('Modeller', 'entrenar', 'Iniciando entrenamiento del modelo...')
            features = ['media_movil_7d', 'media_movil_30d', 'volatilidad_7d', 'volatilidad_30d', 'ixic_cerrar']
            df_model = df.dropna(subset=features + ['cerrar'])

            X = df_model[features]
            y = df_model['cerrar']

            model = LinearRegression()
            model.fit(X, y)
            score = model.score(X, y)
            joblib.dump(model, self.modelo_path)
            self.logger.info('Modeller', 'entrenar', f'Modelo entrenado con score R2: {score:.4f}')
            print(f" Modelo entrenado. Score (R²): {score:.4f}")
            return model

        except Exception as e:
            self.logger.error("Modeller", "entrenar", f"Error durante el entrenamiento: {e}")
            return None

    def predecir(self, df):
        try:
            self.logger.info('Modeller', 'predecir', 'Iniciando predicción...')
            if self.modelo is None:
                self.modelo = joblib.load(self.modelo_path)

            features = ['media_movil_7d', 'media_movil_30d', 'volatilidad_7d', 'volatilidad_30d', 'ixic_cerrar']
            df_pred = df.dropna(subset=features).copy()

            if df_pred.empty:
                self.logger.error("Modeller", "predecir", "No hay datos suficientes para predecir")
                return None, None

            ultimo = df_pred.iloc[-1]
            X_pred = ultimo[features].values.reshape(1, -1)
            y_pred = self.modelo.predict(X_pred)[0]

            fecha = ultimo.name.strftime('%Y-%m-%d') if isinstance(ultimo.name, pd.Timestamp) else 'sin_fecha'
            self.logger.info('Modeller', 'predecir', f'Predicción realizada para la fecha {fecha}')
            return y_pred, fecha

        except Exception as e:
            self.logger.error("Modeller", "predecir", f"Error al predecir: {e}")
            return None, None
