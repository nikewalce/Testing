from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
import logging
import allure
from config import Config
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.config = Config()
        self.logger = getattr(browser, 'logger', self._create_logger())
        self.class_name = type(self).__name__

    def _create_logger(self):
        logger = logging.getLogger("selenium_test_log")
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            # Запись в файл
            file_handler = logging.FileHandler("diplom.log", mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            # Формат логов
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def take_screenshot(self):
        """Сделать скриншот страницы и приложить к allure отчету"""
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    def allert(self):
        try:
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.accept()
            self.logger.info(f"[{self.class_name}] Alert найден и закрыт")
        except NoAlertPresentException:
            self.logger.debug(f"[{self.class_name}] Нет алерта")
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Ошибка при работе с alert: {e}")
            raise

    def get_element(self, locator, timeout):
        self.logger.info(f"Получение элемента: {locator}")
        try:
            return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Ошибка при получении элемента {locator}: {e}")
            raise

    def presence_of_element_located(self, locator, timeout):
        try:
            return WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Элемент не найден (presence_of): {locator}, {e}")
            raise

    def refresh_page(self):
        try:
            actions = ActionChains(self.browser)
            actions.key_down(Keys.CONTROL).send_keys('r').key_up(Keys.CONTROL).perform()
            self.logger.info(f"[{self.class_name}] Страница перезагружена через Ctrl+R")
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Ошибка при обновлении страницы: {e}")
            raise

    def text_to_be_present_in_element(self,  locator, text, timeout):
        self.logger.info(f"[{self.class_name}] Проверка наличия текста '{text}' в элементе {locator}")
        try:
            return WebDriverWait(self.browser, timeout).until(EC.text_to_be_present_in_element(locator, text))
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Текст '{text}' не найден в элементе: {locator}, {e}")
            raise

    def mouseover(self, locator, timeout):
        try:
            self.logger.info(f"[{self.class_name}] Наведение на элемент: {locator}")
            element = self.get_element(locator, timeout=timeout)
            actions = ActionChains(self.browser)
            actions.move_to_element(element).perform()
        except Exception as e:
            self.logger.error(f"[{self.class_name}] Ошибка при наведении на элемент {locator}: {e}")
            raise

    def scroll_to_top(self, count_scrolling: int):
        self.logger.debug(f"Скроллинг вверх через ActionChains ({count_scrolling} раз Page Up)")
        actions = ActionChains(self.browser)
        for _ in range(count_scrolling):
            actions.send_keys(Keys.PAGE_UP).pause(0.2).perform()
        self.logger.debug("Скроллинг вверх завершен")

    def scroll_to_end(self, count_scrolling: int):
        self.logger.debug(f"Скроллинг вниз через ActionChains ({count_scrolling} раз Page Down)")
        actions = ActionChains(self.browser)
        for _ in range(count_scrolling):
            actions.send_keys(Keys.PAGE_DOWN).pause(0.2).perform()
        self.logger.debug("Скроллинг вниз завершен")

    def click_with_scroll(self, locator, timeout):
        self.logger.debug("Ожидание элемента для клика с прокруткой: %s", locator)
        element = WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        actions = ActionChains(self.browser)
        actions.move_to_element(element).pause(0.2).perform()
        element.click()
        self.logger.info("Клик выполнен по элементу: %s", locator)
