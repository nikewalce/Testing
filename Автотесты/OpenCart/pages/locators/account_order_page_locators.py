from selenium.webdriver.common.by import By

class AccountOrderPageLocators:
    ORDER_CUSTOMER_NAME = (By.XPATH, "//tr/td[2]")
    VIEW_LINK = (By.XPATH, "//a[@data-original-title='View']")
    IPHONE_TD = (By.XPATH, "//td[contains(text(), 'iPhone')]")
    ADDDRESS_INFO = (By.XPATH, "//table[@class='table table-bordered table-hover']//td[text()='Payment Address']/ancestor::table")
    RETURN_LINK = (By.XPATH, "//a[@data-original-title='Return']")
    INPUT_TELEPHONE = (By.XPATH, "//input[@id='input-telephone']")
    REASON_FOR_RETURN_CHECKBOX = (By.XPATH, "//input[@name='return_reason_id']")
    SUBMIT_RETURN_BUTTON = (By.XPATH, "//input[@value='Submit']")
