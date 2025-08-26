from typing import Callable

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from src.ui.locators.base_locator import Locator


class Wait:
    def __init__(self, browser: WebDriver, logger):
        self.browser = browser
        self.logger = logger

    def wait_for(
        self,
        condition: Callable[[WebDriver], bool],
        locator: Locator = None,
        timeout: float | int = 5,
        reverse: bool = False,
        **kwargs,
    ):
        """Ожидания локатора с условием.

        :param condition: Условие, которое нужно ожидать.
        :param locator: Локатор элемента.
        :param timeout: Время ожидания в секундах.
        :param reverse: Флаг инверсии условия.
        """
        action = "отсутствия" if reverse else "присутствия"
        description = f"Ожидание {action}: {locator if locator else 'условие без локатора'}"
        self.logger.info(description)

        try:
            if isinstance(locator, Locator):
                _locator = (locator.by, locator.value)
            else:
                _locator = locator
            wait = WebDriverWait(self.browser, timeout=timeout)
            condition_func = wait.until_not if reverse else wait.until
            element = condition_func(
                condition(_locator, **kwargs)
                if _locator
                else condition(**kwargs)
            )
            self.logger.debug(f"Успешно: {locator if locator else 'условие'}")
            return element

        except TimeoutException as err:
            error_msg = f"Ошибка: {locator if locator else 'условие'} {'все еще присутствует' if not reverse else 'все еще отсутствует'} после {timeout} секунд"
            self.logger.error(error_msg)
            raise err

        except Exception as e:
            self.logger.error(f"Ошибка: {locator} - {str(e)}")
            raise e
