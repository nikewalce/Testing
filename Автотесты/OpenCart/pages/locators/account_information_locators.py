from selenium.webdriver.common.by import By

class AccountInformationLocators:
    INPUT_FIRSTNAME = (By.XPATH, "//input[@id='input-firstname']")
    INPUT_LASTNAME = (By.XPATH, "//input[@id='input-lastname']")
    INPUT_EMAIL = (By.XPATH, "//input[@id='input-email']")
    INPUT_TELEPHONE = (By.XPATH, "//input[@id='input-telephone']")
