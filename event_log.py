"""File log for events and errors. This is the only use of the filesystem."""

import logging
from pathlib import Path


def get_logger():
    logger = logging.getLogger("software_fj")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_dir / "events.log", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(file_handler)
    return logger
