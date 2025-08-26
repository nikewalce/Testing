from typing import Any, Literal

from src.ui.pom.pages.base_element.locators import base_element_locators
from src.ui.pom.pages.base_element.page.base_element_page import (
    BaseElementPage,
)
from src.ui.pom.pages.inventory_page.locators import inventory_locators

_ElementTypes = Literal[
    "кнопка",
    "поле",
    "выпадающее поле",
    "чек-бокс",
    "заголовок",
    "всплывающее окно",
    "пункт меню",
]
_ActionsTypes = Literal[
    "активна",
    "кликабельная",
    "отображено",
    "отсутствует",
    "недоступна",
    "не отображен",
]


class CheckBaseElementPage(BaseElementPage):
    """Набор проверок для элементов, существующих на всех страницах"""

    def _normalize_key(self, key: str) -> str:
        """
        Нормализует ключ, удаляя окончания.

        :param text: Строка, которую нужно нормализовать.
        :return: Нормализованная строка без окончания.
        """
        suffixes = [
            "ая",
            "ьно",
            "но",
            "ьна",
            "ьный",
            "ый",
            "ое",
            "ет",
            "н",
            "ен",
            "на",
            "ный",
            "ным",
            "ма",
            "мым",
            "м",
        ]
        for suffix in suffixes:
            if key.endswith(suffix):
                return key[: -len(suffix)]

        return key

    def get_checks(self, *args, **kwargs) -> dict[str, Any]:
        """
        Возвращает словарь функций проверок.

        :return: Словарь, где ключи — это нормализованные состояния,
                 а значения — функции проверок.
        """
        return {
            "актив": lambda: self.check.elements.verify_active(
                *args, **kwargs
            ),
            "отображе": lambda: self.check.elements.verify_visible(
                *args, **kwargs
            ),
            "кликабел": lambda: self.check.elements.verify_clickable(
                *args, **kwargs
            ),
            "недоступ": lambda: self.check.elements.verify_disabled(
                *args, **kwargs
            ),
            "отсутству": lambda: self.check.elements.verify_present(
                *args, reverse=True, **kwargs
            ),
            "невиди": lambda: self.check.elements.verify_invisible(
                *args, **kwargs
            ),
        }

    def get_element(self, value: str = None) -> dict[str, Any]:
        """
        Возвращает словарь элементов интерфейса.

        :param value: Значение для форматирования имени элемента.
        :return: Словарь, где ключи — это типы элементов, а значения — локаторы.
        """
        return {
            "кнопка": base_element_locators.BUTTON.format(value=value),
            "поле": base_element_locators.FIELD.format(name=value),
            "заголовок в таблице результатов": base_element_locators.FIELD_IN_SEARCH_RESULT_TABLE.format(
                name=value
            ),
            "чек-бокс": base_element_locators.CHECKBOX_FIELD.format(
                name=value
            ),
            "всплывающее окно": base_element_locators.POPUP_WINDOW,
            "заголовок": base_element_locators.H2_TITLE.format(name=value),
            "пункт меню": base_element_locators.MENU_ITEM.format(item=value),
            "стрелка скачивания": base_element_locators.DOWNLOAD_BUTTON,
            "иконка с галочкой": base_element_locators.SUCCESSFUL_RESULT,
            "иконка с крестиком": base_element_locators.UNSUCCESSFUL_RESULT,
            "предупреждающее сообщение": base_element_locators.WARNING_MESSAGE.format(
                name=value
            ),
            "окно календаря": base_element_locators.CALENDAR_WINDOW,
            "стрелка влево календаря": base_element_locators.ARROW_LEFT_CALENDAR,
            "стрелка вправо календаря": base_element_locators.ARROW_RIGHT_CALENDAR,
            "значение выпадающего списка": base_element_locators.EL_IN_DROPDOWN_LISTBOX.format(
                value=value
            ),
            "тоггл": base_element_locators.TAB.format(name=value),
            "перо редактировать": base_element_locators.PENCIL_EDIT,
            "таблица результатов поиска": base_element_locators.TABLE_OF_SEARCH_RESULT,
            "расширенный поиск": base_element_locators.ADVANCED_FILTER,
            "главная поисковая строка": base_element_locators.FIELD_MAIN_SEARCH,
            "иконка удалить": base_element_locators.DELETE_ICON,
            "иконка-плюс для добавления нового подразделения": base_element_locators.BUTTON_ADD_DEVISION,
            "кнопка редактировать у поля": base_element_locators.BUTTON_EDIT_IN_ROW_TABLE_BY_VALUE.format(
                value=value
            ),
            "кнопка сохранение изменений": base_element_locators.BUTTON_CONFIRM.format(
                value=value
            ),
            "кнопка отменена изменений": base_element_locators.BUTTON_RESET.format(
                value=value
            ),
            "поле редактирования": base_element_locators.FIELD_EDIT.format(
                name=value
            ),
            "чек-бокс дела": inventory_locators.CHECKBOX_CASE.format(
                value=value
            ),
            "поле расширенного поиска": base_element_locators.FIELD_ADVANCED_SEARCH.format(
                name=value
            ),
            "заголовок страницы": base_element_locators.PAGE_TITLE.format(
                value=value
            ),
            "форма": base_element_locators.FORM.format(value=value),
            "выпадающее поле": base_element_locators.FIELD_DIV.format(
                name=value
            ),
        }

    def check_expected_result(
        self,
        element: _ElementTypes,
        name: str,
        expected_result: _ActionsTypes,
        timeout: float | int = 0,
        **kwargs,
    ) -> None:
        """
        Проверка элемента на условия.

        :param element: Тип элемента.
        :param name: Имя элемента.
        :param expected_result: Тип проверки.
        :param timeout: Таймаут ожидания (по умолчанию 0).
        """
        locator = self.get_element(value=name)[element]
        if expected_result != "отсутствует":
            self.interactions.scroll_to(
                locator, use_js=True, timeout=timeout, **kwargs
            )
        normalize_key = self._normalize_key(expected_result)
        action = self.get_checks(locator, timeout=3)[normalize_key]
        action()

    def check_sorted(self, item: str, type_sort: str, checkboxes: str) -> None:
        """
        Проверка сортировки таблицы по возрастанию
        :param item: Наименование столбца, к которому применилась сортировка.
        :param type_sort: Вид сортировки
        :param checkboxes: Флаг, обозначающий сортировку столбца чекбоксов
        """
        key = None
        sort_map = {
            "возрастанию": False,
            "убыванию": True,
        }
        locator = (
            base_element_locators.CHECKBOX_FOR_TEST.format(name=item)
            if checkboxes == "чекбоксов"
            else base_element_locators.COLOMN_IN_TABLE.format(name=item)
        )
        if item == "№":
            key = self.helpers.natural_sort_key
        self.check.records.check_sorting_of_table(
            locator,
            check_checkbox=(checkboxes == "чекбоксов"),
            reverse=sort_map[type_sort],
            key=key,
            timeout=2,
        )

    def check_sorted_by_asc_with_date(self, item: str) -> None:
        """Проверка сортировки таблицы с датами по возрастанию"""
        self.check.records.check_sorting_of_table_with_date(
            base_element_locators.COLOMN_IN_TABLE.format(name=item),
        )

    def check_sorted_by_desc_with_date(self, item: str) -> None:
        """Проверка сортировки таблицы с датами по убыванию"""
        self.check.records.check_sorting_of_table_with_date(
            base_element_locators.COLOMN_IN_TABLE.format(name=item),
            reverse=True,
        )

    def check_result_search_with_advanced_filter(
        self, item: str, type_check: str, value: str
    ) -> None:
        """
        Проверка результатов поиска по полному совпадению в таблице значений
        :param item: Столбец, по которому применялась фильтрация.
        :param value: Значение фильтрации.
        :param type_check: Флаг полноты проверки совпадения строк
        """
        filter_map = {
            "имеет": True,
            "включает": False,
        }
        self.helpers.pause(2)
        if type_check == "не имеет":
            self.check.elements.verify_text(
                locator=base_element_locators.COLOMN_IN_TABLE.format(
                    name=item
                ),
                expected_text=value,
                reverse=True,
            )
        else:
            self.check.records.should_contain_text_in_rows_table(
                locator=base_element_locators.COLOMN_IN_TABLE.format(
                    name=item
                ),
                expected_text=value,
                exact_match=filter_map[type_check],
            )

    def check_state_chip(self, state: str, item: str, value: str) -> None:
        """
        Проверка состояния чипса на странице фильтрации
        :param state: Наименование состояния, регудирующее выбор необходимой проверки.
        :param item: Параметр фильтрации.
        :param value: Значение фильтрации.
        """
        chips = base_element_locators.CHIP_CONTENT.format(
            item=item, value=value
        )
        if state == "появился":
            self.check.elements.verify_visible(chips)
        elif state == "отсутствует":
            self.check.elements.verify_present(chips, reverse=True)

    def check_error_message(self, condition: str, error_message: str) -> None:
        """
        Проверка наличия уведомления об ошибки.

        :param condition: Метка для регулирования проверки на ошибку.
        :param error_message: Сообщение об ошибке.
        """
        error = base_element_locators.ERROR_MESSAGE.format(value=error_message)
        if condition == "отображена":
            self.check.elements.verify_visible(error, timeout=1)
        elif condition == "не отображена":
            self.check.elements.verify_present(error, reverse=True, timeout=1)

    def check_filtering_panel(self, value) -> None:
        """Проверка, что панель фильтрации открыта / закрыта

        :param value: открыта / закрыта
        """
        panel = base_element_locators.FILTERING_PANEL
        if value == "открыта":
            self.check.elements.verify_visible(panel, timeout=1)
        elif value == "закрыта":
            self.check.elements.verify_visible(panel, reverse=True, timeout=1)

    def check_contains_text(self, element: str, expected_text):
        """Проверка, что элемент содержит текст.
        :param element: элемент
        :param expected_text: ожидаемый текст
        """
        _elements = {
            "модальное окно с дополнительной информацией": base_element_locators.MODAL_WINDOW_INFO,
        }
        locator = _elements[element]
        self.interactions.scroll_to(locator, timeout=2)
        self.check.elements.verify_text(locator, expected_text)
