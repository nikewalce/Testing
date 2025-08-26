from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.ui.locators.base_locator import Locator
from src.ui.pom.utils.wait import Wait


class BaseElements:
    """Класс для методов работы с базовыми элементами"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.wait = Wait(self.browser, self.logger)
        self.class_name = type(self).__name__

    def present_element(self, locator: Locator, timeout: float | int = 0):
        """
        Находит элемент в HTML странице по локатору.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :return: Найденный веб-элемент.
        """
        try:
            element: WebElement = self.wait.wait_for(
                EC.presence_of_element_located, locator, timeout
            )
            return element
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нахождении элемента \
                в HTML странице по локатору: {locator}"
            )
            raise e

    def present_elements(self, locator: Locator, timeout: float | int = 0):
        """
        Находит элементы в HTML странице по локатору.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :return: Найденные веб-элементы.
        """
        try:
            elements: WebElement = self.wait.wait_for(
                EC.presence_of_all_elements_located, locator, timeout
            )
            return elements
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нахождении элементов \
                в HTML странице по локатору: {locator}"
            )
            raise e

    def find_element(
        self,
        locator: Locator,
        timeout: float | int = 0,
    ):
        """
        Находит видимый элемент на странице по локатору.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :return: Найденный веб-элемент.
        """
        try:
            element: WebElement = self.wait.wait_for(
                EC.visibility_of_element_located, locator, timeout
            )
            return element
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нахождении элемента \
                по локатору: {locator}"
            )
            raise e

    def find_elements(self, locator: Locator, timeout: float | int = 0):
        """
        Находит видимые элементы на странице по локатору.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :return: Найденный веб-элемент.
        """
        try:
            elements = self.wait.wait_for(
                EC.visibility_of_all_elements_located, locator, timeout
            )
            return elements
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нахождении элементов \
                по локатору: {locator}"
            )
            raise e

    def find_child_element(self, parent_element, child_locator: Locator):
        """
        Находит видимый дочерний элемент в пределах родительского элемента по локатору.

        :param parent_element: Родительский веб-элемент.
        :param child_locator: Локатор дочернего элемента.
        :return: Найденный дочерний веб-элемент.
        """
        try:
            child_element = parent_element.find_element(
                child_locator.by, child_locator.value
            )
            self.logger.debug(
                f"{self.class_name}: Дочерний элемент найден по локатору: {child_locator}"
            )
            return child_element
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нахождении дочернего элемента \
                   по локатору: {child_locator}"
            )
            raise e

    def is_element_present(self, locator: Locator, timeout: float | int = 0) -> bool:
        """
        Проверяет, присутствует ли элемент на странице.

        :param locator: Локатор элемента
        :param timeout: Время ожидания
        :return: True если элемент найден, False если нет
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
