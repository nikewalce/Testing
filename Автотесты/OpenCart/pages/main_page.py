from pages.base_page import BasePage
from pages.locators.main_page_locators import MainPageLocators as Locator
import allure

class MainPage(BasePage):
    @allure.step('В панели с категорией товаров нажать "Cameras"')
    def click_cameras_button(self):
        self.logger.info(f"[{self.class_name}] В панели с категорией товаров нажать 'Cameras'")
        self.get_element(Locator.CAMERAS_BUTTON, timeout=1).click()
        return self

    @allure.step('В верхней навигационной панели нажать "My account"')
    def click_my_account_button(self):
        self.logger.info(f'[{self.class_name}] 	В верхней навигационной панели нажать "My account"')
        self.get_element(Locator.MY_ACCOUNT_BUTTON, timeout=1).click()
        return self

    @allure.step('Выбрать "Login"')
    def click_link_login(self):
        self.logger.info(f'[{self.class_name}] Выбрать "Login"')
        self.get_element(Locator.LINK_LOGIN, timeout=1).click()
        return self

    @allure.step('В панели с категорией товаров навести мышкой на "Components"')
    def components_mouseover(self):
        self.logger.info(f'[{self.class_name}] В панели с категорией товаров навести мышкой на "Components"')
        self.mouseover(Locator.COMPONENTS_LINK, timeout=1)
        return self

    @allure.step('В выпавшем списке нажать "Monitors"')
    def click_monitors_link(self):
        self.logger.info(f'[{self.class_name}] В выпавшем списке нажать "Monitors"')
        self.get_element(Locator.MONITOR_LINK, timeout=1).click()
        return self
