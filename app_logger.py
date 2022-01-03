import logging

log_format = '%(asctime)s - Уровень %(levelname)s в %(filename)s.%(funcName)s: %(message)s'


def get_file_handler():
    file_handler = logging.FileHandler("log.txt")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    return file_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    return logger


