from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.pom.core import (
    elements,
    helpers,
    interactions,
    records,
    select,
    style,
)
from src.ui.pom.utils.wait import Wait
from src.ui.pom.verification.manager import CheckManager


class BaseManager:
    """Менеджер работы с базовым функционалом"""

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.logger = browser.logger
        self._elements = elements.BaseElements(self.browser, self.logger)
        self._helpers = helpers.BaseHelpers(self.browser, self.logger)
        self._interactions = interactions.BaseInteractions(
            self.browser, self.logger
        )
        self._select = select.BaseSelect(self.browser, self.logger)
        self._records = records.BaseRecords(self.browser, self.logger)
        self._style = style.BaseStyle(self.browser, self.logger)
        self.check = CheckManager(self.browser, self.logger)
        self.wait = Wait(self.browser, self.logger)

    @property
    def elements(self):
        return self._elements

    @property
    def helpers(self):
        return self._helpers

    @property
    def interactions(self):
        return self._interactions

    @property
    def select(self):
        return self._select

    @property
    def records(self):
        return self._records

    @property
    def style(self):
        return self._style
