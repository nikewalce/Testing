import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    LOCATORS = {
        "О нас": (By.LINK_TEXT, "[ О нас ]"),
        "Услуги": (By.LINK_TEXT, "[ Услуги ]"),
        "Проекты": (By.LINK_TEXT, "[ Проекты ]"),
        "Отзывы": (By.LINK_TEXT, "[ Отзывы ]"),
        "Контакты": (By.LINK_TEXT, "[ Контакты ]")
    }

    @allure.step("Клик по ссылке: {link_text}")
    def click_link(self, link_text):
        element = self.wait.until(EC.element_to_be_clickable(self.LOCATORS[link_text]))
        element.click()

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url
