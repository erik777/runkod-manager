import time

from manager.check import main as check
from manager.config_writer import main as config_writer
from manager.sync import main as sync


def main():
    while True:
        sync()
        check()
        config_writer()
        time.sleep(1)
