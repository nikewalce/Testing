from selenium.webdriver.common.by import By

class CompareProductLocators:
    REMOVE_HTC_BUTTON = (By.XPATH, "//a[contains(@href, 'remove=28')]")
    ADD_TO_CART_IPHONE_BUTTON = (By.XPATH, "//input[contains(@onclick, \"cart.add('40', '1');\")]")
    ADD_TO_CART_PALM_BUTTON = (By.XPATH, "//input[contains(@onclick, \"cart.add('29', '1');\")]")
    SHOPPING_CART_LINK = (By.XPATH, "//a[@title='Shopping Cart']")
