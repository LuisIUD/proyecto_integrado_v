import datetime
import logging
import os

class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Asegura que los campos personalizados estén presentes en cada log
        extra = self.extra.copy()
        extra.update(kwargs.get("extra", {}))
        kwargs["extra"] = extra
        return msg, kwargs

class Logger:
    def __init__(self):
        # Crear carpeta de logs si no existe
        os.makedirs('logs', exist_ok=True)

        # Nombre del archivo de log con timestamp
        log_file = f"logs/GOOG_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Formato con campos personalizados
        formatter = logging.Formatter(
            fmt='[%(asctime)s | %(name)s | %(class_name)s | %(function_name)s | %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Configuración del handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Crear logger
        base_logger = logging.getLogger("GOOGAnalysis")
        base_logger.setLevel(logging.INFO)
        base_logger.addHandler(file_handler)
        base_logger.propagate = False  # Evita duplicación en consola si usas root logger

        # Adaptador para manejar campos extra personalizados
        self.logger = CustomAdapter(base_logger, {'class_name': '-', 'function_name': '-'})

    def info(self, class_name, function_name, description):
        self.logger.info(description, extra={'class_name': class_name, 'function_name': function_name})

    def warning(self, class_name, function_name, description):
        self.logger.warning(description, extra={'class_name': class_name, 'function_name': function_name})

    def error(self, class_name, function_name, description):
        self.logger.error(description, extra={'class_name': class_name, 'function_name': function_name})
