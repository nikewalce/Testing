from datetime import datetime

from src.ui.locators.base_locator import Locator


class BaseRecords:
    """Класс для методов работы с данными таблиц на страницах"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.class_name = type(self).__name__

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def parsing_rows(
        self,
        locator: Locator,
        timeout: float | int = 0,
    ):
        """
        Парсинг столбцов в таблице записей
        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        """
        try:
            rows = self.base.elements.present_elements(locator, timeout)
            values = [
                str(row.text) for row in rows if row.text != "Нет данных"
            ]
            self.logger.debug(
                f"Записи в таблице собраны по локатору {locator}"
            )
            return values
        except Exception as e:
            self.logger.error(f"Ошибка при сборе данных по локатору {locator}")
            raise e

    def parsing_rows_with_date(
        self,
        locator: Locator,
        timeout: float | int = 0,
    ):
        """
        Парсинг столбцов с датами в таблице записей
        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        """
        try:
            rows = self.base.elements.present_elements(locator, timeout)
            values = [
                datetime.strptime(row.text[:10], "%d.%m.%Y")
                for row in rows
                if row.text != "Нет данных"
            ]
            self.logger.debug(
                f"Записи в таблице собраны по локатору {locator}"
            )
            return values
        except Exception as e:
            self.logger.error(f"Ошибка при сборе данных по локатору {locator}")
            raise e

    def parse_checkboxes(
        self,
        locator: Locator,
        timeout: float | int = 0,
        check_mark: bool = False,
    ) -> list:
        """
        Парсинг состояния чекбоксов в таблице записей.
        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :param check_mark: Флаг для проверки состояния отметок.
        :return: Список состояний чекбоксов (True - выбран, False - не выбран).
        """
        try:
            checkboxes = self.base.elements.present_elements(locator, timeout)
            class_to_state_map = (
                {"success--text": "success", "": "warning"}
                if check_mark
                else {"mdi-checkbox-marked": "marked", "": "blank"}
            )
            states = [
                next(
                    (
                        state
                        for cls, state in class_to_state_map.items()
                        if cls in checkbox.get_attribute("class")
                    ),
                    None,
                )
                for checkbox in checkboxes
            ]
            self.logger.debug(
                f"Состояния чекбоксов собраны по локатору {locator}: {states}"
            )
            return states
        except Exception as e:
            self.logger.error(f"Ошибка при сборе данных по локатору {locator}")
            raise e

    def parse_match_count(self, locator: Locator, timeout: float | int = 0) -> int:
        """
               Подсчитывает количество элементов.
               :param locator: Локатор элемента.
               :param timeout: Время ожидания в секундах.
               """
        elements = self.base.elements.present_elements(locator, timeout)
        try:
            self.logger.info(
                f"Найдено {len(elements)} по локатору {locator}"
            )
            return len(elements)
        except Exception as e:
            self.logger.error(
                f"Ошибка при подсчете элементов по локатору {locator}"
            )
            raise e


