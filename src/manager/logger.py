import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'log'))
log_path = os.path.join(log_dir, 'runkod-manager.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def create_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = RotatingFileHandler(log_path, maxBytes=1024 * 100000, backupCount=10)
    logger.addHandler(handler)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    return logger
