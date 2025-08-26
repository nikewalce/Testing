import logging
from pathlib import Path
from typing import Union

from src.support.logging.handlers.console_handler import ConsoleLogHandler
from src.support.logging.handlers.file_handler import FileLogHandler
from src.support.logging.handlers.memory_handler import MemoryErrorHandler
from src.conf import settings


class Logger:
    """Класс для создания и настройки логгера."""

    def __init__(
        self,
        name: str,
        log_level: str = settings.LOG_LEVEL,
        log_handlers: (
            list[Union[ConsoleLogHandler, FileLogHandler, MemoryErrorHandler]]
            | None
        ) = None,
        log_dir: Path = Path(settings.LOG_DIR),
        max_file_size: int = settings.LOG_MAX_SIZE,
        backup_count: int = settings.LOG_BACKUP_COUNT,
    ):
        """
        Инициализирует логгер с указанными параметрами.

        :param name: Имя логгера.
        :param log_level: Уровень логирования (например, "DEBUG", "INFO").
        :param log_handlers: Список обработчиков логирования (по умолчанию используется консольный и файловый).
        :param log_dir: Директория для хранения файлов логов.
        :param max_file_size: Максимальный размер файла логов (в байтах).
        :param backup_count: Количество резервных файлов.
        """
        if log_handlers is None:
            formatter = logging.Formatter(settings.LOG_FORMAT)
            log_handlers = [
                ConsoleLogHandler(formatter),
                FileLogHandler(
                    log_dir, max_file_size, backup_count, formatter
                ),
            ]

        self._logger = logging.getLogger(name)
        self._logger.setLevel(
            getattr(logging, log_level.upper(), logging.INFO)
        )

        self._logger.handlers.clear()

        for handler in log_handlers:
            if not any(
                isinstance(h, type(handler)) for h in self._logger.handlers
            ):
                handler.add_handler(self._logger)

        # ! Очень перегруженная логика в классе, отрефакторить

        memory_handler = MemoryErrorHandler(capacity=5)
        memory_handler.setFormatter(settings.LOG_FORMAT)
        self._logger.addHandler(memory_handler)

    def __getattr__(self, item):
        """
        Делегирует вызов к внутреннему объекту _logger.
        """
        if not hasattr(self, "_logger"):
            raise AttributeError(f"'Logger' object has no attribute '{item}'")
        return getattr(self._logger, item)

    @property
    def logger(self) -> logging.Logger:
        """Возвращает экземпляр логгера."""
        return self._logger
