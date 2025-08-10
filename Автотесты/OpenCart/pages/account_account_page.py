from pages.base_page import BasePage
from pages.locators.account_account_locators import AccountAccountLocators as Locator
import allure

class AccountAccountPage(BasePage):
    @allure.step('Нажать "Edit your account information"')
    def click_edit_account_information(self):
        self.logger.info(f'[{self.class_name}] Нажать "Edit your account information"')
        self.get_element(Locator.EDIT_ACCOUNT_INFORMATION_LINK, timeout=1).click()
        return self

    @allure.step('В панели с категорией товаров нажать "Phones & PDAs"')
    def click_PhonesAndPDAs(self):
        self.logger.info(f'[{self.class_name}] В панели с категорией товаров нажать "Phones & PDAs"')
        self.get_element(Locator.PHONESANDPDAS_LINK, timeout=1).click()
        return self

    @allure.step("Клик по логотипу главной страницы")
    def click_main_page_logo(self):
        self.logger.info(f"[{self.class_name}] Клик по логотипу главной страницы")
        self.get_element(Locator.MAIN_PAGE_LOGO, timeout=1).click()
        return self
