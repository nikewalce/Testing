import re

from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class BaseHelpers:
    """Класс методов для вспомогательных функций"""

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.actions = ActionChains(browser)
        self.class_name = type(self).__name__

    def execute_script(self, script: str, *args, **kwargs):
        """
        Выполняет скрипт в браузере.

        :param script: Скрипт для выполнения.
        :param kwargs: Дополнительные аргументы для скрипта.
        """
        self.browser.execute_script(script, *args, **kwargs)

    def pause(self, timeout: float | int = 0):
        """
        Пауза в тесте.

        :param timeout: Время паузы.
        """
        try:
            self.actions.pause(timeout).perform()
            self.logger.debug(
                f"{self.class_name}: Пауза в тесте {timeout} сек."
            )
        except Exception as e:
            self.logger.error(f"{self.class_name}: Ошибка при паузе в тесте.")
            raise e

    def press_enter(self):
        """
        Нажатие клавиши Enter.
        """
        try:
            self.actions.send_keys(Keys.ENTER).perform()
            self.logger.debug(f"{self.class_name}: Нажата клавиша Enter.")
        except Exception as e:
            self.logger.error(
                f"{self.class_name}: Ошибка при нажатии клавиши Enter."
            )
            raise e

    def wait_for_js_to_load(self, timeout: float | int = 0):
        """
        Ожидает завершения выполнения JavaScript на странице.

        :param timeout: Максимальное время ожидания завершения выполнения JavaScript в секундах.
        """
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.execute_script("return document.readyState")
            == "complete"
        )

    def natural_sort_key(self, value: str):
        """Функция для извлечения чисел из строк"""
        return [int(num) for num in re.findall(r"\d+", value)]

    def move_to_action(self, slider, pixels):
        """Функция, которая скролит слайдер на pixels"""
        self.actions.click_and_hold(slider).move_by_offset(0, pixels).release().perform()