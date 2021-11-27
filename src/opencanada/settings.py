import logging.config
from dataclasses import dataclass
from functools import lru_cache

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

ERROR_LOG_FILENAME = ".opendata-errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(asctime)s:%(name)s: %(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "ancestry": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile", "verbose_output"]},
}
logging.config.dictConfig(LOGGING_CONFIG)


@dataclass
class OpenCanadaConfig:
    language: str = 'en'
    url: str = 'https://open.canada.ca'
    api_url: str = 'https://open.canada.ca/data/api'
    inventory_dataset: str = '4ed351cf-95d8-4c10-97ac-6b3511f359b7'


@lru_cache(maxsize=None)
def get_config(language='en'):
    return OpenCanadaConfig(language=language)
