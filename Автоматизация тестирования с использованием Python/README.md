Задача: Написать тесты на главную страницу сайта effective-mobile.ru, проверяющие переход по всем блокам по клику (О нас, Контакты и пр.). Проверять нужно соответствующие локаторы и url’ы.
Для тестирования используется Selenium и Pytest, для генерации подробных отчетов о прохождении тестов используется Allure 

1. Установка зависимостей

pip install -r requirements.txt

4. Установка Allure

Windows

Скачайте Allure.zip с [GitHub Releases](https://github.com/allure-framework/allure2/releases) и распакуйте.

Добавьте путь к папке bin в переменную окружения PATH (например, C:\allure\bin).
Скачайте Java и добавьте путь к системной переменной JAVA_HOME (например, C:\Program Files (x86)\Java\jre1.8.0_441)

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
