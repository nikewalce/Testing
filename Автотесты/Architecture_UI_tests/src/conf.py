from decouple import config
from dotenv import load_dotenv
import testit_api_client

load_dotenv()


class Settings:
    """
    Управление настройками проекта.
    """

    # Настройки запуска
    RUN_LOCAL = config("RUN_LOCAL", default="True")

    # Браузер
    BROWSER_NAME = config("BROWSER_NAME", default="chrome")
    BROWSER_VERSION = config("BROWSER_VERSION", default="139.0")

    PORTAL_URL = config("PORTAL_URL", default="chrome")

    # Логирование
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")
    LOG_FORMAT = config(
        "LOG_FORMAT", default="%(asctime)s - %(levelname)s - %(message)s"
    )
    LOG_MAX_SIZE = config("LOG_MAX_SIZE", default=1024 * 1024 * 10)  # 10 МБ
    LOG_BACKUP_COUNT = config("LOG_BACKUP_COUNT", default=5)
    LOG_DIR = config("LOG_DIR", default="logs")

    # База данных
    DB = config("DB", default="postgresql")
    DB_NAME = config("DB_NAME", default="postgres")
    DB_USER = config("DB_USER", default="user")
    DB_PASS = config("DB_PASS", default="password")
    DB_HOST = config("DB_HOST", default="localhost")
    DB_PORT = config("DB_PORT", default="5432")

    # API
    API_URL = config("API_URL", default="http://localhost:8000")

    # Faker
    FAKE_LANGUAGE = config("FAKE_LANGUAGE", default="ru_RU")

    # Учетные данные пользователей
    CREDENTIALS = {
        "DOMAIN": {
            "login": config("DOMAIN_LOGIN", default="domain_login"),
            "password": config("DOMAIN_PASSWORD", default="domain_password"),
            "type": "DOMAIN",
        },
        "TECHNICAL": {
            "login": config("TECHNICAL_LOGIN", default="technical_login"),
            "password": config(
                "TECHNICAL_PASSWORD", default="technical_password"
            ),
            "type": "TECHNICAL",
        },
        "UNKNOWN": {
            "login": config("UNKNOWN_LOGIN", default="fake"),
            "password": config("UNKNOWN_PASSWORD", default="fake_password"),
            "type": "UNKNOWN",
        },
    }

    # SuperUser
    ADMIN_CREDENTIALS = {
        "login": config("ADMIN_LOGIN", default=""),
        "password": config("ADMIN_PASSWORD", default=""),
        "type": "DOMAIN",
    }

    # TestIt
    USE_TEST_IT = config("USE_TEST_IT", default=False, cast=bool)
    TEST_IT_PROJECT_ID = config("TEST_IT_PROJECT_ID")
    TEST_IT_TOKEN = config("TEST_IT_TOKEN")
    TEST_IT_URL = config("TEST_IT_URL")
    TEST_IT_MAIN_SECTION_ID = config("TEST_IT_MAIN_SECTION_ID")
    TEST_IT_ANY_CONFIGURATION = config("TEST_IT_ANY_CONFIGURATION")
    testrun_id = config("TEST_IT_TESTRUN_ID", "")

    configuration = testit_api_client.Configuration(host=TEST_IT_URL)
    configuration.api_key["Bearer or PrivateToken"] = TEST_IT_TOKEN
    configuration.api_key_prefix["Bearer or PrivateToken"] = "PrivateToken"

    TELEGRAM_TELEBOT_TOKEN = config("TELEGRAM_TELEBOT_TOKEN")
    TELEGRAM_CONNECTED_CHAT = config("TELEGRAM_CONNECTED_CHAT")


settings = Settings()
