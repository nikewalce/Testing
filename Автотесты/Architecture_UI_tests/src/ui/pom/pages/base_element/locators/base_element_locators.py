from src.ui.locators.base_locator import Locator

SORTED_BUTTON = Locator(
    value='//span[contains(text(), "{name}")]/following-sibling::i',
    name="Кнопка сортировки",
)
