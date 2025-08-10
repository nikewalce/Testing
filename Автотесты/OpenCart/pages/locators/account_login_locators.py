from selenium.webdriver.common.by import By

class AccountLoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@id='input-email']")
    INPUT_PASSWORD = (By.XPATH, "//input[@id='input-password']")
    LOGIN_INPUT = (By.XPATH, "//input[@value='Login']")
