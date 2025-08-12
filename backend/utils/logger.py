import logging
import json

class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        log_entry = self.format(record)
        with open(self.baseFilename, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
            "name": record.name,
        }
        # Adaugă orice alte chei suplimentare
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        return json.dumps(log_record, ensure_ascii=False)

logger = logging.getLogger("math_microservice")
logger.setLevel(logging.INFO)
handler = JsonFileHandler("app_log.json")
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

def log_json(message, **kwargs):
    extra = {"extra": kwargs}
    logger.info(message, extra=extra)