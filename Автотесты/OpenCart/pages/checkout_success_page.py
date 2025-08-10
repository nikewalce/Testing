from pages.base_page import BasePage
from pages.locators.checkout_success_page_locators import CheckoutSuccessPageLocators as Locator
import allure

class CheckoutSuccessPage(BasePage):
    @allure.step('В верхней навигационной панели нажать "My account"')
    def click_my_account_button(self):
        self.logger.info(f'[{self.class_name}] В верхней навигационной панели нажать "My account"')
        self.scroll_to_top(2)
        self.get_element(Locator.MY_ACCOUNT_LINK, timeout=5).click()
        return self

    @allure.step('Выбрать "Order History"')
    def click_order_history_button(self):
        self.logger.info(f'[{self.class_name}] Выбрать "Order History"')
        self.get_element(Locator.ORDER_HISTORY_LINK, timeout=5).click()
        return self
