from src.ui.locators.base_locator import Locator


class BaseStyle:
    """Класс для методов работы со стилями элементов"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.class_name = type(self).__name__

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def is_color_in_range(self, color, min_color, max_color):
        """Проверка нахождения цвета в диапазоне значений
        :param color: Цвет элемента на странице.
        :param min_color: Минимальное приемлемое значение цвета.
        :param max_color: Максимальное приемлемое значение цвета.
        """
        rgba = color.replace("rgba(", "").replace(")", "").split(",")
        color = tuple(map(float, rgba))
        return all(
            min_c <= c <= max_c
            for c, min_c, max_c in zip(color, min_color, max_color)
        )

    def get_value_css_property(
        self, locator: Locator, css_value: str, timeout: float | int = 0
    ):
        """
        Получение значения стиля элемента
        :param locator: Локатор элемента, который имеет искомое значение стиля.
        :param css_value: Искомый атрибут стиля
        :param timeout: Время ожидания в секундах.
        """
        try:
            element = self.base.elements.present_element(locator, timeout)
            style = element.value_of_css_property(css_value)
            self.logger.debug(
                f"{self.class_name}: Найдено искомое значение стиля:"
                f" {css_value} элемента с локатором: {locator} "
            )
            return style
        except Exception:
            self.logger.error(
                f"{self.class_name}: Ошибка -элемент с локатором: {locator}"
                f" не имеет искомое значение стиля: {css_value}"
            )
            return None
