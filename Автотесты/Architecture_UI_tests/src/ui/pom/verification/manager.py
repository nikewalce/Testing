from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.pom.verification import records, ui_elements, windows


class CheckManager:
    def __init__(self, browser: WebDriver, logger):
        self.browser = browser
        self.logger = logger
        self._elements = ui_elements.CheckElement(self.browser, self.logger)
        self._records = records.CheckRerord(self.browser, self.logger)
        self._windows = windows.CheckWindow(self.browser, self.logger)

    @property
    def elements(self):
        return self._elements

    @property
    def windows(self):
        return self._windows

    @property
    def records(self):
        return self._records
