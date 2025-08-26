import os
import datetime
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import pytest
import testit
from decouple import config
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService


from src.ui.pom.core.base_manager import BaseManager
from src.ui.pom.pages.base_element.locators import base_element_locators

load_dotenv()

# ================= PYTEST CONFIG =================

def pytest_configure(config):
    # Базовый каталог для feature-файлов
    config.option.bdd_features_base_dir = "tests/features"

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--ui_url", action="store", default=config("PORTAL_URL"))
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser_version", action="store", default="138")
    parser.addoption("--selenoid_server", action="store", default="0.0.0.0")
    parser.addoption("--run_local", action="store_true", default=True)
    parser.addoption("--browser_log", action="store_true", default=False)
    #parser.addoption("--uid", action="store", default=config("UID"))
    parser.addoption("--log", action="store", default=True)
    parser.addoption("--log_level", action="store", default="INFO")

# ================= LOGGER =================

def setup_logger():
    log = config("LOGGING", default=True, cast=bool)
    log_level = config("LOG_LEVEL", default="INFO").upper()

    logger = logging.getLogger("pytest_logger")
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log:
        logs_path = Path(__file__).resolve().parent / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        log_file = logs_path / "test_session.log"

        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 100, backupCount=5, mode="w", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger.disabled = True

    return logger

# ================= BROWSER FIXTURE =================

@pytest.fixture(scope="function")
def browser(request) -> WebDriver:
    logger = setup_logger()
    request.node._logger = logger

    driver = create_browser(request.config)
    driver.logger = logger
    driver.maximize_window()

    base_url = request.config.getoption("--ui_url")
    driver.get(base_url)
    logger.info(f"==> Opened URL: {base_url}")

    yield driver

    if request.config.getoption("--browser_log"):
        logs = driver.get_log("browser")
        for log in logs:
            logger.info(f"[{log['level']}] {log['timestamp']}: {log['message']}")

    driver.quit()
    logger.info("==> Browser session closed.")

def create_browser(config) -> WebDriver:
    browser_name = config.getoption("--browser")
    browser_version = config.getoption("--browser_version")
    selenoid_server = config.getoption("--selenoid_server")
    run_local = config.getoption("--run_local")
    #headless = config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        download_dir = os.path.join(os.getcwd(), "upload")
        os.makedirs(download_dir, exist_ok=True)

        options.add_argument("--allow-running-insecure-content")
        options.add_argument(
            f"--unsafely-treat-insecure-origin-as-secure={config.getoption('--ui_url')}"
        )
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
    else:
        raise ValueError(
            "Unsupported browser name. Use 'chrome', 'firefox' or 'edge'."
        )

    capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "timeZone": "Europe/Samara",
        },
    }

    for key, value in capabilities.items():
        options.set_capability(key, value)

    if run_local:
        if browser_name == "chrome":
            options = ChromeOptions()
            # if headless:
            #     options.add_argument(argument="headless=new")
            driver = webdriver.Chrome(options=options, service=ChromiumService())
        elif browser_name == "firefox":
            options = FFOptions()
            # if headless:
            #     options.add_argument(argument="headless=new")
            driver = webdriver.Firefox(options=options, service=FFService())
        elif browser_name == "edge":
            options = EdgeOptions()
            # if headless:
            #     options.add_argument(argument="headless=new")
            driver = webdriver.Edge(options=options, service=EdgeService())
        elif browser_name == "yandex":
            options = webdriver.ChromeOptions()
            # if headless:
            #     options.add_argument(argument="headless=new")
            binary_yandex_driver_file = '../yandexdriver.exe'
            service = ChromiumService(binary_yandex_driver_file)
            driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = WebDriver(command_executor=selenoid_server, options=options)
    return driver

# ================= TEST CONTEXT =================

@pytest.fixture
def test_context():
    return {
        "saved_data": {},
        "filled_data": {},
        "new_count": 0,
        "read_count": 0,
        "rows": {},
        "save_comment": {},
        "subdivisions": {},
        "comment": {},
        "field":{},
    }

# ================= SCREENSHOT =================

def attach_screenshot_to_testit(browser):
    process_id = os.getpid()
    screenshot_path = f"screenshots/failure_screenshot_{process_id}.png"
    browser.get_screenshot_as_file(screenshot_path)
    testit.addAttachments(screenshot_path)
    os.remove(screenshot_path)

# ================= PYTEST-BDD HOOKS =================

@pytest.hookimpl(hookwrapper=True)
def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    browser = request.getfixturevalue("browser")
    timeout = config("TIMEOUT_LOADING_ANIMATION", default=5)
    base_page = BaseManager(browser)

    try:
        base_page.check.elements.verify_visible(
            base_element_locators.HEXAGON_LOADING_ANIMATION, timeout=timeout, reverse=True
        )
        base_page.check.elements.verify_visible(
            base_element_locators.LINE_LOADING_ANIMATION, timeout=timeout, reverse=True
        )
        base_page.helpers.wait_for_js_to_load(timeout=timeout)

        base_page.check.elements.verify_visible(
            base_element_locators.CIRCULAR_LOADING_ANIMATION, timeout=15, reverse=True
        )
        base_page.check.elements.verify_visible(
            base_element_locators.BUTTON_LOADING_ANIMATION, timeout=15, reverse=True
        )
    except Exception as e:
        attach_screenshot_to_testit(browser)
        raise e
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    outcome = yield
    rep_list = outcome.get_result()
    if isinstance(rep_list, list):
        rep_call = next((rep for rep in rep_list if rep.when == "call"), None)
    else:
        rep_call = rep_list if getattr(rep_list, "when", None) == "call" else None

    if rep_call and rep_call.failed:
        browser = request.getfixturevalue("browser")
        attach_screenshot_to_testit(browser)

@pytest.hookimpl()
def pytest_sessionstart(session):
    logger = setup_logger()
    logger.info(f"==> Test session started at {datetime.datetime.now()}")

@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    logger = setup_logger()
    logger.info(f"==> Test session finished at {datetime.datetime.now()}")
