import pytest
from config import Config
from tests.api.models import Token
import requests
from tests.sql_queries.sql_config_api import CartDB
import logging

@pytest.fixture(scope="session")
def db():
    """Фикстура для инициализации подключения к базе данных."""
    db_instance = CartDB()
    return db_instance

@pytest.fixture(scope="function")
def logger(request):
    logger = logging.getLogger(request.node.name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        # Запись в файл
        file_handler = logging.FileHandler("diplom.log", mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        # Формат логов
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    yield logger
    # Удаление хендлеров после завершения теста, чтобы не дублировались логи
    for h in logger.handlers[:]:
        logger.removeHandler(h)

def pytest_addoption(parser):
    parser.addoption(
        "--cart",
        action="store",
        default="http://localhost/index.php?route=api",
        help="OpenCart api"
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--cart")

@pytest.fixture(scope="session")
def login_data():
    config = Config()
    login_data = {
        'username': config.token_username,
        'key': config.token_key,
    }
    return login_data

@pytest.fixture(scope="session")
def api_token(base_url, login_data, db):
    """Фикстура для получения и проверки токена."""
    login_response = requests.post(f"{base_url}/login", data=login_data)
    assert login_response.status_code == 200, "Ошибка авторизации"
    validated_token = Token(**login_response.json())
    assert isinstance(validated_token.api_token, str), "Токен не строка"
    yield validated_token.api_token
    #Чистим за собой
    db.delete_cart_by_api_id(2)
    db.delete_session_by_session_id(validated_token.api_token)
    db.delete_oc_session_by_session_id(validated_token.api_token)
