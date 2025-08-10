from pages.base_page import BasePage
from pages.locators.search_page_locators import SearchPageLocators as Locator
import allure

class SearchPage(BasePage):
    @allure.step('На карточке товара "Samsung Galaxy Tab 10.1" нажать "Compare this Product"(добавить к сравнению)')
    def click_samsung_compare(self):
        self.logger.info(f'[{self.class_name}] На карточке товара "Samsung Galaxy Tab 10.1" нажать "Compare this Product"(добавить к сравнению)')
        self.get_element(Locator.COMPARE_SAMSUNG_BUTTON, timeout=1).click()
        return self

    @allure.step('Над карточками товаров нажать "Product Compare"')
    def click_total_compare_link(self):
        self.logger.info(f'[{self.class_name}] Над карточками товаров нажать "Product Compare"]')
        self.get_element(Locator.COMPARE_TOTAL_LINK, timeout=1).click()
        return self
