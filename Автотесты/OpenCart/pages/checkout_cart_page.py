from pages.base_page import BasePage
from pages.locators.checkout_cart_locators import CheckoutCartLocators as Locator
import allure

class CheckoutCartPage(BasePage):
    @allure.step('Нажать кнопку "Checkout"')
    def click_checkout_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Checkout"')
        self.get_element(Locator.CHECKOUT_BUTTON, timeout=1).click()
        return self

    @allure.step('Выбрать "Register Account"')
    def click_input_register_account(self):
        self.logger.info(f'[{self.class_name}] Выбрать "Register Account"')
        self.get_element(Locator.INPUT_REGISTER_ACCOUNT, timeout=1).click()
        return self

    @allure.step('Нажать "Continue"')
    def click_button_continue(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.get_element(Locator.NEW_CUSTOMER_BUTTON_CONTINUE, timeout=3).click()
        return self

    @allure.step('Заполнить поле "First Name" значением "Testname"')
    def enter_firstname(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "First Name" значением "Testname"')
        element = self.get_element(Locator.INPUT_FIRST_NAME, timeout=1)
        element.clear()
        element.send_keys(self.config.register_firstname)
        return self

    @allure.step('Заполнить поле "Last Name" значением "Testlastname"')
    def enter_lastname(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Last Name" значением "Testlastname"]')
        element = self.get_element(Locator.INPUT_LAST_NAME, timeout=1)
        element.clear()
        element.send_keys(self.config.register_lastname)
        return self

    @allure.step('Заполнить поле "E-Mail" значением "test@test.ru"')
    def enter_email(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "E-Mail" значением "test@test.ru"]')
        element = self.get_element(Locator.INPUT_EMAIL, timeout=1)
        element.clear()
        element.send_keys(self.config.register_email)
        return self

    @allure.step('Ввод телефона')
    def enter_phone(self):
        self.logger.info(f"[{self.class_name}] Ввод телефона: {self.config.register_telephone}")
        element = self.get_element(Locator.INPUT_TELEPHONE, timeout=1)
        element.clear()
        element.send_keys(self.config.register_telephone)
        return self

    @allure.step('Заполнить поле "Address 1" значением "Pushkina-Kolotushkina 4"')
    def enter_shipping_address(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Address 1" значением "Pushkina-Kolotushkina 4"]')
        self.scroll_to_end(1)
        element = self.get_element(Locator.INPUT_SHIPPING_ADDRESS1, timeout=1)
        element.clear()
        element.send_keys(self.config.register_shipping_address1)
        return self

    @allure.step('Заполнить поле "City" значением "Testcity"')
    def enter_shipping_city(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "City" значением "Testcity"]')
        element = self.get_element(Locator.INPUT_SHIPPING_CITY, timeout=1)
        element.clear()
        element.send_keys(self.config.register_city)
        return self

    @allure.step('Заполнить поле "Post Code" значением "123456"')
    def enter_shipping_postcode(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Post Code" значением "123456"')
        element = self.get_element(Locator.INPUT_SHIPPING_POSTCODE, timeout=1)
        element.clear()
        element.send_keys(self.config.register_postcode)
        return self

    @allure.step('Выбрать в поле "Country" значение "Antigua and Barbuda"')
    def select_shipping_county(self):
        self.logger.info(f'[{self.class_name}] Выбрать в поле "Country" значение "Antigua and Barbuda"')
        self.get_element(Locator.SELECT_INPUT_SHIPPING_COUNTY, timeout=1).click()
        self.get_element(Locator.OPTION_SHIPPING_COUNTY, timeout=1).click()
        return self

    @allure.step('Выбрать в поле "Region / State" значение "Barbuda"')
    def select_shipping_region(self):
        self.logger.info(f'[{self.class_name}] Выбрать в поле "Region / State" значение "Barbuda"]')
        self.get_element(Locator.SELECT_INPUT_SHIPPING_REGION, timeout=1).click()
        self.get_element(Locator.OPTION_SHIPPING_REGION, timeout=1).click()
        return self

    @allure.step('Заполнить поле "Password" значением "password"')
    def enter_password(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Password" значением "password"')
        element = self.get_element(Locator.INPUT_PASSWORD, timeout=1)
        element.clear()
        element.send_keys(self.config.register_password)
        return self

    @allure.step('Заполнить поле "Password Confirm" значением "password"')
    def enter_password_confirm(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Password Confirm" значением "password"]')
        element = self.get_element(Locator.INPUT_PASSWORD_CONFIRM, timeout=1)
        element.clear()
        element.send_keys(self.config.register_password)
        return self

    @allure.step('Активировать чекбокс "I have read and agree to the Terms & Conditions"')
    def click_checkbox(self):
        self.logger.info(f'[{self.class_name}] Активировать чекбокс "I have read and agree to the Terms & Conditions"')
        self.click_with_scroll(Locator.INPUT_REGISTER_AGREE, timeout=2)
        return self

    @allure.step('Нажать "Continue"')
    def click_continue(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.click_with_scroll(Locator.CONTINUE_BUTTON, timeout=2)
        return self

    @allure.step('Обновить страницу')
    def reload_page(self):
        self.logger.info(f'[{self.class_name}] Обновить страницу')
        self.refresh_page()
        self.presence_of_element_located(Locator.FORM_CHECK_LABEL, timeout=2)
        return self

    @allure.step('В верхней навигационной панели нажать "My account" \n В выпавшем списке нажать "My account"')
    def click_my_account(self):
        self.logger.info(f'[{self.class_name}] В верхней навигационной панели нажать "My account" \n В выпавшем списке нажать "My account"]')
        self.scroll_to_top(5)
        self.get_element(Locator.MY_ACCOUNT_LINK_DROPDOWN, timeout=1).click()
        self.get_element(Locator.MY_ACCOUNT_LINK, timeout=1).click()
        return self

    @allure.step('Нажать кнопку удаления товара "Palm Treo Pro"')
    def click_remove_palm_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку удаления товара "Palm Treo Pro"')
        self.get_element(Locator.REMOVE_PALM_BUTTON, timeout=4).click()
        return self

    @allure.step('В поле "Quantity" ввести значение "2" для товара "Iphone"')
    def enter_quantity_iphone(self):
        self.logger.info(f'[{self.class_name}] В поле "Quantity" ввести значение "2" для товара "Iphone"')
        element = self.get_element(Locator.INPUT_QUANTITY_IPHONE, timeout=1)
        element.clear()
        element.send_keys("2")
        return self

    @allure.step('Нажать кнопку "Update" для количества товара "Iphone"')
    def click_update_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Update" для количества товара "Iphone"')
        self.get_element(Locator.UPDATE_BUTTON, timeout=1).click()
        return self

    @allure.step('Нажать на вкладку "Estimate Shipping & Taxes"')
    def click_estimate_shipping_link(self):
        self.logger.info(f'[{self.class_name}] Нажать на вкладку "Estimate Shipping & Taxes"')
        self.get_element(Locator.ESTIMATE_SHIPPIN_LINK, timeout=1).click()
        return self

    @allure.step('Выбрать в поле "Country" значение "Antigua and Barbuda"')
    def click_select_estimate_country(self):
        self.logger.info(f'[{self.class_name}] Выбрать в поле "Country" значение "Antigua and Barbuda"')
        self.get_element(Locator.SELECT_ESTIMATE_COUNTRY, timeout=1).click()
        self.get_element(Locator.OPTION_SHIPPING_COUNTY, timeout=1).click()
        return self

    @allure.step('Выбрать в поле "Region / State" значение "Barbuda"')
    def click_select_estimate_region(self):
        self.logger.info(f'[{self.class_name}] Выбрать в поле "Region / State" значение "Barbuda"')
        self.get_element(Locator.SELECT_ESTIMATE_REGION, timeout=1).click()
        self.get_element(Locator.OPTION_SHIPPING_REGION, timeout=1).click()
        return self

    @allure.step('Заполнить поле "Post Code" значением "123456"')
    def enter_estimate_postcode(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Post Code" значением "123456"')
        element = self.get_element(Locator.INPUT_ESTIMATE_POSTCODE, timeout=1)
        element.clear()
        element.send_keys(self.config.register_postcode)
        return self

    @allure.step('Нажать кнопку "Get Quotes"')
    def click_get_quotes_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Get Quotes"')
        self.get_element(Locator.GET_QUOTES_BUTTON, timeout=1).click()
        return self

    @allure.step('Нажать кнопку закрытия формы')
    def click_cancel_modal_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку закрытия формы')
        self.get_element(Locator.CANCEL_MODAL_BUTTON, timeout=1).click()
        return self

    @allure.step('Выбрать чек-бох "I want to use an existing address"(если не выбран)')
    def click_checkbox_use_existing_address(self):
        self.logger.info(f'[{self.class_name}] Выбрать чек-бох "I want to use an existing address"(если не выбран)')
        self.get_element(Locator.CHECKBOX_USE_EXISTING_ADDRESS, timeout=1).click()
        return self

    @allure.step('Нажать "Continue"')
    def click_continue_button_payment_address(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.get_element(Locator.CONTINUE_BUTTON_PAYMENT_ADDRESS, timeout=1).click()
        return self

    @allure.step('Выбрать чек-бох "I want to use an existing address"(если не выбран)')
    def click_checkbox_use_existing_shipping_address(self):
        self.logger.info(f'[{self.class_name}] Выбрать чек-бох "I want to use an existing address"(если не выбран)')
        self.get_element(Locator.CHECKBOX_USE_EXISTING_SHIPPING_ADDRESS, timeout=1).click()
        return self

    @allure.step('Нажать "Continue"')
    def click_continue_button_shipping_address(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.get_element(Locator.CONTINUE_BUTTON_SHIPPING_ADDRESS, timeout=1).click()
        return self

    @allure.step('В поле "Add Comments" добавить текст из 10 символов')
    def enter_comment_textarea(self):
        self.logger.info(f'[{self.class_name}] В поле "Add Comments" добавить текст из 10 символов')
        element = self.get_element(Locator.COMMENT_TEXTAREA, timeout=1)
        element.clear()
        element.send_keys("TEXTONETWO")
        return self

    @allure.step('Нажать "Continue"')
    def click_continue_button_shipping_method(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.get_element(Locator.CONTINUE_BUTTON_SHIPPING_METHOD, timeout=1).click()
        return self

    @allure.step('Нажать "Continue"')
    def click_continue_button_payment_method(self):
        self.logger.info(f'[{self.class_name}] Нажать "Continue"')
        self.get_element(Locator.CONTINUE_BUTTON_PAYMENT_METHOD, timeout=1).click()
        return self

    @allure.step('Нажать "Confirm Order"')
    def click_confirm_order_button(self):
        self.logger.info(f'[{self.class_name}] Нажать "Confirm Order"')
        self.get_element(Locator.CONFIRM_ORDER_BUTTON, timeout=1).click()
        return self
