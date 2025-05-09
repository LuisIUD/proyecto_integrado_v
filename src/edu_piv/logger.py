import datetime
import logging
import os

class Logger:
    def __init__(self):
        # Crear carpeta de logs si no existe
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Ruta del archivo de log
        self.log_file = f"logs/dolar_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Configuración básica del logger
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='[%(asctime)s | %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Instancia del logger
        self.logger = logging.getLogger()

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
