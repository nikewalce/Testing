import email
import poplib
import re
from contextlib import closing
from email import policy

from decouple import config
from dotenv import load_dotenv
from faker import Faker
from lxml import html

# from src.api.database import Database
from src.ui.enums.users.roles import RoleUser
from src.ui.locators.authorization import login_page_locators
from src.ui.pom.core.base_manager import BaseManager
from src.ui.pom.pages.base_element.locators import base_element_locators
from src.ui.locators.authorization import login_page_locators as locators
from src.ui.locators.my_profile import my_profile_locators
from src.ui.locators.authorization import reset_password_locators
from selenium.common.exceptions import TimeoutException

load_dotenv()
fake = Faker()


class AuthorizationPage(BaseManager):
    """
    Набор методов для работы со страницей Авторизация.
    """

    @classmethod
    def get_roles(cls):
        return {
            RoleUser.ADMINISTRATOR.value: [
                config("USER_NAME"),
                config("USER_PASS"),
            ],
        }

    @classmethod
    def get_divisions(cls):
        return {
            "0": [config("DIVISION_ZERO"), config("DIVISION_ZERO_PASS")],
            "1": [config("DIVISION_ONE"), config("DIVISION_ONE_PASS")],
            "2": [config("DIVISION_TWO"), config("DIVISION_TWO_PASS")],
            "3": [config("DIVISION_THREE"), config("DIVISION_THREE_PASS")],
            "все": [config("DIVISION_ALL"), config("DIVISION_ALL_PASS")],
        }

    def check_open(self):
        """Проверка открытие страницы авторизации."""
        self.check.windows.verify_url(config("PORTAL_URL"), timeout=30)

    def open_auth_page(self):
        """Открытие страницы авторизации"""
        self.interactions.go_to_page(config("PORTAL_URL"), login_page_locators.LOGIN_TITLE_TEXT, 30)

    def check_auth_page(self):
        """Проверка отображения текста 'Вход в систему'"""
        self.check.elements.verify_visible(login_page_locators.LOGIN_TITLE_TEXT, timeout=5)

    def refresh_page(self):
        """Обновление страницы"""
        self.interactions.refresh_page()

    def click_back_button(self):
        """Нажимает на кнопку назад"""
        self.interactions.go_back()

    def go_to_page(self):
        """Переход на страницу по ссылке"""
        try:
            self.interactions.go_to_page(config("MY_PROFILE_URL"),
                                         wait_locator=my_profile_locators.MY_PROFILE_TEXT,
                                         timeout=30)
            return True
        except TimeoutException:
            self.logger.error("Страница профиля не загрузилась за отведённое время")
            return False

    def get_field_value(self, field: str):
        """Получить текущее значение из поля логина или пароля, чтобы было не пустое.

        :param field: Название поля ('логин' или 'пароль')
        """
        if field.lower() == "логин":
            locator = locators.LOGIN_FIELD
        elif field.lower() == "пароль":
            locator = locators.PASSWORD_FIELD
        else:
            raise ValueError(f"Некорректное имя поля: '{field}'. Ожидается 'логин' или 'пароль'.")

        assert self.interactions.get_input_value(locator, timeout=30) != "", f"Поле {field.lower()} не должно быть пустым"

    def check_empty_fields(self, login_value, password_value):
        """
            Проверить, что поля логина и/или пароля пустые, в зависимости от переданных значений.

        :param login_value: Значение логина из примера
        :param password_value: Значение пароля из примера
        """
        if login_value == "существующий":
            login_value = config("USER_NAME")
        elif login_value == "пустой":
            login_value = ""
        if password_value == "валидный":
            password_value = config("USER_PASS")
        elif password_value == "пустой":
            password_value = ""
        actual_login = self.interactions.get_input_value(login_page_locators.LOGIN_FIELD, timeout=10)
        self.logger.info(f"В поле логин введен: {actual_login}")
        assert actual_login == login_value, f"Ожидалось, что поле 'логин' будет пустым, но получено '{actual_login}'"
        actual_password = self.interactions.get_input_value(login_page_locators.PASSWORD_FIELD, timeout=10)
        self.logger.info(f"В поле логин введен: {actual_password}")
        assert actual_password == password_value, f"Ожидалось, что поле 'пароль' будет пустым, но получено '{actual_password}'"

    def is_field_empty(self, field: str, enter_data: str):
        """Проверяет, что поле подсвечено как пустое (имеет красную рамку).

        :param field: Название поля ('логин' или 'пароль').
        :param enter_data: Введенные данные в поле логина или пароля
        """
        if field.lower() == "логин":
            locator = locators.LOGIN_FIELD
        elif field.lower() == "пароль":
            locator = locators.PASSWORD_FIELD
        else:
            raise ValueError(f"Некорректное имя поля: '{field}'. Ожидается 'логин' или 'пароль'.")
        if enter_data == "":
            #Получить цвет рамки
            border_color = self.interactions.get_element_color_property(locator, "border-color", timeout=5)
            self.logger.info(f"{field.capitalize()} — цвет рамки: {border_color}")
            assert border_color in ['#F93232', 'rgb(249, 50, 50)']

    def is_field_invalid(self, field: str):
        """Проверяет, что поле подсвечено как некорректное (имеет красную рамку и текст).

        :param field: Название поля ('логин' или 'пароль').
        """
        if field.lower() == "логин":
            locator = locators.LOGIN_FIELD
        elif field.lower() == "пароль":
            locator = locators.PASSWORD_FIELD
        else:
            raise ValueError(f"Некорректное имя поля: '{field}'. Ожидается 'логин' или 'пароль'.")
        #Получить цвет рамки
        border_color = self.interactions.get_element_color_property(locator, "border-color", timeout=5)
        # Получить цвет текста:
        text_color = self.interactions.get_element_color_property(locator, "color")
        self.logger.info(f"{field.capitalize()} — цвет рамки: {border_color}, цвет текста {text_color}")
        assert border_color in ['#F93232', 'rgb(249, 50, 50)']
        assert text_color in ['#F93232', 'rgba(249, 50, 50, 1)']

    def entering_field(self, value: str, field: str):
        """Ввод данных в поля логина и пароля.

        :param field: Название поля ('логин' или 'пароль')
        :param value: Тип ввода ('существующий', 'несуществующий', 'валидный', 'невалидный')
        """
        input_data = {
            "логин": {
                "существующий": {"value": config("USER_NAME")},
                "несуществующий": {"value": fake.user_name()},
                "пустой": {"value": ""}
            },
            "пароль": {
                "валидный": {"value": config("USER_PASS")},
                "невалидный": {"value": fake.user_name()},
                "пустой": {"value": ""},
                "восстановленный": {
                    "value": lambda: self.get_verification_code(
                        message_type="пароль"
                    ),
                    "delay": 5,
                },
            },
        }
        if field not in input_data:
            raise ValueError(f"Недопустимое поле: {field}")
        if value not in input_data[field]:
            raise ValueError(f"Недопустимое значение для '{field}': {value}")

        entry = input_data[field][value]
        value_to_enter = entry["value"]

        if "delay" in entry:
            self.helpers.pause(entry["delay"])

        if callable(value_to_enter):
            value_to_enter = value_to_enter()

        self.interactions.input_text(
            base_element_locators.FIELD.format(name=field.capitalize()),
            text=value_to_enter,
            timeout=30
        )

    def get_reset_password_link(self, last_n: int = 3):
        """Получение ссылки для сброса пароля из последних N писем"""
        username = config("MAIL_USERNAME")
        password = config("MAIL_PASSWORD")
        pattern = r"(https://[^\s]+/reset-password/[a-z0-9\-]+)"

        try:
            with closing(poplib.POP3_SSL("mail.itfb.com")) as mail:
                mail.user(username)
                mail.pass_(password)
                email_count = len(mail.list()[1])
                if email_count == 0:
                    return None
                for i in range(email_count, max(email_count - last_n, 0), -1):
                    _, lines, _ = mail.retr(i)
                    msg_content = b"\n".join(lines)
                    msg = email.message_from_bytes(msg_content, policy=policy.default)

                    html_text = next(
                        (
                            part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            for part in msg.iter_parts()
                            if part.get_content_type() in ("text/html", "text/plain")
                        ),
                        None,
                    )
                    if not html_text:
                        continue
                    text = html.fromstring(html_text).text_content()
                    match = re.search(pattern, text)
                    if match:
                        return match.group(1)
        except poplib.error_proto as e:
            self.logger.error(f"Ошибка POP3: {e}")
        return None

    def get_verification_code(self, message_type: str):
        """Получение кода проверки из почты
        :param message_type: текст типа сообщения (код проверки, пароль, проверочный код, сдаточная опись)
        authorization_page.get_verification_code("пароль"))
        """
        username = config("MAIL_USERNAME")
        password = config("MAIL_PASSWORD")
        type_mail = {
            "код проверки": "Код безопасности для входа: ",
            "пароль": "Пароль: ",
            "проверочный код": "Ваш код подтверждения: ",
            "сдаточная опись": "Необходимо вынести решение о согласовании по проекту сдаточной описи: ",
        }
        pattern = rf"{re.escape(type_mail[message_type])}(\d+)"
        try:
            with closing(poplib.POP3_SSL("mail.itfb.com")) as mail:
                mail.user(username)
                mail.pass_(password)

                if (email_count := len(mail.list()[1])) == 0:
                    return None

                _, lines, _ = mail.retr(email_count)
                msg_content = b"\n".join(lines)
                msg = email.message_from_bytes(
                    msg_content, policy=policy.default
                )
                html_text = next(
                    (
                        part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore"
                        )
                        for part in msg.iter_parts()
                        if part.get_content_type() == "text/html"
                    ),
                    None,
                )
                if html_text:
                    text = html.fromstring(html_text).text_content()
                    match = re.search(pattern, text)
                    if match:
                        return match.group(1)
        except poplib.error_proto as e:
            self.logger.error(f"Ошибка POP3: {e}")

        return None
