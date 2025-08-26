import logging

from src.support.logging.handlers._abc import LogHandler


class ConsoleLogHandler(LogHandler):
    """
    Обработчик логирования для вывода сообщений в консоль.
    """

    def __init__(self, formatter: logging.Formatter):
        """
        Инициализирует обработчик для консольного логирования.
        :param formatter: Форматтер, который будет использоваться для форматирования
                          сообщений перед выводом в консоль.
        """
        self._formatter = formatter

    def add_handler(self, logger):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._formatter)
        logger.addHandler(console_handler)
