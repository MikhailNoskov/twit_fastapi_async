import logging


class CustomStreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord):
        filename = ".".join([f"{record.name}"[4:], "log"])
        message = self.format(record)
        with open(f"logs/{filename}", "a", encoding="utf8") as log_file:
            log_file.write(message + "\n")


logs_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {"format": "%(levelname)s | %(name)s | %(message)s"},
        "custom": {"format": "%(levelname)s: %(name)s | %(asctime)s | %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "custom",
        },
        "file": {
            "()": CustomStreamHandler,
            "level": "DEBUG",
            "formatter": "custom",
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        }
    },
}
