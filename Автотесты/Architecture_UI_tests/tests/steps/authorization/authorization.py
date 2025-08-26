import pytest
from pytest_bdd import given, when, then, parsers
import datetime
from src.ui.pom.pages.authorization.authorization import AuthorizationPage
from src.ui.pom.pages.main.main_page import MainPage
from src.ui.pom.pages.main.check import CheckMainPage
from src.ui.pom.pages.user_actions.user_actions import UserActionsPage
from src.ui.locators.authorization import login_page_locators as locator

@pytest.fixture
def authorization_page(browser):
    return AuthorizationPage(browser)

@pytest.fixture
def main_page(browser):
    return MainPage(browser)

@pytest.fixture
def user_actions_page(browser):
    return UserActionsPage(browser)

@given("Учетная запись пользователя добавлена в систему")
def user_account_created_in_system():
    pass

@given("Пользователь получил ссылку для сброса пароля на электронную почту")
def user_received_password_reset_link(authorization_page):
    assert authorization_page.get_reset_password_link() is not None, "Ссылка для сброса пароля не была получена"

@given("Пользователь перешел по ссылке и задал пароль")
def user_followed_link_and_set_password(authorization_page):
    # url = authorization_page.get_reset_password_link()
    # authorization_page.set_password(url)
    pass

@given('Пользователь находится на странице входа')
def open_login_page(authorization_page):
    authorization_page.open_auth_page()
    authorization_page.check_open()

@given('Авторизоваться в системе под валидной УЗ')
def auth_valid_account(authorization_page):
    authorization_page.check_open()
    authorization_page.login()

@when('Пользователь вводит логин и пароль')
def enter_credentials(authorization_page):
    authorization_page.entering_field(value="существующий", field="логин")
    authorization_page.entering_field(value="валидный", field="пароль")

@when(parsers.parse('Пользователь вводит некорректный логин: "{login}" и/или пароль: "{password}"'))
def enter_not_valid_credentials(authorization_page, login, password):
    authorization_page.entering_field(value=login, field="логин")
    authorization_page.entering_field(value=password, field="пароль")

@when(parsers.parse('Пользователь не вводит логин: "{login}" и/или пароль: "{password}"'))
def not_enter_credentials(authorization_page, login, password):
    authorization_page.entering_field(value=login, field="логин")
    authorization_page.entering_field(value=password, field="пароль")

@when('Пользователь нажимает кнопку "Войти"')
def click_login(authorization_page):
    authorization_page.interactions.click_on(locator.LOGIN_BUTTON)

@when('Пользователь нажимает кнопку "Выход из системы"')
def click_logout(main_page):
    main_page.click_logout()

@when('Пользователь нажимает кнопку "Назад" в браузере')
def click_back_button(authorization_page):
    authorization_page.click_back_button()

@when('Пользователь обновляет страницу или переходит на защищённый раздел по прямой ссылке')
def refresh_page(authorization_page):
    authorization_page.refresh_page()
    assert authorization_page.go_to_page() == False

@then('Отображаются поля логина и пароля, кнопки "Войти" и "Войти с помощью ADFS"')
def check_login_elements_displayed(authorization_page):
    (authorization_page
     .check_login_field()
     .check_password_field()
     .check_login_button()
     .check_login_ADFS_button())

@then('Поля логина и пароля заполнены')
def check_fields_filled_correctly(authorization_page):
    authorization_page.get_field_value("логин")
    authorization_page.get_field_value("пароль")

@then(parsers.parse('Поля логина: "{login}" и/или пароля "{password}" остаются пустыми'))
def check_fields_is_empty(authorization_page, login, password):
    authorization_page.check_empty_fields(login, password)

@then('Система отображает сообщение об ошибке: "Неверный логин или пароль. Повторите попытку"')
def check_login_error_message(authorization_page):
    authorization_page.error_message()

@then('Система отображает сообщение об ошибке: "Заполните поле"')
def check_error_message_empty_field(authorization_page):
    authorization_page.error_message_empty_field()

@then('Поля логина и пароля подсвечиваются как некорректные')
def check_fields_invalid_highlight(authorization_page):
    authorization_page.is_field_invalid("логин")
    authorization_page.is_field_invalid("пароль")

@then(parsers.parse('Система подсвечивает незаполненные поля "{login}" или "{password}"'))
def check_empty_fields_highlight(authorization_page, login, password):
    authorization_page.is_field_empty("логин", login)
    authorization_page.is_field_empty("пароль", password)

@then('Система проверяет учетные данные, статус учетной записи и полномочия')
def check_account_data(browser):
    pass

@then('Пользователь перенаправляется на Главную страницу')
@then('Отображается Главная страница')
def check_homepage_loaded(main_page):
    main_page.check_open()

@then('Пользователь перенаправляется на страницу авторизации')
@then('Пользователь остаётся на странице входа')
@then('Cтраница не загружается, и система перенаправляет на страницу авторизации')
def check_authpage_loaded(authorization_page):
    authorization_page.check_open()

@then('Кнопка "Выход из системы" доступна для нажатия')
def check_clickable_logout(browser):
    main_page = CheckMainPage(browser)
    main_page.check_clickable_logout()

@then('Пользователю доступны разделы и модули согласно ролям')
@then('Доступны функции согласно ролям')
def check_roles_access():
    pass

@then('Выполняется проверка журнала действий пользователя')
@then('Аутентификация отображается в журнале действий')
def check_audit_log(main_page, user_actions_page):
    test_start_time = datetime.datetime.now()
    main_page.open_main_menu()
    main_page.click_submenu("Аудит", "Журнал действий пользователей")
    user_actions_page.check_open()
    user_actions_page.check_auth_user(test_start_time)
