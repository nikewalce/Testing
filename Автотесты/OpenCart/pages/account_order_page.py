from pages.base_page import BasePage
from pages.locators.account_order_page_locators import AccountOrderPageLocators as Locator
import allure

class AccountOrderPage(BasePage):
    @allure.step('Нажать "View" для ранее созданного заказа')
    def click_view_button(self):
        self.logger.info(f'[{self.class_name}] Нажать "View" для ранее созданного заказа')
        self.get_element(Locator.VIEW_LINK, timeout=1).click()
        return self

    @allure.step('Нажать кнопку "Return" для ранее заказанного товара')
    def click_return_link(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Return" для ранее заказанного товара')
        self.get_element(Locator.RETURN_LINK, timeout=1).click()
        return self

    @allure.step('Заполнить поле "Telephone" любым 11-и значным номером')
    def enter_telephone(self):
        self.logger.info(f'[{self.class_name}] Заполняем поле "Telephone" любым 11-и значным номером')
        telephone = '12345678910'
        telephone_input = self.get_element(Locator.INPUT_TELEPHONE, timeout=1)
        telephone_input.clear()
        telephone_input.send_keys(telephone)
        return self

    @allure.step('В поле "Reason for Return" нажать на любой чекбокс')
    def click_reason_for_return_checkbox(self):
        self.logger.info(f'[{self.class_name}] В поле "Reason for Return" нажать на любой чекбокс')
        self.get_element(Locator.REASON_FOR_RETURN_CHECKBOX, timeout=1).click()
        return self

    @allure.step('Нажать "Submit"')
    def click_submit_button(self):
        self.logger.info(f'[{self.class_name}] ')
        self.get_element(Locator.SUBMIT_RETURN_BUTTON, timeout=1).click()
        return self

    @allure.step('Открыта история заказов. Проверяем, что в ней присутствует созданный заказ')
    def check_customer_info(self):
        self.logger.info(f'[{self.class_name}] Открыта история заказов. Проверяем, что в ней присутствует созданный заказ]')
        self.get_element(Locator.VIEW_LINK, timeout=1).click()
        product_name = self.get_element(Locator.IPHONE_TD, timeout=1).text
        address_info = self.get_element(Locator.ADDDRESS_INFO, timeout=1).text
        return (product_name == "iPhone") and (self.config.register_firstname in address_info) and (self.config.register_city in address_info)
