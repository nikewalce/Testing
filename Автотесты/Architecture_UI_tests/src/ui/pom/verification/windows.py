from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from src.ui.pom.utils.wait import Wait


class CheckWindow:
    def __init__(self, browser: WebDriver, logger):
        self.browser = browser
        self.logger = logger
        self.wait = Wait(self.browser, self.logger)

    def verify_url(self, expected_url: str, timeout: float | int = 0) -> None:
        """
        Проверяет, что страница открыта.

        :param expected_url: Ожидаемый URL.
        :param timeout: Время ожидания в секундах.
        :return: True, если страница открыта, иначе False.
        :raises AssertionError: Если страница не открыта.
        """
        self.logger.info("Проверка, что страница открыта.")
        try:
            self.wait.wait_for(
                condition=EC.url_contains, url=expected_url, timeout=timeout
            )
            self.logger.debug("Страница открыта")
        except AssertionError as e:
            self.logger.error(f"Страница не открыта: {e}")
            raise e
