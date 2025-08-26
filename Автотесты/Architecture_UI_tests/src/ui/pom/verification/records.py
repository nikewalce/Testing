import re
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from src.ui.locators.base_locator import Locator
from src.ui.pom.utils.wait import Wait


class CheckRerord:
    def __init__(self, browser: WebDriver, logger):
        self.browser = browser
        self.logger = logger
        self.wait = Wait(self.browser, self.logger)

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def clean_string(self, value):
        """
        Удаляет спецсимволы из строки и обрабатывает пустые значения.
        :param value: Исходное значение.
        :return: Очищенное значение, где пустые строки заменяются специальным маркером.
        """
        if not isinstance(value, str) or not value.strip():
            return 'zzz'
        return re.sub(r'[^\w\s+]', '', value).strip()

    def should_contain_text_in_rows_table(
        self,
        locator: Locator,
        expected_text: str,
        exact_match: bool = False,
        timeout: float | int = 0,
    ):
        """
        Проверяет, что все строки таблицы по заданному локатору содержат ожидаемый текст.

        :param locator: Локатор элемента таблицы.
        :param expected_text: Ожидаемый текст, который должен содержаться в каждой строке.
        :param exact_match: Флаг, указывающий на необходимость точного совпадения текста.
        :param timeout: Время ожидания в секундах.
        """
        self.logger.info(
            f"Проверка, что все строки таблицы по локатору {locator} содержат текст '{expected_text}'"
        )
        rows = self.wait.wait_for(
            EC.presence_of_all_elements_located, locator, timeout
        )
        all_match = all(
            (
                expected_text == row.text
                if exact_match
                else expected_text.lower() in row.text.lower()
            )
            for row in rows
        )

        if not all_match:
            self.logger.error(
                f"Не все строки таблицы по локатору {locator} "
                f"{'точно' if exact_match else ''} содержат текст '{expected_text}'"
            )
            raise AssertionError(
                f"Не все строки таблицы по локатору {locator} "
                f"{'точно' if exact_match else ''} содержат текст '{expected_text}'"
            )

        self.logger.debug(
            f"Все строки таблицы по локатору {locator} "
            f"{'точно' if exact_match else ''} содержат текст '{expected_text}'"
        )

    def should_verify_results_in_date_range(
        self,
        locator: Locator,
        date_range: str,
        have_time: bool = False,
        timeout: float | int = 0,
    ):
        """
        Проверяет, что все строки таблицы по заданному локатору содержат дату в диапазоне.
        :param locator: Локатор элемента таблицы.
        :param date_range: Диапазон дат.
        :param have_time: Признак того, что дата должна содержать время.
        :param timeout: Время ожидания в секундах.
        """
        self.logger.info(
            f"Проверка, что все строки таблицы по локатору {locator} содержат дату в диапазоне {date_range}"
        )
        date_start, date_end = date_range.split(" — ")
        date_start = datetime.strptime(date_start, "%d.%m.%Y")
        date_end = datetime.strptime(date_end, "%d.%m.%Y")

        rows = self.wait.wait_for(
            EC.presence_of_all_elements_located, locator, timeout
        )

        def parse_date(date_string: str) -> datetime:
            """
            Пробует парсить дату в нескольких форматах: '%d.%m.%Y' и '%Y-%m-%d'.
            :param date_string: Строка с датой.
            :return: Объект datetime.
            """
            date_formats = ["%d.%m.%Y", "%Y-%m-%d"]

            for fmt in date_formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    pass
            raise ValueError(f"Неверный формат даты: {date_string}")

        try:
            for row in rows:
                row_text = row.text.strip()
                if "Дата регистрации:" in row_text:
                    row_text = row_text.replace(
                        "Дата регистрации:", ""
                    ).strip()
                date_text = row_text.split(" ")[0]
                document_date = parse_date(date_text)
                assert (
                    date_start <= document_date <= date_end
                ), f"Дата {document_date} не входит в диапазон {date_range}"
                self.logger.debug(
                    f"Все строки таблицы по локатору {locator} содержат дату в диапазоне {date_range}"
                )
        except AssertionError as e:
            self.logger.error(
                f"Не все строки таблицы по локатору {locator} содержат дату в диапазоне {date_range}"
            )
            raise e

    def should_match_count(
        self,
        locator: Locator,
        expected_count: int,
        timeout: float | int = 0,
    ) -> None:
        """
        Проверяет, что элемент имеет ожидаемое количество элементов.

        :param locator: Локатор элемента.
        :param expected_count: Ожидаемое количество элементов.
        :param timeout: Время ожидания в секундах.
        """
        elements = self.wait.wait_for(
            EC.presence_of_all_elements_located, locator, timeout
        )
        self.logger.info(
            f"Проверка, что {locator} имеет {expected_count} элементов"
        )
        try:
            assert (
                len(elements) == expected_count
            ), f"{locator} имеет {expected_count} элементов"
            self.logger.debug(f"{locator} имеет {expected_count} элементов")
        except AssertionError as e:
            self.logger.error(
                f"{locator} должно иметь {expected_count} элементов"
            )
            raise e

    def check_filled_input_field(
        self,
        locator: Locator,
        expected_value: str,
        timeout: float | int = 0,
    ):
        """
        Проверяет, что поле заполнено введенным значением
        :param locator: Локатор элемента.
        :param expected_value: Ожидаемое значение.
        :param timeout: Время ожидания в секундах.
        """
        element = self.wait.wait_for(
            EC.presence_of_element_located, locator, timeout
        )
        try:
            assert element.get_attribute("value") == expected_value
            self.logger.debug(
                f"Подтвержается что поле с локатором {locator} содержит {expected_value}"
            )
        except AssertionError as e:
            self.logger.error(
                f"Ошибка - поле с локатором {locator} не содержит {expected_value}"
            )
            raise e

    def check_sorting_of_table(
        self,
        locator: Locator,
        reverse: bool = False,
        timeout: float | int = 0,
        check_checkbox: bool = False,
        key=None,
    ) -> None:
        """
        Проверка сортировки строк в таблице по возрастанию или убыванию.
        :param locator: Локатор элементов, к которым применяется сортировка.
        :param reverse: Флаг для сортировки в обратном порядке.
        :param timeout: Время ожидания в секундах.
        :param check_checkbox: Флаг, обозначающий проверку сортировки чекбоксов
        """
        values = self.base.records.parsing_rows(locator, timeout)
        if check_checkbox:
            values = self.base.records.parse_checkboxes(locator, timeout)
        try:
            sorting_key = key or self.clean_string
            sorted_values = sorted(values, key=sorting_key, reverse=reverse)
            assert values == sorted_values
            self.logger.debug("Колонка отсортирована правильно.")
        except AssertionError as e:
            self.logger.error(
                f"""
                "Колонка отсортирована не правильно."
                "Ожидалось: {sorted_values}"
                "Получено: {values}"
            """
            )
            raise e

    def check_sorting_of_table_with_date(
        self,
        locator: Locator,
        reverse: bool = False,
        timeout: float | int = 0,
    ) -> None:
        """
        Проверка сортировки дат в таблице по возрастанию или убыванию.
        :param locator: Локатор элементов, к которым применяется сортировка.
        :param reverse: Флаг для сортировки в обратном порядке.
        :param timeout: Время ожидания в секундах.
        """
        values = self.base.records.parsing_rows_with_date(locator, timeout)
        try:
            if reverse:
                sorted_values = sorted(values, reverse=reverse)
            else:
                sorted_values = sorted(values)
            assert values == sorted_values
            self.logger.debug("Колонка отсортирована правильно.")
        except AssertionError as e:
            self.logger.error(
                f"""
                "Колонка не отсортирована правильно."
                "Ожидалось: {sorted_values}, но получено: {values}"
            """
            )
            raise e

    def should_contain_text_in_tables_column(
        self,
        locator: Locator,
        expected_text: str,
        timeout: float | int = 0,
    ):
        """
        Проверяет, что одна ячейка колонки таблицы по заданному локатору содержит ожидаемый текст.

        :param locator: Локатор колонки таблицы.
        :param expected_text: Ожидаемый текст, который должен содержаться в одной из ячейек.
        :param timeout: Время ожидания в секундах.
        """
        self.logger.info(
            f"Проверка, что одна ячейка таблицы по локатору {locator} содержит текст '{expected_text}'"
        )
        list_td = self.wait.wait_for(
            EC.presence_of_all_elements_located, locator, timeout
        )
        try:
            for td in list_td:
                if expected_text in td.text:
                    assert True
                    self.logger.debug(
                        f"Ячейка таблицы по локатору {locator} содержит текст '{expected_text}'"
                    )
                    break
        except AssertionError as e:
            self.logger.error(
                f"Ни одна ячейка таблицы по локатору {locator} не содержит текст '{expected_text}'"
            )
            raise e

    def should_not_contain_text_in_column_table_data(
        self,
        locator: Locator,
        expected_text: str,
        timeout: float | int = 0,
    ):
        """
        Проверяет, что все ячейки колонки таблицы по заданному локатору не содержат ожидаемый текст.

        :param locator: Локатор колонки таблицы.
        :param expected_text: Ожидаемый текст, который не должен содержаться в ячейеках.
        :param timeout: Время ожидания в секундах.
        """
        expected = expected_text.strip().lower()
        self.logger.info(
            f"Проверка, что все ячейки таблицы по локатору {locator} не содержат текст '{expected}'"
        )
        list_td = self.wait.wait_for(
            EC.presence_of_all_elements_located, locator, timeout
        )
        for td in list_td:
            actual = td.text.strip().lower()
            if expected in actual:
                self.logger.error(
                    f"Ячейка таблицы по локатору {locator} содержит текст '{expected}'"
                )
                assert False, f"Ячейка таблицы по локатору {locator} содержит текст '{expected}'"
            else:
                self.logger.debug(
                    f"Ячейки таблицы по локатору {locator} не содержат текст '{expected}'"
                )
                assert True
