import logging


class CustomStreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord):
        filename = '.'.join([f'{record.name}'[4:], 'log'])
        message = self.format(record)
        with open(f'logs/{filename}', 'a', encoding='utf8') as log_file:
            log_file.write(message + '\n')


logs_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        },
        "custom": {
            "format": "%(levelname)s | %(name)s | %(lineno)s | %(asctime)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": 'logging.StreamHandler',
            "level": "DEBUG",
            "formatter": "base",
        },
        "file": {
            "()": CustomStreamHandler,
            "level": "INFO",
            "formatter": "base",
        },
        'celery_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'logs/celery.log',
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'custom',
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            # "propagate": False,
        }
    },
}
