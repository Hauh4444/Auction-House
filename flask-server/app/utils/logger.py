import logging


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Set up and return a configured logger.

    Args:
        name (str): Name of the logger.
        log_file (str): File path where the log messages will be stored.
        level (int, optional): Logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger