# # logger_config.py
# import logging
# from logging.handlers import RotatingFileHandler
# import os

# LOG_DIR = "logs"
# LOG_FILE = "scooter_app.log"
# os.makedirs(LOG_DIR, exist_ok=True)
# log_path = os.path.join(LOG_DIR, LOG_FILE)

# def get_logger(name="scooter_app"):
#     logger = logging.getLogger(name)
#     if logger.handlers:
#         return logger  # already configured

#     logger.setLevel(logging.DEBUG)

#     # console handler
#     ch = logging.StreamHandler()
#     ch.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)

#     # rotating file handler
#     fh = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
#     fh.setLevel(logging.DEBUG)
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)

#     return logger


import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "scooter_app.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE)

def get_logger(name="scooter_app"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


