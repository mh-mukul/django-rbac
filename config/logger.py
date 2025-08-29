import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs directory exists


class NoSensitiveDataFilter:
    def filter(self, record):
        msg = record.getMessage().lower()
        if "password" in msg or "secret" in msg or "token" in msg:
            record.msg = "[SENSITIVE DATA REMOVED]"
        return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} "
                      "{process:d} {thread:d} {message}",
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },

    "filters": {
        "no_sensitive_data": {
            "()": NoSensitiveDataFilter,
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["no_sensitive_data"],
        },
        "django_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "formatter": "verbose",
            "filters": ["no_sensitive_data"],
        },
        "json_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.json"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "formatter": "json",
            "filters": ["no_sensitive_data"],
        },
        "authorization_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "authorization.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "formatter": "verbose",
            "filters": ["no_sensitive_data"],
        },
        "authentication_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "authentication.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "formatter": "verbose",
            "filters": ["no_sensitive_data"],
        },
    },

    "root": {
        "handlers": ["console"],  # console only, no file
        "level": "WARNING",       # log only warnings+ for root
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["django_file", "json_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "authorization": {
            "handlers": ["console", "authorization_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "authentication": {
            "handlers": ["console", "authentication_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
