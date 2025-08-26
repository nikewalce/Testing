from decouple import config
from dotenv import load_dotenv

from src.ui.pom.core.base_manager import BaseManager
from src.ui.pom.pages.base_element.locators import base_element_locators
from src.ui.pom.pages.base_element.test_data.text_before_2_kb_and_after import (
    generate_text_by_size,
)
from src.ui.pom.pages.e_dock import locators as e_dock_locators
from src.ui.pom.pages.inventory_page.locators import inventory_locators

load_dotenv()


class BaseElementPage(BaseManager):
    """Набор методов работы с базовыми элементами, существующими на всех страницах"""

    @property
    def authorization_page(self):
        if not hasattr(self, "_authorization_page"):
            from src.ui.pom.pages.authorization import AuthorizationPage

            self._authorization_page = AuthorizationPage(self.browser)
        return self._authorization_page

    def click_first_record_in_table(self) -> None:
        """Клик на первую запись в таблице сущностей"""
        self.interactions.click_on(
            base_element_locators.LINES_IN_TABLE, timeout=3, use_js=True
        )

    def point_sort(self, item: str) -> None:
        """Наведение курсора на кнопку сортировки
        :param item: Наименование столбца, к которому применяется наведение курсора.
        """
        self.interactions.scroll_to(
            base_element_locators.SORTED_BUTTON.format(name=item), timeout=2
        )
        self.interactions.point_to_element(
            base_element_locators.SORTED_BUTTON.format(name=item), timeout=2
        )

    def get_original_values(self, item: str, checkboxes: str) -> None:
        """Получение исходных значений столбца до сортировки
        :param item: Наименование столбца, к которому применяется получение исходных значений.
        :param checkboxes: Флаг, который обозначает столбец чекбоксов
        """
        self.helpers.pause(1)
        rows = self.records.parsing_rows(
            base_element_locators.COLOMN_IN_TABLE.format(name=item)
        )
        if checkboxes == "чекбоксов":
            rows = self.records.parse_checkboxes(
                base_element_locators.CHECKBOX_FOR_TEST.format(name=item)
            )
        return rows

    def click_sort(self, item: str) -> None:
        """Клик на кнопку сортировки
        :param item: Наименование столбца, к которому применяется сортировка.
        """
        self.interactions.click_on(
            base_element_locators.SORTED_BUTTON.format(name=item)
        )

    def click_button(self, item: str, use_js: bool = False) -> None:
        """Клик на кнопку
        :param item: Наименование кнопки.
        :param use_js: параметр применения js скрипта."""
        button = base_element_locators.BUTTON.format(value=item)
        self.interactions.scroll_to(button, use_js=use_js, timeout=3)
        self.interactions.click_on(
            button,
            use_js=use_js,
            timeout=3,
        )

    def click_on_cross_for_clear_field(self, value: str) -> None:
        """Клик на кнопку очистки поля
        :param value: Наименование поля, к которому применяется очистка."""
        clear_field = base_element_locators.BUTTON_CLEAR_FIELD.format(
            value=value
        )
        self.interactions.scroll_to(clear_field, use_js=True, timeout=2)
        self.interactions.point_to_element(clear_field, timeout=2)
        self.interactions.click_on(clear_field, timeout=1)

    def click_button_script(self, script, value) -> None:
        """
        Выполняет клик по кнопке в зависимости от сценария.
        """
        if script == "внизу страницы":
            self.click_button(item=value, use_js=True)
        elif script == "страницы":
            self.click_button(item=value)
        elif script == "очистки поля":
            self.click_on_cross_for_clear_field(value=value)
        elif script == "в модальном окне":
            self.click_button_in_modal_window(item=value)
        else:
            raise ValueError(f"Неизвестный сценарий: {script}")

    def click_checkbox(self, item, use_js=False) -> None:
        """Клик по чек-боксу."""
        element = base_element_locators.CHECKBOX_FIELD.format(name=item)
        self.interactions.scroll_to(element)
        self.interactions.click_on(element, use_js=use_js)

    def click_checkbox_script(self, script, value) -> None:
        """
        Выполняет клик по чек-боксу в зависимости от сценария.
        """
        if script == "внизу страницы":
            self.click_checkbox(item=value, use_js=True)
        elif script == "страницы":
            self.click_checkbox(item=value)
        elif script == "в модальном окне":
            self.click_checkbox_in_modal_window(item=value)
        else:
            raise ValueError(f"Неизвестный сценарий: {script}")

    def click_field(self, item, use_js=False) -> None:
        """Клик по полю."""
        element = base_element_locators.FIELD.format(name=item)
        self.interactions.scroll_to(element)
        self.interactions.click_on(element, use_js=use_js)

    def click_field_script(self, script, value) -> None:
        """
        Выполняет клик по полю в зависимости от сценария.
        """
        if script == "внизу страницы":
            self.click_field(item=value, use_js=True)
        elif script == "страницы":
            self.click_field(item=value)
        elif script == "в модальном окне":
            self.click_field_in_modal_window(item=value, use_js=True)
        else:
            raise ValueError(f"Неизвестный сценарий: {script}")

    def perform_click_action(self, element, script, value) -> None:
        """
        Выполняет действие клика на элемент
        в зависимости от его типа и сценария.
        """
        actions = {
            "кнопку": self.click_button_script,
            "чек-бокс": self.click_checkbox_script,
            "поле": self.click_field_script,
            "стрелку": self.click_arrow_script,
            "вкладку": lambda script, value: self.click_on_tab(value),
            "breadcrumbs": self.click_breadcrumbs_script,
            "значок": self.click_bell_ring_script,
            "ссылку": self.click_link_script,
        }
        try:
            actions[element](script, value)
        except ValueError:
            raise ValueError(f"Неизвестный элемент: {element}")

    def click_input_filter(self, item: str, pre_condition) -> None:
        """
        Клик на поле расширенного поиска
        :param item: Наименование поля расширенного поиска.
        """
        if pre_condition == "в семантическом поиске":
            element = e_dock_locators.SEMANTIC_FIELD.format(name=item)
        else:
            element = base_element_locators.FIELD_ADVANCED_SEARCH.format(
                name=item
            )

        self.interactions.scroll_to(element, timeout=3, use_js=True)
        self.interactions.click_on(element, timeout=3)

    def click_on_value_in_dropdown_advanced_filter(self, item: str) -> None:
        """
        Кликнуть на значение в  поле расширенного фильтра
        :param item: Значение расширенной фильтрации.
        """
        self.interactions.click_on(
            base_element_locators.EL_IN_DROPDOWN_LISTBOX.format(value=item),
            timeout=2,
        )

    def click_arrow_back_button(self) -> None:
        """Клик на стрелку назад"""
        self.interactions.click_on(
            base_element_locators.BACK_ARROW_BUTTON, timeout=2
        )

    def click_arrow_left_button(self) -> None:
        """Клик на стрелку влево"""
        self.interactions.scroll_to(
            base_element_locators.ARROW_LEFT_CALENDAR, timeout=2
        )
        self.interactions.click_on(
            base_element_locators.ARROW_LEFT_CALENDAR, timeout=2
        )

    def click_breadcrumbs_script(self, script: str, value: str) -> None:
        """
        Клик на хлебную крошку
        :param script: Регулирует применение js-скрипта к элементу
        :param value: Наименование хлебной крошки
        """
        if script == "страницы":
            self.interactions.click_on(
                base_element_locators.CLICKABLE_BREADCRUMBS.format(name=value),
                timeout=2,
            )

    def click_bell_ring_script(self, script: str, value: str) -> None:
        if script == "страницы" and value == "Уведомления":
            self.interactions.click_on(
                base_element_locators.BELL_RING_BUTTON, use_js=True, timeout=2
            )

    def click_link_script(self, script: str, value: str) -> None:
        if script == "страницы":
            self.interactions.click_on(
                base_element_locators.LINK_OBJECT.format(value=value)
            )

    def click_arrow_script(self, script, value) -> None:
        """Клик на стрелку"""
        if script == "страницы" and value == "Назад":
            self.click_arrow_back_button()
        elif script == "в модальном окне":
            self.click_on_arrow_in_modal_window(value)
        elif script == "влево календаря":
            self.click_arrow_left_button()

    def click_on_arrow_in_modal_window(self, value, use_js=True):
        """
        Клик на стрелку в модальном окне

        :param value(str) : Значение поля.
        """
        self.interactions.click_on(
            base_element_locators.ARROW_IN_MODAL_WINDOW.format(name=value),
            use_js=use_js,
            timeout=3,
        )

    def click_field_in_modal_window(self, item, use_js=False):
        """Клик по полю в модальном окне."""
        element = base_element_locators.FIELD_IN_MODAL_WINDOW.format(name=item)
        self.interactions.scroll_to(element, timeout=2)
        self.interactions.click_on(element, timeout=2, use_js=use_js)

    def click_checkbox_in_modal_window(self, item, use_js=True):
        """Клик по чекбоксу в модальном окне."""
        element = base_element_locators.CHECKBOX_IN_MODAL_WINDOW.format(
            name=item
        )
        self.interactions.scroll_to(element)
        self.interactions.click_on(element, timeout=2, use_js=use_js)

    def click_button_in_modal_window(self, item, use_js=False):
        """Клик по кнопке в модальном окне."""
        element = base_element_locators.BUTTON_IN_MODAL_WINDOW.format(
            name=item
        )
        self.interactions.scroll_to(element)
        self.interactions.click_on(element, timeout=2, use_js=use_js)

    def fill_field_main_search(self, text: str) -> None:
        """Заполнить поле главной поисковой строки."""
        if text in ["до 2 КБ", "больше 2 КБ"]:
            text = generate_text_by_size(text)
        self.interactions.input_text(
            base_element_locators.FIELD_MAIN_SEARCH, text, timeout=1
        )

    def click_on_tab(self, value: str) -> None:
        """Клик на вкладку."""
        element = base_element_locators.TAB.format(name=value)
        self.interactions.scroll_to(element, timeout=2)
        self.interactions.click_on(element, timeout=2)

    def input_value_in_field_with_placeholder(
        self, context, placeholder: str, value: str
    ) -> None:
        """
        Ввести значение в поле с подсказкой.

        :param placeholder: Наименование поля.
        :param value: Значение в поле.
        """
        if not hasattr(context, "filled_data"):
            context.filled_data = {}
        element = base_element_locators.FIELD_BY_PLACEHOLDER.format(
            name=placeholder
        )
        self.interactions.click_on(element)
        self.interactions.input_text(element, value)

        if placeholder == "гггг":
            self.interactions.click_on(
                inventory_locators.EL_IN_DROPDOWN_YEAR.format(value=value)
            )

        context.filled_data[placeholder] = value

    def input_text_in_filed(
        self, context, field, value: str = None, _input=None
    ) -> None:
        """Ввести текст в поле."""
        if _input == "ввода":
            _field = base_element_locators.FIELD_SIBLING.format(name=field)
        else:
            _field = base_element_locators.FIELD.format(name=field)

        self.interactions.scroll_to(_field, timeout=5)

        if field == "Подтверждение пароля" and value is None:
            value = context.save_value
        elif value == "пароль юзера с 2хфакторной аутентификацией":
            value = config("ARCHIVIST_WITH_2FA_PASS")
        elif field == "Код подтверждения" and value is None:
            self.helpers.pause(20)
            value = self.authorization_page.get_verification_code(
                message_type="проверочный код"
            )
        self.interactions.input_text(_field, value, timeout=3)
