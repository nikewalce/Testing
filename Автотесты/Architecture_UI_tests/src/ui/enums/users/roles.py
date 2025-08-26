from enum import Enum


class RoleUser(Enum):
    ADMINISTRATOR = "Администратор"
    USER_CHANGE_PAROL = "Пользователь со сбросом пароля"
    BLOCK_USER = "Пользователь заблокирован"
    NOACTIVE_USER = "Пользователь неактивен"
