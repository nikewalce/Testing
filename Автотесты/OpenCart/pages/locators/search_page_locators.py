from selenium.webdriver.common.by import By

class SearchPageLocators:
    COMPARE_SAMSUNG_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'Samsung Galaxy Tab 10.1')]]//button[@data-original-title='Compare this Product']")
    COMPARE_TOTAL_LINK = (By.XPATH, "//a[@id='compare-total']")
