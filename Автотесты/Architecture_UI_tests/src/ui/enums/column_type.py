from enum import Enum


class ColumnType(Enum):
    BY_CHECKBOX = "чекбокс"
    BY_MASK = "по маске"
    BY_LIST = "из выпадающего списка"
    BY_PLACEHOLDER_WITHOUT_CONFIRM = (
        "по подсказке внутри поля без подтверждения"
    )
    BY_PLACEHOLDER = "по подсказке внутри поля с подтверждением"
    BY_MASK_WITHOUT_CONFIRM = "по маске без подтверждения выбора"
    BY_YEAR = "год"
    BY_DATE = "дата"
    BY_DATE_FROM = "дата с"
    BY_DATE_TO = "дата по"
    BY_SWITCH = "переключатель"
    BY_FILE_INPUT = "выбор файла"
    BY_OPTIONS_INPUT = "выбор в настройках"
    READONLY = "только для чтения"
    TABLE_BY_MASK_WITHOUT_CONFIRM = (
        "поле в таблице по маске без подтверждения выбора"
    )
