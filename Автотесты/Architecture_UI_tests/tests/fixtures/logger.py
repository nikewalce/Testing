import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest


@pytest.fixture
def logger(request: pytest.FixtureRequest) -> logging.Logger:
    """A fixture for initializing the logger."""
    log = request.config.getoption("--log")
    logger = logging.getLogger(request.node.name)
    logger.setLevel(level=request.config.getoption("--log_level"))

    if log is True:
        logs_path = Path(__file__).resolve().parents[2] / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        log_file = logs_path / f"{request.node.name}.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 100, backupCount=5, mode="w"
        )
        file_handler.setFormatter(
            logging.Formatter("%(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)
    else:
        logger.disabled = True
    return logger
