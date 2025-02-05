Задача: Написать тесты на главную страницу сайта effective-mobile.ru, проверяющие переход по всем блокам по клику (О нас, Контакты и пр.). Проверять нужно соответствующие локаторы и url’ы.
Для тестирования используется Selenium и Pytest, для генерации подробных отчетов о прохождении тестов используется Allure 

Требования

- Python 3.10
- Google Chrome и ChromeDriver (должен совпадать с версией Chrome)

Установка и запуск проекта

1. Клонирование репозитория

git clone https://github.com/nikewalce/Testing/tree/main/%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D1%81%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC%20Python
cd project_root

2. Создание виртуального окружения

python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate    # Для Windows

3. Установка зависимостей

pip install -r requirements.txt

4. Установка Allure

Windows

Скачайте Allure с GitHub Releases и распакуйте.

Добавьте путь к папке bin в переменную окружения PATH (например, C:\allure\bin).

macOS/Linux

brew install allure

5. Проверка установки Allure

allure --version

6. Запуск тестов

pytest --alluredir=allure-results

7. Генерация и просмотр отчета Allure

allure serve allure-results

Пример успешного вывода команды

pytest --alluredir=allure-results
============================= test session starts =============================
collected 5 items

tests/test_links.py .....                                           [100%]
============================== 5 passed in 3.45s ==============================
