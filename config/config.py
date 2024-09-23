import logging
import logging.config
from dataclasses import dataclass
import os
from dotenv import load_dotenv, find_dotenv

from yaml import safe_load

config = safe_load(open("./config/config.yaml"))
log_dir = config["ai_ocr"]["log_dir"]
os.makedirs(name=log_dir, mode=0o777, exist_ok=True)
logging.config.fileConfig("./config/logger.ini")
logger = logging.getLogger()

import logging
from logging.handlers import RotatingFileHandler

_ = load_dotenv(find_dotenv())


def get_logger(name=None):
    # Define log formatter
    formatter = logging.Formatter(
        "%m/%d/%Y %I:%M:%S %p - %(levelname)-8s: %(message)s - %(pathname)s l\
            ine:%(lineno)d",
    )

    # Define info handler
    info_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "sys.log"),
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,  # Keep multiple backup files
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Define error handler
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "err.log"),
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,  # Keep multiple backup files
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Get logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set logger level to INFO

    # Clear existing handlers
    if not logger.handlers:
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

    return logger


@dataclass
class AIOCRConfig(object):
    log_dir: str = config["ai_ocr"]["log_dir"]
