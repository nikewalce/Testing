from pages.base_page import BasePage
from pages.locators.catalog_page_locators import CatalogPageLocators as Locator
import allure

class CatalogPage(BasePage):
    @allure.step('На карточке товара "Canon EOS 5D" нажать "Add to Cart"(иконка корзины)')
    def click_add_to_cart_canon_e0s5d_button(self):
        self.logger.info(f'[{self.class_name}] На карточке товара "Canon EOS 5D" нажать "Add to Cart"(иконка корзины)')
        self.scroll_to_end(5)
        self.get_element(Locator.ADD_TO_CART_CanonEOS5D_BUTTON, timeout=1).click()
        return self

    @allure.step('На карточке товара "HTC Touch HD" нажать "Compare this Product"(добавить к сравнению)')
    def click_compare_htc_button(self):
        self.logger.info(f'[{self.class_name}] На карточке товара "HTC Touch HD" нажать "Compare this Product"(добавить к сравнению)')
        self.get_element(Locator.COMPARE_HTC_BUTTON, timeout=5).click()
        self.scroll_to_end(3)
        return self

    @allure.step('На карточке товара "iPhone" нажать "Compare this Product"(добавить к сравнению)')
    def click_compare_iphone_button(self):
        self.logger.info(f'[{self.class_name}] На карточке товара "iPhone" нажать "Compare this Product"(добавить к сравнению)')
        self.get_element(Locator.COMPARE_IPHONE_BUTTON, timeout=10).click()
        self.scroll_to_end(3)
        return self

    @allure.step('На карточке товара "Palm Treo Pro" нажать "Compare this Product"(добавить к сравнению)')
    def click_compare_palm_button(self):
        self.logger.info(f'[{self.class_name}] На карточке товара "Palm Treo Pro" нажать "Compare this Product"(добавить к сравнению)')
        self.get_element(Locator.COMPARE_PALM_BUTTON, timeout=10).click()
        return self

    @allure.step('В поисковой строке вверху страницы ввести в поисковую строку "Samsung"')
    def enter_string_in_search(self):
        self.logger.info(f'[{self.class_name}] В поисковой строке вверху страницы ввести в поисковую строку "Samsung"')
        element = self.get_element(Locator.SEARCH_INPUT, timeout=1)
        element.clear()
        element.send_keys("Samsung")
        return self

    @allure.step('Нажать кнопку поиск')
    def click_search_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку поиск]')
        self.get_element(Locator.SEARCH_SPAN, timeout=1).click()
        return self

    @allure.step('Нажать кнопку "Add to Wish List" под товаром "Apple Cinema 30')
    def click_add_to_wish_list_apple(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Add to Wish List" под товаром "Apple Cinema 30')
        self.get_element(Locator.ADD_TO_WISH_LIST_APPLE_BUTTON, timeout=1).click()
        self.scroll_to_end(3)
        return self

    @allure.step('Нажать кнопку "Add to Wish List" под товаром "Samsung SyncMaster 941BW')
    def click_add_to_wish_list_samsung(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Add to Wish List" под товаром "Samsung SyncMaster 941BW')
        self.scroll_to_end(3)
        self.get_element(Locator.ADD_TO_WISH_LIST_SAMSUNG_BUTTON, timeout=1).click()
        return self

    @allure.step('В верхней навигационной панели нажать "Wish List"')
    def click_wish_list(self):
        self.logger.info(f'[{self.class_name}] В верхней навигационной панели нажать "Wish List"')
        self.scroll_to_top(3)
        self.get_element(Locator.WISH_LIST_LINK, timeout=1).click()
        return self
