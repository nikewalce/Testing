import logging
from typing import Type


def raise_error(
    message: str,
    logger: logging.Logger,
    exception: Type[BaseException] = Exception,
    *args,
) -> None:
    """
    Логирует сообщение об ошибке и выбрасывает указанное исключение.

    :param logger: Логгер, который будет использоваться для записи ошибки.
    :param message: Сообщение, которое будет записано в лог.
    :param exception: Исключение, которое будет выброшено после записи ошибки.
    :param args: Дополнительные аргументы для исключения.
    """
    logger.error(message)
    raise exception(message, *args)
