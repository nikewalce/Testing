from pages.base_page import BasePage
from pages.locators.account_wishlist_page_locators import AccountWishlistPageLocators as Locator
import allure

class AccountWishlistPage(BasePage):
    @allure.step('Нажать кнопку "Add to Cart" товара "Apple Cinema 30"')
    def click_add_to_cart_apple_button(self):
        self.logger.info(f'[{self.class_name}] Нажать кнопку "Add to Cart" товара "Apple Cinema 30"')
        self.get_element(Locator.ADD_TO_CART_APPLE_BUTTON, timeout=1).click()
        return self
