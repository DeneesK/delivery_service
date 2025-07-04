import logging

from core.conf import config

LOGGING = {
    "format": "%(asctime)s  - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.DEBUG if config.IS_DEV_MODE else logging.INFO,
}

logging.basicConfig(**LOGGING)  # type: ignore
