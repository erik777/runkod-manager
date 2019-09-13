import time
import sys

from manager.checker import checker
from manager.config_writer import writer as config_writer
from manager.sync import sync as sync
from manager.logger import create_logger

logger = create_logger('worker')


def ex_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = ex_hook


def main():
    while True:
        sync()
        checker()
        config_writer()
        time.sleep(1)
