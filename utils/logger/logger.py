import logging
import sys

def make_logger(unique_name):
    log = logging.getLogger(unique_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: %(message)s'))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log
