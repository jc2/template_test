import logging


def init_log(name):
    logger = logging.getLogger(f"{name}")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f"{name}.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger
