from pages.locators.account_login_locators import AccountLoginPageLocators as Locator
from pages.base_page import BasePage
import allure

class AccountLoginPage(BasePage):
    @allure.step('Заполнить поле "E-Mail" значением "test@test.ru"')
    def enter_email(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "E-Mail" значением "test@test.ru"')
        element = self.get_element(Locator.EMAIL_INPUT, timeout=1)
        element.clear()
        element.send_keys(self.config.register_email)
        return self

    @allure.step('	Заполнить поле "Password" значением "password"')
    def enter_password(self):
        self.logger.info(f'[{self.class_name}] 	Заполнить поле "Password" значением "password"')
        element = self.get_element(Locator.INPUT_PASSWORD, timeout=1)
        element.clear()
        element.send_keys(self.config.register_password)
        return self

    @allure.step('Нажать "Login"')
    def click_login_button(self):
        self.logger.info(f'[{self.class_name}] Нажать "Login"')
        self.get_element(Locator.LOGIN_INPUT, timeout=1).click()
        return self
