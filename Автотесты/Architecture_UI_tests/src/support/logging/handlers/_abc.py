import logging
from abc import ABC, abstractmethod


class LogHandler(ABC):
    """Абстрактный базовый класс для обработчиков."""

    @abstractmethod
    def add_handler(self, logger: logging.Logger) -> None:
        """
        Добавление обработчика к экземпляру логирования.
        :param logger: Экземпляр логгера, к которому добавляется обработчик.
        """
