from pages.base_page import BasePage
from pages.locators.compare_product_locators import CompareProductLocators as Locator
import allure

class CompareProductPage(BasePage):
    @allure.step('Нажать кнопку "Remove" под товаром "HTC Touch HD"')
    def click_remove_htc_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Remove" под товаром "HTC Touch HD"')
        self.scroll_to_end(2)
        self.get_element(Locator.REMOVE_HTC_BUTTON, timeout=5).click()
        return self

    @allure.step('Нажать кнопку "Add to Cart" под товаром "iPhone"')
    def click_add_to_cart_iphone(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Add to Cart" под товаром "iPhone"')
        self.get_element(Locator.ADD_TO_CART_IPHONE_BUTTON, timeout=5).click()
        self.scroll_to_end(2)
        return self

    @allure.step('Нажать кнопку "Add to Cart" под товаром "Palm Treo Pro"')
    def click_add_to_cart_palm(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Add to Cart" под товаром "Palm Treo Pro"')
        self.scroll_to_end(2)
        self.get_element(Locator.ADD_TO_CART_PALM_BUTTON, timeout=5).click()
        return self

    @allure.step('В верхней навигационной панели нажать "Shopping Cart"')
    def click_shopping_cart_link(self):
        self.logger.info(f'[{self.class_name}] В верхней навигационной панели нажать "Shopping Cart"')
        self.scroll_to_top(2)
        self.get_element(Locator.SHOPPING_CART_LINK, timeout=5).click()
        return self
