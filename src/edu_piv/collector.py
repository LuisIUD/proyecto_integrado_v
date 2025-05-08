import requests
import pandas as pd
from bs4 import BeautifulSoup
#import selenium
from logger import Logger
import os



class Collector:
    def __init__(self,logger):
        self.url= 'https://es.finance.yahoo.com/quote/GOOG/history/'
        self.logger = logger
        if not os.path.exists('/src/edu_piv/static'):
            os.makedirs('/src/edu_piv/static')
        if not os.path.exists('/src/edu_piv/static/data'):
            os.makedirs('/src/edu_piv/static/data')

    def collertor_data(self):
        try:
          df = pd.DataFrame()
          headers= {
             'User-Agent':'Mozilla/5.0'
          }
          response = requests.get(self.url,headers=headers)
          if response.status_code != 200:
             self.logger.error("Error al consultar la url : {}".format(response.status_code))
             return df
          soup = BeautifulSoup(response.text,'html.parser')
          table = soup.select_one('div[data-testid="history-table"] table')
          if table is None:
             self.logger.error("Error al buscar la tabla data-testid=history-table")
             return df
          headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
          rows=[]
          for tr in table.tbody.find_all('tr'):
             colums = [td.get_text(strip=True) for td in tr.find_all('td')]
             if len(colums) == len(headerss):
                rows.append(colums)
          df = pd.DataFrame(rows,columns=headerss).rename(columns={
                'Fecha':'fecha',
                'Abrir':'abrir',
                'Máx.':'max',
                'Mín.':'min',
                'CerrarPrecio de cierre ajustado para splits.':'cerrar',
                'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.':'cierre_ajustado',
                'Volumen':'volumen'
            })
          #self.logger.info("Datos obtenidos exitosamente {}".format(df.shape))
          return df
        except Exception as error:
          self.logger.error("Error al obtener los datos de la url {error}")