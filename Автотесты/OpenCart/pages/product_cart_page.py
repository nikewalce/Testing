from pages.base_page import BasePage
from pages.locators.product_cart_page_locators import CartProductLocators as Locator
import allure
import os
import time
import pyautogui

class ProductCartPage(BasePage):
    @allure.step('В разделе "Available Options" в поле "Select" выбрать цвет "Red"')
    def click_select_available_options_dropdown_button(self):
        self.logger.info(f'[{self.class_name}] В разделе "Available Options" в поле "Select" выбрать цвет "Red"')
        self.get_element(Locator.SELECT_AVAILABLE_OPTIONS_DROPDOWN_LIST, timeout=1).click()
        self.get_element(Locator.OPTION_RED, timeout=1).click()
        return self

    @allure.step('В разделе "Available Options" в поле "Qty" ввести количество товара "2"')
    def qty_entry(self):
        self.logger.info(f'[{self.class_name}] В разделе "Available Options" в поле "Qty" ввести количество товара "2"')
        qty = 2
        element = self.get_element(Locator.INPUT_QTY, timeout=1)
        element.clear()
        element.send_keys(qty)
        return self

    @allure.step('Добавить товар в корзину. Нажать кнопку "Add to Cart"')
    def click_add_to_cart_button(self):
        self.logger.info(f'[{self.class_name}] Добавить товар в корзину. Нажать кнопку "Add to Cart"')
        self.get_element(Locator.ADD_TO_CART_BUTTON, timeout=1).click()
        return self

    @allure.step('В верхней навигационной панели нажать "Shopping Cart"')
    def click_shopping_cart(self):
        self.logger.info(f'[{self.class_name}] В верхней навигационной панели нажать "Shopping Cart"')
        self.get_element(Locator.SHOPPING_CART_BUTTON, timeout=3).click()
        return self

    @allure.step('Выбрать чекбокс "Medium" для опции "Radio"')
    def click_radio_medium_checkbox(self):
        self.logger.info(f'[{self.class_name}] Выбрать чекбокс "Medium" для опции "Radio"')
        self.get_element(Locator.RADIO_MEDIUM_CHECKBOX, timeout=1).click()
        return self

    @allure.step('Выбрать чекбокс "Checkbox 3" для опции "Checkbox"')
    def click_checkbox3(self):
        self.logger.info(f'[{self.class_name}] Выбрать чекбокс "Checkbox 3" для опции "Checkbox"')
        self.click_with_scroll(Locator.CHECKBOX3, timeout=3)
        self.scroll_to_end(1)
        return self

    @allure.step('Выбрать чекбокс "Checkbox 3" для опции "Checkbox"')
    def click_checkbox4(self):
        self.logger.info(f'[{self.class_name}] Выбрать чекбокс "Checkbox 3" для опции "Checkbox"')
        self.get_element(Locator.CHECKBOX4, timeout=1).click()
        return self

    @allure.step('Заполнить поле "Text" значением "Текст"')
    def enter_text_text(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Text" значением "Текст"')
        element = self.get_element(Locator.TEXT_INPUT, timeout=1)
        element.clear()
        element.send_keys('Текст')
        return self

    @allure.step('Нажать в поле "Select"')
    def click_select_available_options_dropdown(self):
        self.logger.info(f'[{self.class_name}] Нажать в поле "Select"')
        self.get_element(Locator.SELECT_AVAILABLE_OPTIONS_DROPDOWN, timeout=1).click()
        return self

    @allure.step('В выпавшем списке выбрать "Yellow"')
    def click_yellow_available_options(self):
        self.logger.info(f'[{self.class_name}] В выпавшем списке выбрать "Yellow"')
        self.get_element(Locator.YELLOW_AVAILABLE_OPTIONS, timeout=1).click()
        return self

    @allure.step('Заполнить поле "Textarea" значением "Текст"')
    def enter_textarea_available_options(self):
        self.logger.info(f'[{self.class_name}] Заполнить поле "Textarea" значением "Текст"')
        element = self.get_element(Locator.TEXTAREA_AVAILABLE_OPTIONS, timeout=1)
        element.clear()
        element.send_keys('Текст')
        return self

    @allure.step('В поле "File" вставить пустой файл формата txt')
    def upload_file(self):
        self.logger.info(f'[{self.class_name}] ')
        self.get_element(Locator.BUTTON_UPLOAD_FILE, timeout=5).click()
        #Не работает без слипа
        time.sleep(1)
        pyautogui.press('esc')
        file_input = self.presence_of_element_located(Locator.INPUT_TYPE_FILE,timeout=5)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'requirements.txt'))
        file_input.send_keys(file_path)
        self.allert()
        return self

    @allure.step('Поля дат и времени заполнить любым значением')
    def enter_date_time(self):
        self.logger.info(f'[{self.class_name}] Поля дат и времени заполнить любым значением')
        date_text = '2025-05-11'
        time_text = '14:25'
        date = self.get_element(Locator.DATE_INPUT, timeout=1)
        date.clear()
        date.send_keys(date_text)
        time_input = self.get_element(Locator.TIME_INPUT, timeout=1)
        time_input.clear()
        time_input.send_keys(time_text)
        dateandtime = self.get_element(Locator.DATEANDTIME_INPUT, timeout=1)
        dateandtime.clear()
        dateandtime.send_keys(f"{date_text} {time_text}")
        return self

    @allure.step('Нажать кнопку корзины справа от поля поиска')
    def click_cart_div(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку корзины справа от поля поиска')
        self.get_element(Locator.CART_DIV, timeout=3).click()
        return self

    @allure.step('В форме нажать "Checkout"')
    def click_cart_checkout(self):
        self.logger.info(f'[{self.class_name}] В форме нажать "Checkout"')
        self.get_element(Locator.CART_CHECKOUT, timeout=3).click()
        return self
