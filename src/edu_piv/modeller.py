import os

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score


class Modeller:
    def __init__(self,logger):
        self.logger = logger
        self.model_ruta = "src/edu_piv/static/models/"
        self.pkl_ruta="src/edu_piv/static/models/{}".format("dolar_model.pkl")
        if not os.path.exists(self.model_ruta):
            os.makedirs(self.model_ruta)

    def preparar_df(self,df=pd.DataFrame()):
        df = df.copy()
        return df,True,

    def entrenar_df(self,df=pd.DataFrame()):
        df = df.copy()
        return df,True,

    def predecir_df(self,df=pd.DataFrame()):
        df = df.copy()
        valor,fecha_pre,fila=0,"",0
        return df,True,valor,fecha_pre,fila
    