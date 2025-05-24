import datetime
import logging
import os

class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        extra.update(kwargs.get("extra", {}))
        kwargs["extra"] = extra
        return msg, kwargs

class Logger:
    def __init__(self, name="GOOGAnalysis"):  # <-- Ahora acepta nombre dinámico
        os.makedirs('logs', exist_ok=True)
        log_file = f"logs/{name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        formatter = logging.Formatter(
            fmt='[%(asctime)s | %(name)s | %(class_name)s | %(function_name)s | %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        base_logger = logging.getLogger(name)  # <-- Usa el nombre dinámico
        base_logger.setLevel(logging.INFO)
        base_logger.addHandler(file_handler)
        base_logger.addHandler(console_handler)
        base_logger.propagate = False

        self.logger = CustomAdapter(base_logger, {'class_name': '-', 'function_name': '-'})

    def info(self, class_name, function_name, description):
        self.logger.info(description, extra={'class_name': class_name, 'function_name': function_name})

    def warning(self, class_name, function_name, description):
        self.logger.warning(description, extra={'class_name': class_name, 'function_name': function_name})

    def error(self, class_name, function_name, description):
        self.logger.error(description, extra={'class_name': class_name, 'function_name': function_name})
