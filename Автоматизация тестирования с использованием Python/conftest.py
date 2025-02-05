import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get("https://effective-mobile.ru/")
    yield driver
    driver.quit()
