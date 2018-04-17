import logging
import logging.handlers

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    fh = logging.handlers.RotatingFileHandler('./logtest.log', maxBytes=10240, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(fh)
    return logger