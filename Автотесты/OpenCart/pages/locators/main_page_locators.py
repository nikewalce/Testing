from selenium.webdriver.common.by import By

class MainPageLocators:
    CAMERAS_BUTTON = (By.XPATH, "//a[text()='Cameras']")
    MY_ACCOUNT_BUTTON = (By.XPATH, "//a[@title='My Account' and @class='dropdown-toggle']")
    LINK_LOGIN = (By.XPATH, "//a[text()='Login']")
    COMPONENTS_LINK = (By.XPATH, "//a[contains(text(), 'Components')]")
    MONITOR_LINK = (By.XPATH, "//a[contains(text(), 'Monitors')]")
