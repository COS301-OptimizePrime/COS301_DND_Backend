import logging
import logging.handlers


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    fh = logging.handlers.RotatingFileHandler('./dnd_backend.log',
                                              maxBytes=10240)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    file_handler_error = logging.handlers.RotatingFileHandler('./dnd_backend.err',
                                                              maxBytes=10240)
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(fh)
    logger.addHandler(file_handler_error)

    return logger
