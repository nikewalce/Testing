Здесь хранятся мои учебные тестовые проекты по тестированию  
Васильев Д.А.  
Автоматизация: https://github.com/nikewalce/ITFB_hw/tree/main/hw_9  

#Какие знаешь статус коды?

Статусные коды HTTP представляют собой стандартизированные индикаторы, отправляемые сервером в ответ на запросы клиента, чтобы указать на результат обработки запроса. Они помогают определить, был ли запрос успешным, произошла ли ошибка и какого рода действия требуется предпринять дальше. Они разделены на пять классов:

## 🚩1xx: Информационные

- 100 Continue
Промежуточный ответ, указывающий, что начальная часть запроса принята и клиент может продолжать отправку данных.
- 101 Switching Protocols
Сервер соглашается переключить протоколы в соответствии с запросом клиента, отправленным в заголовке Upgrade.


## 🚩2xx: Успешные

- 200 OK
Стандартный ответ для успешных HTTP-запросов. Ресурс успешно обработан и передан в теле ответа.
- 201 Created
Запрос был успешно выполнен, и в результате был создан новый ресурс.
- 204 No Content
Запрос успешно обработан, но в ответе нет содержимого.


## 🚩3xx: Перенаправления

- 301 Moved Permanently
Запрашиваемый ресурс был окончательно перемещен на URL, указанный в заголовке Location. Клиент должен использовать этот новый URL в будущем.
- 302 Found
Запрашиваемый ресурс временно находится по другому URI, указанному в заголовке Location.
- 304 Not Modified
Ресурс не был изменен с момента последнего запроса клиента, использующего условные заголовки типа If-Modified-Since или If-None-Match.


## 🚩4xx: Ошибки клиента

- 400 Bad Request
Сервер не может обработать запрос из-за неверного синтаксиса.
- 401 Unauthorized
Для доступа к запрашиваемому ресурсу требуется аутентификация.
- 403 Forbidden
Сервер понял запрос, но отказывается его авторизовать.
- 404 Not Found
Запрашиваемый ресурс не найден на сервере.
- 405 Method Not Allowed
Метод, указанный в запросе, не поддерживается для данного ресурса.


## 🚩5xx: Ошибки сервера

- 500 Internal Server Error
Общая ошибка сервера, когда сервер сталкивается с непредвиденными обстоятельствами.
- 501 Not Implemented
Сервер не поддерживает функциональные возможности, необходимые для обработки запроса.
- 502 Bad Gateway
Сервер, выступая в роли шлюза или прокси, получил неверный ответ от вышестоящего сервера.
- 503 Service Unavailable
Сервер временно не может обработать запрос из-за перегрузки или технического обслуживания.
- 504 Gateway Timeout
Шлюз или прокси-сервер не получил вовремя ответ от вышестоящего сервера для завершения запроса.


# Как бы провел автоматизацию валидации имейла (кейса)?

## Определение требований и правил валидации  

Прежде чем писать тесты, нужно понять, какие требования предъявляются к email. Обычно email должен:  
- Содержать "@" и "."  
- Иметь корректную структуру (username@domain.com)  
- Не содержать запрещенные символы (например, пробелы, кириллицу)  
- Не быть слишком коротким (a@b.c — невалидно)  
- Не быть слишком длинным (например, > 320 символов)  
- Соответствовать формату регулярного выражения (RFC 5322)  
- Пример регулярного выражения для валидации email:  
```^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$```

## Написание автоматических тестов  
```
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://example.com/signup")  # Открываем страницу регистрации
    yield driver
    driver.quit()

@pytest.mark.parametrize("email, expected", [
    ("valid.email@example.com", True),    # Валидный email
    ("invalid-email.com", False),         # Нет "@"
    ("@nodomain.com", False),             # Нет имени
    ("user@.com", False),                 # Нет домена
    ("user@domain..com", False),          # Двойная точка
    ("user@domain.c", False),             # Слишком короткое доменное расширение
])
def test_email_validation(driver, email, expected):
    email_input = driver.find_element(By.NAME, "email")
    submit_button = driver.find_element(By.NAME, "submit")

    email_input.clear()
    email_input.send_keys(email)
    submit_button.click()

    error_message = driver.find_element(By.ID, "email-error")

    if expected:
        assert error_message.is_displayed() is False, f"Ошибка для валидного email: {email}"
    else:
        assert error_message.is_displayed() is True, f"Нет ошибки для невалидного email: {email}"
```

## Проверка на сервере (API-тестирование)
Помимо UI, нужно проверять валидацию на сервере через API-запросы.  
Пример API-теста с Postman + Newman или RestAssured в Java  
```
import pytest
import requests

BASE_URL = "https://example.com/api/register"

@pytest.mark.parametrize("email, expected_status", [
    ("valid.email@example.com", 200),  
    ("invalid-email.com", 400),        
    ("user@.com", 400),               
])
def test_email_validation_api(email, expected_status):
    response = requests.post(BASE_URL, json={"email": email})
    assert response.status_code == expected_status
```

## Интеграция тестов в CI/CD  
Чтобы автоматические тесты запускались регулярно, их можно интегрировать в Jenkins, GitHub Actions, GitLab CI.
```
name: Run Email Validation Tests

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```
