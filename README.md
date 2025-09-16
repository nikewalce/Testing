Здесь хранятся мои учебные тестовые проекты по тестированию  
Васильев Д.А.  
Автоматизация: https://github.com/nikewalce/ITFB_hw/tree/main/hw_9  

# Как бы провел автоматизацию валидации имейла (кейса)?

#Определение требований и правил валидации  

Прежде чем писать тесты, нужно понять, какие требования предъявляются к email. Обычно email должен:  
- Содержать "@" и "."  
- Иметь корректную структуру (username@domain.com)  
- Не содержать запрещенные символы (например, пробелы, кириллицу)  
- Не быть слишком коротким (a@b.c — невалидно)  
- Не быть слишком длинным (например, > 320 символов)  
- Соответствовать формату регулярного выражения (RFC 5322)  
- Пример регулярного выражения для валидации email:  
```^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$```

#Написание автоматических тестов  
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

# Проверка на сервере (API-тестирование)
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

# Интеграция тестов в CI/CD  
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
