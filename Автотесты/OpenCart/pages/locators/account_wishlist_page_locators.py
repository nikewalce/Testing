from selenium.webdriver.common.by import By

class AccountWishlistPageLocators:
    ADD_TO_CART_APPLE_BUTTON = (By.XPATH, "//button[contains(@onclick, \"cart.add('42')\") and contains(@class, 'btn-primary')]")
