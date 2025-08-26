from enum import Enum


class MainMenuForm(Enum):
    NOMENCLATURE = "Номенклатуры дел"
    EDOCK = "Электронные документы"
    CASE = "Дела"
    INVENTORY = "Описи"
    RECEIVE_ACT = "Акты приема-передачи"
    DELETE_ACT = "Акты об уничтожении"
    TC = "Транспортные контейнеры"
    ADMINISTRATION = "Администрирование"
    NSI = "НСИ"
    SYSTEM_OPTIONS = "Системные настройки"


class InventorySubForm(Enum):
    DELIVERY_INVENTORY = "Сдаточные описи"
    SUMMARY_INVENTORY = "Сводные описи"


class AdministrationSubForm(Enum):
    USER = "Пользователи"
    EVENT_LOG = "Журнал событий"
    SYSTEM_ROLES = "Системные роли"


class MainMenuSubFormEntry(Enum):
    PROJECT = "Проекты"
    APPROVED = "Утвержденные"
