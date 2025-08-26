from selenium.webdriver.support.select import Select

from src.ui.locators.base_locator import Locator


class BaseSelect:
    """Класс для методов работы с базовыми выборами элементов"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.class_name = type(self).__name__

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def select_by_index(
        self, locator: Locator, index: int, timeout: float | int = 0
    ):
        """
        Выбор элемента по индексу.

        :param locator: Локатор элемента.
        :param index: Индекс для выбора.
        :param timeout: Время ожидания локатора.
        """
        element = self.base.elements.find_element(locator, timeout)
        try:
            select = Select(element)
            select.select_by_index(index)
            self.logger.debug(
                f"{self.class_name}: Элемент с локатором {locator} выбран по индексу {index}."
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при выборе элемента с локатором {locator} по индексу {index}."
            )
            raise e

    def select_by_value(
        self, locator: Locator, value: str, timeout: float | int = 0
    ):
        """
        Выбор элемента по значению.

        :param locator: Локатор элемента.
        :param value: Значение для выбора.
        :param timeout: Время ожидания локатора.
        """
        element = self.base.elements.find_element(locator, timeout)
        try:
            select = Select(element)
            select.select_by_value(value)
            self.logger.debug(
                f"{self.class_name}: Элемент с локатором {locator} выбран по значению {value}."
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при выборе элемента с локатором {locator} по значению {value}."
            )
            raise e

    def select_by_visible_text(
        self, locator: Locator, text: str, timeout: float | int = 1
    ):
        """
        Выбор элемента по видимому тексту.

        :param locator: Локатор элемента.
        :param text: Видимый текст для выбора.
        :param timeout: Время ожидания локатора.
        """
        element = self.base.elements.find_element(locator, timeout)
        try:
            select = Select(element)
            select.select_by_visible_text(text)
            self.logger.debug(
                f"{self.class_name}: Элемент с локатором {locator} выбран по видимому тексту {text}."
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при выборе элемента с локатором {locator} по видимому тексту {text}."
            )
            raise e
