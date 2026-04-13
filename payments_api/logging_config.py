from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


LOG_DIR = Path("D:/logs")
LOG_FILE = LOG_DIR / "payments.log"


def setup_logging() -> None:
    """Configure app logging once with daily file rotation."""
    logger = logging.getLogger("payments_api")
    if logger.handlers:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    # Example rotated file: payments.log.2026-04-09_log
    file_handler.suffix = "%Y-%m-%d_log"
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the payments_api logger namespace."""
    return logging.getLogger(f"payments_api.{name}")
