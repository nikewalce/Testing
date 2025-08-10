import requests
import pytest
from tests.api.models import AddCart, DeleteCart, UpdateCart, SelectCart, CurrencyChange, AddVoucher
import json
import allure

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Добавить товар в корзину")
@pytest.mark.api_cart
def test_add_to_cart(base_url, api_token, db, logger):
    add_to_cart_url = f'{base_url}/cart/add&api_token={api_token}'
    add_payload = {
        'product_id': 40,  # ID товара
        'quantity': 1, #кол-во товаров
    }
    with allure.step("Отправка POST-запроса на добавление товара в корзину"):
        logger.info(f"POST {add_to_cart_url} | payload: {add_payload}")
        response = requests.post(add_to_cart_url, data=add_payload)
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
    with allure.step("Проверка кода ответа и валидация модели AddCart"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(AddCart(**response.json()), AddCart), "Валидация ответа от добавления товара в корзину не прошла"
    with allure.step("Проверка, что товар добавлен в корзину (через БД)"):
        assert db.check_product_in_cart(api_token, add_payload['product_id'], add_payload['quantity']), "Товар не добавлен в корзину"

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Изменить количество ранее добавленого товара в корзине")
@pytest.mark.api_cart
def test_update_cart_item_quantity(base_url, api_token, db, logger):
    update_cart_item_url = f'{base_url}/cart/edit&api_token={api_token}'
    # Можно через параметризацию добавить несколько
    update_payload = {
        'key': db.select_cart_id_by_session_id(api_token),  # cart_id из таблицы oc_cart
        'quantity': 2,  # кол-во товаров
    }
    with allure.step("Отправка POST-запроса на изменение количества товара"):
        logger.info(f"POST {update_cart_item_url} | payload: {update_payload}")
        response = requests.post(update_cart_item_url, data=update_payload)
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
    with allure.step("Проверка кода ответа и валидация модели UpdateCart"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(UpdateCart(**response.json()), UpdateCart), "Валидация ответа от изменения товара в корзине не прошла"
    with allure.step("Проверка изменения количества в БД"):
        assert db.check_update_quantity_in_cart(update_payload['key'], api_token, update_payload['quantity']), "В базе данных в таблице oc_cart quantity не равно заданному"

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Получить содержимое корзины")
@pytest.mark.api_cart
def test_select_cart_info(base_url, api_token, db, logger):
    select_cart_info_url = f'{base_url}/cart/products&api_token={api_token}'
    with allure.step("Отправка POST-запроса на получение содержимого корзины"):
        logger.info(f"POST {select_cart_info_url}")
        response = requests.post(select_cart_info_url, data={})
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
    with allure.step("Проверка ответа и валидации модели SelectCart"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(SelectCart(**response.json()), SelectCart), "Валидация ответа от получения содержимого корзины не прошла"
    with allure.step("Проверка, что корзина не пуста в БД"):
        assert db.select_cart_info_by_session_id(api_token)

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Удалить ранее добавленый товар из корзины")
@pytest.mark.api_cart
def test_delete_cart(base_url, api_token, db, logger):
    delete_cart_url = f'{base_url}/cart/remove&api_token={api_token}'
    delete_payload = {
        'key': db.select_cart_id_by_session_id(api_token),  # cart_id из таблицы oc_cart
    }
    with allure.step("Отправка POST-запроса на удаление товара из корзины"):
        logger.info(f"POST {delete_cart_url} | payload: {delete_payload}")
        response = requests.post(delete_cart_url, data=delete_payload)
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
    with allure.step("Проверка кода ответа и валидации модели DeleteCart"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(DeleteCart(**response.json()), DeleteCart), "Валидация ответа от удаления товара из корзины не прошла"
    with allure.step("Проверка, что корзина пуста через БД"):
        assert not db.select_cart_info_by_session_id(api_token)

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Изменения валюты для сессии")
@pytest.mark.parametrize('currency, currency_sign', [('GBP', '£'), ('USD', '$'), ('EUR', '€')])
@pytest.mark.api_cart
def test_session_currency_changes(base_url, api_token, db, currency, currency_sign, logger):
    currency_changes_url = f'{base_url}/currency&api_token={api_token}'
    payload = {
        'currency': currency,
    }
    with allure.step(f"Смена валюты на {currency}"):
        logger.info(f"POST {currency_changes_url} | payload: {payload}")
        response = requests.post(currency_changes_url, data=payload)
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(CurrencyChange(**response.json()),CurrencyChange), "Валидация ответа при смене валюты не прошла"
    with allure.step("Проверка отображения валюты в корзине"):
        select_cart_info_url = f'{base_url}/cart/products&api_token={api_token}'
        response_cart_info = requests.post(select_cart_info_url, data={})
        logger.info(f"Ответ после смены валюты: {response_cart_info.text}")
        assert currency_sign in response_cart_info.json()['totals'][0]['text']
    #Проверяем на вхождение подстроки в строку, т.к. второй элемент кортежа это строка ('4b00d52c16ee85f765caf8165d', '{"api_id":"2","language":"en-gb","currency":"GBP"}', datetime.datetime(2025, 5, 8, 13, 23, 47))
    with allure.step("Проверка смены валюты в БД"):
        assert currency in db.select_oc_session(api_token)[1]

@allure.feature('DIPLOM')
@allure.story('Тестирование API opencart')
@allure.title("Добавление ваучера в корзину для сессии")
@pytest.mark.api_cart
def test_add_voucher_to_cart(base_url, api_token, db, logger):
    add_voucher_to_cart_url = f'{base_url}/voucher/add&api_token={api_token}'
    payload = {
					"from_name": "fromNane",
					"from_email": "from@from.com",
					"to_name": "toName",
					"to_email": "to@to.com",
					"amount": "2",
					"code": "V-1111",
					"message": "strng",
				}
    with allure.step("Отправка запроса на добавление ваучера"):
        logger.info(f"POST {add_voucher_to_cart_url} | payload: {payload}")
        response = requests.post(add_voucher_to_cart_url, data=payload)
        logger.info(f"Response: {response.status_code} | Body: {response.text}")
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert isinstance(AddVoucher(**response.json()), AddVoucher), "Валидация ответа при добавлении ваучера не прошла"
    with allure.step("Проверка, что ваучер появился в сессии в БД"):
        assert json.loads(db.select_oc_session(api_token)[1]).get("vouchers"), "Ключ 'vouchers' отсутствует или пуст"
    with allure.step("Проверка, что ваучер отображается в корзине"):
        select_cart_info_url = f'{base_url}/cart/products&api_token={api_token}'
        response_cart_info = requests.post(select_cart_info_url, data={})
        logger.info(f"Ответ после добавления ваучера: {response_cart_info.text}")
        assert response_cart_info.json().get("vouchers"), "Ключ 'vouchers' пуст или отсутствует в ответе"
        assert isinstance(SelectCart(**response_cart_info.json()), SelectCart), "Валидация ответа от получения содержимого корзины не прошла"
