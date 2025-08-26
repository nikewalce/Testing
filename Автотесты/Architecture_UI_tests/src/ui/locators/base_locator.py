from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import field_validator
from selenium.webdriver.common.by import By


class Locator(BaseModel):
    """
    Класс для представления и работы с локаторами элементов на веб-странице.

    :param by: Тип локатора, по умолчанию используется XPATH.
    :param value: Строка XPATH локатора, поддерживающая форматирование.
    :param name: Человекочитаемое имя локатора (необязательно).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    by: str = Field(default=By.XPATH)
    value: str
    name: Optional[str] = None

    @field_validator("by")
    def validate_by(cls, v):
        """
        Валидация поля `by`.

        :param v: Значение для валидации.
        :return: Проверенное значение.
        :raises ValueError: Если значение не является
                            поддерживаемым типом локатора.
        """
        if v != By.XPATH:
            raise ValueError(
                f"Неподдерживаемый тип локатора: {v}. Разрешен только XPATH"
            )
        return v

    def __repr__(self):
        """
        Возвращает строковое представление объекта Locator.

        :return: Строковое представление объекта.
        """
        return f"Locator(by={self.by}, value={self.value}, name={self.name})"

    def format(self, *args, **kwargs):
        """
        Возвращает новый объект Locator с отформатированным значением.

        :param kwargs: Аргументы для форматирования строки value.
        :return: Новый объект Locator с отформатированным значением.
        """
        formatted_value = self.value.format(*args, **kwargs)
        return Locator(by=self.by, value=formatted_value, name=self.name)
