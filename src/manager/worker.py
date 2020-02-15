import sys
import time

from manager.config_writer import writer as config_writer
from manager.domain_cleaner import domain_cleaner
from manager.logger import create_logger
from manager.project_checker import project_checker
from manager.sync import sync as sync

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
        project_checker()
        config_writer()
        domain_cleaner()
        time.sleep(1)
