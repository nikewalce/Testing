from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from src.ui.locators.base_locator import Locator
from src.ui.pom.utils.wait import Wait


class CheckElement:
    def __init__(self, browser: WebDriver, logger):
        self.browser = browser
        self.logger = logger
        self.wait = Wait(self.browser, self.logger)

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def verify_present(
        self, locator: Locator, timeout: float | int = 0, reverse: bool = False
    ) -> None:
        """Проверяет наличие элемента на странице.

        :param locator: Локатор элемента, наличие которого нужно проверить.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.presence_of_element_located, locator, timeout, reverse
        )

    def verify_visible(
        self, locator: Locator, timeout: float | int = 0, reverse: bool = False
    ) -> None:
        """Проверка видимости элемента на странице.

        :param locator: Локатор элемента, наличие которого нужно проверить.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.visibility_of_element_located, locator, timeout, reverse
        )

    def verify_clickable(
        self,
        locator: Locator,
        timeout: float | int = 0,
        reverse: bool = False,
        **kwargs,
    ) -> None:
        """Проверка кликабельности элемента на странице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.element_to_be_clickable, locator, timeout, reverse, **kwargs
        )

    def verify_text(
        self,
        locator: Locator,
        expected_text: str,
        timeout: float | int = 0,
        reverse: bool = False,
    ) -> None:
        """Проверяет, что элемент содержит ожидаемый текст.

        :param locator: Локатор элемента.
        :param expected_text: Ожидаемый текст.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.text_to_be_present_in_element,
            locator,
            timeout,
            reverse,
            text_=expected_text,
        )

    def verify_attribute_value(
        self,
        locator: Locator,
        attribute: str,
        expected_value: str,
        timeout: float | int = 0,
        reverse: bool = False,
    ) -> None:
        """Проверяет, что элемент имеет ожидаемый атрибут.

        :param locator: Локатор элемента.
        :param attribute: Название атрибута.
        :param expected_value: Ожидаемое значение атрибута.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.text_to_be_present_in_element_attribute,
            locator,
            timeout,
            reverse,
            attribute_=attribute,
            text_=expected_value,
        )

    def verify_element_color(
        self,
        child_locator: Locator,
        min_color: tuple[int, int, int, float] = (0, 0, 0, 0.0),
        max_color: tuple[int, int, int, float] = (0, 0, 0, 0.0),
        type_css: str = "color",
    ) -> None:
        """Проверяет, что элемент при наведении курсора меняет цвет.

        :param child_locator: Локатор дочернего элемента, который меняет цвет.
        :param min_color: Минимальное значение диапазона цвета
        :param max_color: Максимальное значение диапазона цвета
        :param type_css: Наименование параметра стиля, по умолчанию "color"
        """
        try:
            current_color = self.base.style.get_value_css_property(
                child_locator, type_css
            )

            assert self.base.style.is_color_in_range(
                current_color, min_color, max_color
            ), f"Цвет {current_color} не входит в диапазон от {min_color} до {max_color}"
            self.logger.debug(
                f"Подтвержается что элемент с локатором {child_locator}"
                f" при наведении имеет цвет в диапазоне от {min_color} до {max_color}"
            )
        except TimeoutException as e:
            self.logger.error(
                f"Ошибка - элемент с локатором {child_locator}"
                f" не имеет при наведении цвет в диапазоне от {min_color} до {max_color}"
            )
            raise e

    def verify_css_property(
        self,
        locator: Locator,
        css_value: str,
        css_item: str,
        timeout: float | int = 0,
    ):
        """Проверяет, что стиль элемента имеет искомое значение.

        :param locator: Локатор элемента, который имеет искомое значение стиля.
        :param css_value: Атрибут стиля
        :param css_item: Ожидаемое значение атрибута стиля
        :param timeout: Время ожидания в секундах.
        """
        try:
            element = self.base.style.get_value_css_property(
                locator, css_value, timeout
            )
            assert element == css_item
            self.logger.debug(
                f"Подтвержается что элемент с локатором - {locator},"
                f"имеет искомое значения стиля - {css_item}."
            )
        except AssertionError as e:
            self.logger.error(
                f"Ошибка: элемент с локатором - {locator}"
                f" не имеет искомое значения стиля - {css_item}."
            )
            raise e

    def verify_disabled(
        self, locator: Locator, timeout: float | int = 0
    ) -> None:
        """Проверка недоступности элемента.

        :param locator: Локатор элемента, который проверяется на недоступность.
        :param timeout: Время ожидания в секундах.
        """
        element = self.wait.wait_for(
            EC.visibility_of_element_located, locator, timeout
        )
        try:
            assert element and not element.is_enabled()
            self.logger.debug(f"Элемент с локатором {locator} недоступен")
        except AssertionError as e:
            self.logger.error(
                f"Ошибка - Элемент с локатором {locator} доступен"
            )
            raise e

    def verify_active(
        self,
        locator: Locator,
        timeout: float | int = 0,
    ) -> None:
        """
        Проверка активности элемента.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания в секундах.
        :return: True, если элемент активен, иначе False.
        """
        self.verify_attribute_value(
            locator=locator,
            attribute="aria-selected",
            expected_value="true",
            timeout=timeout,
        )

    def verify_bool_visible(
        self, locator: Locator, timeout: float | int = 0
    ) -> bool:
        """
        Проверяет видимость элемента на странице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :return: bool:
                    False, если элемент не найден по локатору;
                    True, если элемент найден по локатору.
        """
        try:
            self.wait.wait_for(
                EC.visibility_of_element_located, locator, timeout
            )
            self.logger.debug(f"Элемент найден по локатору: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Элемент не найден по локатору: {locator}")
            return False

    def verify_select(
        self,
        locator: Locator,
        timeout: float | int = 0,
    ):
        """
        Проверяет выбран ли элемент.
        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        """
        try:
            self.wait.wait_for(
                EC.element_located_to_be_selected, locator, timeout
            )
            self.logger.debug(f"Элемент {locator} является выбранным")
        except AssertionError:
            self.logger.debug(f"Элемент {locator} не является выбранным")

    def verify_invisible(
        self, locator: Locator, timeout: float | int = 0, reverse: bool = False
    ) -> None:
        """Проверка невидимости элемента на странице.

        :param locator: Локатор элемента, наличие которого нужно проверить.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        self.wait.wait_for(
            EC.invisibility_of_element, locator, timeout, reverse
        )
