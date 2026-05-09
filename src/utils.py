import logging


def get_custom_logger(name: str | None = None) -> logging.Logger:
    """
    Создание кастомного логгера.

    Сделал свой логгер, чтобы в консоли не было логов от библиотек.

    Returns:
        logging.Logger

    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False

    return logger
