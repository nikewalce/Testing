from selenium.webdriver.common.by import By

class CheckoutSuccessPageLocators:
    MY_ACCOUNT_LINK = (By.XPATH, "//a[@title='My Account']")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[text()='Order History']")
