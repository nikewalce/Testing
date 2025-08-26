import random

from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.ui.locators.base_locator import Locator


class BaseInteractions:
    """Класс для методов работы с базовыми действиями над элементами"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.actions = ActionChains(browser)
        self.class_name = type(self).__name__

    @property
    def base(self):
        from src.ui.pom.core.base_manager import BaseManager

        return BaseManager(self.browser)

    def click_on(
        self,
        locator: Locator | WebElement,
        timeout: float | int = 0,
        pause: float | int = 0,
        use_js: bool = False,
    ):
        """
        Кликает по элементу на странице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :param pause: Время ожидания перед кликом.
        :param use_js: Использовать ли JS для клика

        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.find_element(locator, timeout)
        try:
            if use_js:
                self.base.helpers.execute_script(
                    "arguments[0].click();", element
                )
                self.logger.debug(
                    f"{self.class_name}: JS клик по элементу с локатором: {locator}"
                )
            else:
                self.actions.move_to_element(element).pause(
                    pause
                ).click().perform()
                self.logger.debug(
                    f"{self.class_name}: Клик по элементу с локатором: {locator}"
                )
        except Exception as e:
            click_type = "JS клике" if use_js else "клике"
            self.logger.error(
                f"{self.class_name}: Ошибка при {click_type} по элементу с локатором: {locator}"
            )
            raise e

    def click_on_presence(
        self,
        locator: Locator | WebElement,
        timeout: float | int = 0,
        pause: float | int = 0,
        use_js: bool = False,
    ):
        """
        Кликает по элементу на странице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :param pause: Время ожидания перед кликом.
        :param use_js: Использовать ли JS для клика

        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.present_element(locator, timeout)
        try:
            if use_js:
                self.base.helpers.execute_script(
                    "arguments[0].click();", element
                )
                self.logger.debug(
                    f"{self.class_name}: JS клик по элементу с локатором: {locator}"
                )
            else:
                self.actions.move_to_element(element).pause(
                    pause
                ).click().perform()
                self.logger.debug(
                    f"{self.class_name}: Клик по элементу с локатором: {locator}"
                )
        except Exception as e:
            click_type = "JS клике" if use_js else "клике"
            self.logger.error(
                f"{self.class_name}: Ошибка при {click_type} по элементу с локатором: {locator}"
            )
            raise e

    def go_to_page(self, url: str, wait_locator, timeout: float | int = 5):
        """
        Переходит на указанную страницу и ожидает, что она загрузится.

        :param url: Адрес страницы, на которую нужно перейти.
        :param timeout: Время ожидания загрузки страницы.
        :param wait_locator: Локатор, по которому ожидается загрузка страницы
        """
        try:
            current_url = self.browser.current_url
            if current_url == url:
                self.logger.debug(f"{self.class_name}: Уже на странице {url}")
                return

            self.logger.debug(f"{self.class_name}: Переход на страницу: {url}")
            self.browser.get(url)

            # Ждём появления основного элемента страницы
            self.base.wait.wait_for(
                condition=EC.presence_of_element_located,
                locator=wait_locator,
                timeout=timeout,
            )
            self.logger.debug(f"{self.class_name}: Страница {url} успешно загружена")

        except Exception as e:
            self.logger.error(f"{self.class_name}: Ошибка при переходе на {url}")
            raise

    def go_back(
            self,
            pause: float | int = 0,
            use_js: bool = False,
    ):
        """
        Выполняет переход назад в истории браузера.

        :param pause: Время ожидания перед выполнением действия.
        :param use_js: Использовать ли JS для перехода назад.
        """
        try:
            if pause:
                self.base.helpers.sleep(pause)

            if use_js:
                self.base.helpers.execute_script("window.history.back();")
                self.logger.debug(f"{self.class_name}: Выполнен переход назад через JS")
            else:
                self.browser.back()
                self.logger.debug(f"{self.class_name}: Выполнен переход назад через WebDriver")
        except Exception as e:
            method = "JS переходе назад" if use_js else "переходе назад через WebDriver"
            self.logger.error(f"{self.class_name}: Ошибка при {method}")
            raise e

    def refresh_page(
            self,
            pause: float | int = 0,
            use_js: bool = False,
    ):
        """
        Обновляет текущую страницу.

        :param pause: Время ожидания перед обновлением.
        :param use_js: Использовать ли JS для обновления страницы.
        """
        try:
            if pause:
                self.base.helpers.sleep(pause)

            if use_js:
                self.base.helpers.execute_script("location.reload();")
                self.logger.debug(f"{self.class_name}: Страница обновлена через JS")
            else:
                self.browser.refresh()
                self.logger.debug(f"{self.class_name}: Страница обновлена через WebDriver")
        except Exception as e:
            method = "JS обновлении" if use_js else "обновлении через WebDriver"
            self.logger.error(f"{self.class_name}: Ошибка при {method} страницы")
            raise e

    def set_slider_top(self, locator: Locator | WebElement, pixels: int, timeout: float | int = 5):
        """
        Опускает слайдер меню на pixels
        :param locator: локатор слайдера
        :param pixels: кол-во пикселей, на которой будет опущен слайдер
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.present_element(locator, timeout)
        try:
            self.base.helpers.move_to_action(element, pixels)
            self.logger.debug(
                f"{self.class_name}: Меню прокручено на {pixels} пикселей вниз"
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при скроле меню"
            )
            raise e

    def scroll_to(
        self,
        locator: Locator | WebElement,
        timeout: float | int = 0,
        use_js: bool = False,
    ):
        """
        Прокручивает страницу к элементу

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        :param use_js: Признак использования JavaScript.
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.present_element(locator, timeout)
        try:
            if use_js:
                self.base.helpers.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    element,
                )
            else:
                self.actions.scroll_to_element(element).perform()
            self.logger.debug(
                f"{self.class_name}: Страница прокручена к элементу \
                с локатором: {locator}"
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при скроле к элементу \
                с локатором: {locator}"
            )
            raise e

    def click_random_link(self, locator: str, timeout: float | int = 0):
        """
        Наводит и нажимает на случайную ссылку в таблице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания локатора.
        """
        self.logger.info(
            f"Нажатие на случайную ссылку в таблице по локатору {locator}"
        )
        try:
            rows = self.base.elements.find_elements(locator, timeout)
            if len(rows) == 0:
                self.logger.warning(
                    f"Таблица по локатору {locator} не содержит записей."
                )
                return
            random_row = random.choice(rows)
            random_row.click()
            self.logger.debug(
                f"Случайная ссылка была нажата в таблице по локатору {locator}."
            )

        except Exception as e:
            self.logger.error(
                f"Ошибка при попытке нажать на случайную ссылку в таблице по локатору {locator}."
            )
            raise e

    def get_input_value(
            self, locator: Locator | WebElement, timeout: float | int = 0 ) -> str:
        """
        Получает текущее значение поля ввода.

        :param locator: Локатор или элемент поля.
        :param timeout: Время ожидания, если передан локатор.
        :return: Строковое значение, содержащееся в поле.
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.find_element(locator, timeout)

        try:
            value = element.get_attribute("value")
            self.logger.debug(
                f"{self.class_name}: Получено значение '{value}' из поля с локатором {locator}"
            )
            return value
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при получении значения из поля с локатором {locator}"
            )
            raise e

    def get_element_text(self, locator: Locator | WebElement, timeout: float | int = 0) -> str:
        """
        Получает текст из элемента
        :param locator: локатор из которого нужно получить текст
        :param timeout: время ожидания
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.find_element(locator, timeout)

        try:
            text = element.text
            self.logger.debug(f"{self.class_name}: Получен текст '{text}' из элемента {locator}")
            return text
        except Exception as e:
            self.logger.error(f"{self.class_name}: Ошибка при получении текста из элемента {locator}")
            raise e

    def get_element_color_property(
            self,
            locator: Locator | WebElement,
            css_property: str,
            timeout: float | int = 0
    ) -> str:
        """
        Получает значение CSS-свойства цвета у элемента (например, 'border-color', 'color', 'background-color').

        :param locator: Локатор или WebElement.
        :param css_property: Название CSS-свойства (например, 'border-color').
        :param timeout: Время ожидания элемента на странице.
        :return: Значение CSS-свойства (например, 'rgb(255, 0, 0)').
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.find_element(locator, timeout)

        try:
            value = element.value_of_css_property(css_property)
            self.logger.debug(
                f"{self.class_name}: Значение CSS-свойства '{css_property}' для элемента {locator}: '{value}'"
            )
            return value
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при получении CSS-свойства '{css_property}' у элемента {locator}"
            )
            raise e

    def input_text(
        self,
        locator: Locator | WebElement,
        text: str,
        timeout: float | int = 0,
    ):
        """
        Вводит текст в элемент на странице.
        :param locator: Локатор элемента.
        :param text: Текст для ввода в элемент.
        :param timeout: Время ожидания локатора.
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.base.elements.find_element(locator, timeout)
        try:
            element.click()
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(text)
            self.logger.debug(
                f"{self.class_name}: Введён текст `{text}` в элемент \
                с локатором: {locator}"
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при вводе текста в элемент \
                с локатором: {locator}"
            )
            raise e

    def point_to_element(self, locator: Locator, timeout: float | int = 0):
        """
        Наведение курсора на элемент
        :param locator: Локатор для нахождения элемента на странице.
        :param timeout: Время ожидания локатора.
        """
        try:
            if isinstance(locator, WebElement):
                element = locator
            else:
                element = self.base.elements.present_element(locator, timeout)
            self.actions.move_to_element(element).perform()
            self.logger.debug(
                f"{self.class_name}: Наведение курсора на элемент с локатором {locator}"
            )
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при наведении на элемент с локатором {locator}"
            )
            raise e

    def upload_file(
        self, locator: Locator, file_path: str, timeout: float | int = 0
    ) -> None:
        """
        Загружает файл через элемент ввода типа file.

        :param locator: Локатор элемента ввода типа file.
        :param file_path: Путь к файлу для загрузки.
        :param timeout: Время ожидания локатора.
        """
        try:
            element: WebElement = self.base.elements.present_element(
                locator=locator, timeout=timeout
            )
            element.send_keys(file_path)
            self.logger.info(f"{self.class_name}: Файл загружен: {file_path}")
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при загрузке файла по локатору: {locator}, \
                путь к файлу: {file_path}"
            )
            raise e

    def click_subsequent_field(
        self,
        locator: Locator,
        position: str,
        use_js: bool = False,
        timeout: float | int = 0,
    ) -> None:
        """
        Кликнуть на последующее поле одноименного фильтра
        :param locator: Локатор поля, к которому применяется метод
        :param position: Параметр, устанавливающий какое поле кликнуть
        :param use_js: Параметр использования js скрипта
        :param timeout: Время ожидания локатора.
        """
        position_fields = {
            "первое": 0,
            "второе": 1,
            "третье": 2,
            "четвертое": 3,
        }
        fields = self.base.elements.present_elements(locator, timeout)
        self.scroll_to(fields[position_fields[position]], use_js=use_js)
        self.click_on(fields[position_fields[position]], timeout)
