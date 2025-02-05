import pytest
import allure
from pages.main_page import MainPage

test_data = [
    {"link_text": "О нас", "expected_url": "https://effective-mobile.ru/#about"},
    {"link_text": "Услуги", "expected_url": "https://effective-mobile.ru/#moreinfo"},
    {"link_text": "Проекты", "expected_url": "https://effective-mobile.ru/#cases"},
    {"link_text": "Отзывы", "expected_url": "https://effective-mobile.ru/#Reviews"},
    {"link_text": "Контакты", "expected_url": "https://effective-mobile.ru/#contacts"},
]


@allure.feature("Проверка навигационных ссылок")
@pytest.mark.parametrize("data", test_data)
def test_links(driver, data):
    page = MainPage(driver)

    page.click_link(data["link_text"])

    current_url = page.get_current_url()
    assert current_url == data["expected_url"], (
        f"Ожидался URL {data['expected_url']}, но получен {current_url}"
    )
