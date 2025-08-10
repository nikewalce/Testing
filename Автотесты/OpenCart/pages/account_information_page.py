from pages.base_page import BasePage
from pages.locators.account_information_locators import AccountInformationLocators as Locator
import allure

class AccountInformationPage(BasePage):
    @allure.step('Проверка, что данные совпадают с указанными при оформлении')
    def check_data(self):
        self.logger.info(f"[{self.class_name}] Проверка, что данные совпадают с указанными при оформлении")
        firstname = self.get_element(Locator.INPUT_FIRSTNAME, timeout=1).get_attribute("value")
        lastname = self.get_element(Locator.INPUT_LASTNAME, timeout=1).get_attribute("value")
        email = self.get_element(Locator.INPUT_EMAIL, timeout=1).get_attribute("value")
        telephone = self.get_element(Locator.INPUT_TELEPHONE, timeout=1).get_attribute("value")
        return True if (firstname, lastname, email, telephone) == (self.config.register_firstname, self.config.register_lastname, self.config.register_email, self.config.register_telephone) else False
