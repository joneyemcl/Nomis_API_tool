import logging
import os

import pandas as pd

pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 500)


def setup_logger(name: str, reset_file=False):
    """
    Creates a logger file in the current directory if run as a script, set name=__name__
    """
    if reset_file:
        reset_log(name)
    logger = logging.getLogger(name)
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG,
        filename='logs.txt'
    )
    return logger


def reset_log(name: str) -> None:
    curr_dir = os.path.dirname(os.path.abspath(name))
    log_path = os.path.join(curr_dir, 'logs.txt')
    if os.path.isfile(log_path):
        with open(log_path, 'w'):
            pass