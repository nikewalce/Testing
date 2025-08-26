import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.support.logging.handlers._abc import LogHandler


class FileLogHandler(LogHandler):
    """Обработчик логирования для записи сообщений в файл с ротацией."""

    def __init__(
        self,
        log_dir: Path,
        max_file_size: int,
        backup_count: int,
        formatter: logging.Formatter,
    ):
        """
        Инициализирует обработчик для записи логов в файл с ротацией.

        :param log_dir: Директория для хранения файлов логов.
        :param max_file_size: Максимальный размер файла логов, после которого будет происходить ротация.
        :param backup_count: Количество резервных файлов.
        :param formatter: Форматтер для форматирования сообщений в файле.
        """
        self._log_dir = log_dir
        self._max_file_size = max_file_size
        self._backup_count = backup_count
        self._formatter = formatter

    def add_handler(self, logger):
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / f"{logger.name}.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self._max_file_size,
            backupCount=self._backup_count,
            mode="a",
            encoding="utf-8",
        )
        file_handler.setFormatter(self._formatter)
        logger.addHandler(file_handler)
