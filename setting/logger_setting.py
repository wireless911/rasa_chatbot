import os
import sys

import logging
import sys


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
            + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)


def get_logging_config(name="rasa_actions"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = BASE_DIR + "/logs/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = f"{name}.log"
    if not os.path.exists(log_path+log_file):
        with open(log_file,"w") as f:
            f.write("")
    _path = log_path +log_file
    _LOGGING_CONFIG = dict(
        version=1,
        disable_existing_loggers=False,

        loggers={
            "sanic.root": {
                "level": "INFO",
                "handlers": ["console"]
            },
            "sanic.error": {
                "level": "INFO",
                "handlers": ["error_console"],
                "propagate": True,
                "qualname": "sanic.error"
            },

            "sanic.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": True,
                "qualname": "sanic.access"
            }
        },
        handlers={
            "console": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "generic",
                "when": "midnight",
                "interval": 1,
                "backupCount": 180,
                "filename": _path,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stderr
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": sys.stdout
            },
        },
        formatters={
            "generic": {
                "format": "[%(asctime)s] %(levelname)s (%(process)d) (%(filename)s:%(lineno)d) %(message)s",
                # "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter"
            },
            "access": {
                "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                          "%(request)s %(message)s %(status)d %(byte)d",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter"
            },
        }
    )

    return _LOGGING_CONFIG
