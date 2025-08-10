from selenium.webdriver.common.by import By

class CatalogPageLocators:
    ADD_TO_CART_CanonEOS5D_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(), 'Canon EOS 5D')]]//button[@type='button']")
    COMPARE_HTC_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'HTC Touch HD')]]//button[@data-original-title='Compare this Product']")
    COMPARE_IPHONE_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'iPhone')]]//button[@data-original-title='Compare this Product']")
    COMPARE_PALM_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'Palm Treo Pro')]]//button[@data-original-title='Compare this Product']")
    SEARCH_INPUT = (By.XPATH, "//input[@name='search']")
    SEARCH_SPAN = (By.XPATH, "//span[@class='input-group-btn']")
    ADD_TO_WISH_LIST_APPLE_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'Apple Cinema 30')]]//button[@data-original-title='Add to Wish List']")
    ADD_TO_WISH_LIST_SAMSUNG_BUTTON = (By.XPATH, "//div[@class='product-thumb'][.//a[contains(text(),'Samsung SyncMaster 941BW')]]//button[@data-original-title='Add to Wish List']")
    WISH_LIST_LINK = (By.XPATH, "//a[contains(text(), 'Wish List')]")
    NAV_TOP = (By.XPATH, "//nav[@id='top']")
