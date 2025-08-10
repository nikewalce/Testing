import allure
import pytest

@allure.feature('DIPLOM')
@allure.story('Тестирование регистрации')
@allure.title('Регистрация пользователя при оформление товара')
@pytest.mark.ui_cart
def test_user_registration_at_checkout_product(browser, base_url, clean_test_data, pages):
    pages.browser.get(base_url)
    pages.main.click_cameras_button()
    pages.catalog.click_add_to_cart_canon_e0s5d_button()
    pages.product_cart \
                    .click_select_available_options_dropdown_button() \
                    .qty_entry() \
                    .click_add_to_cart_button() \
                    .click_shopping_cart()
    pages.checkout_cart \
                    .click_checkout_button() \
                    .click_input_register_account() \
                    .click_button_continue() \
                    .enter_firstname() \
                    .enter_lastname() \
                    .enter_email() \
                    .enter_phone() \
                    .enter_shipping_address() \
                    .enter_shipping_city() \
                    .enter_shipping_postcode() \
                    .select_shipping_county() \
                    .select_shipping_region() \
                    .enter_password() \
                    .enter_password_confirm() \
                    .click_checkbox() \
                    .click_continue() \
                    .reload_page() \
                    .click_my_account()
    pages.account_account.click_edit_account_information()
    assert pages.account_info.check_data() == True

@allure.feature('DIPLOM')
@allure.story('Тестирование оформления заказа')
@allure.title('Оформление заказа авторизованным пользователем со страницы сравнения')
@pytest.mark.ui_cart
def test_checkout_from_compare_page_authenticated_user(browser, base_url, create_user_with_address, pages):
    pages.browser.get(base_url)
    pages.main \
            .click_my_account_button() \
            .click_link_login()
    pages.account_login \
                    .enter_email() \
                    .enter_password() \
                    .click_login_button()
    pages.account_account.click_PhonesAndPDAs()
    pages.catalog \
                .click_compare_htc_button() \
                .click_compare_iphone_button() \
                .click_compare_palm_button() \
                .enter_string_in_search() \
                .click_search_button()
    pages.search \
                .click_samsung_compare() \
                .click_total_compare_link()
    pages.compare_product \
                        .click_remove_htc_button() \
                        .click_add_to_cart_iphone() \
                        .click_add_to_cart_palm() \
                        .click_shopping_cart_link()
    pages.checkout_cart \
                    .click_remove_palm_button() \
                    .enter_quantity_iphone() \
                    .click_update_button() \
                    .click_estimate_shipping_link() \
                    .click_select_estimate_country() \
                    .click_select_estimate_region() \
                    .enter_estimate_postcode() \
                    .click_get_quotes_button() \
                    .click_cancel_modal_button() \
                    .click_checkout_button() \
                    .click_checkbox_use_existing_address() \
                    .click_continue_button_payment_address() \
                    .click_checkbox_use_existing_shipping_address() \
                    .click_continue_button_shipping_address() \
                    .enter_comment_textarea() \
                    .click_continue_button_shipping_method() \
                    .click_checkbox() \
                    .click_continue_button_payment_method() \
                    .click_confirm_order_button()
    pages.checkout_success \
                            .click_my_account_button() \
                            .click_order_history_button()
    assert pages.account_order.check_customer_info()

@allure.feature('DIPLOM')
@allure.story('Тестирование заявки на возврат товара')
@allure.title('Заявка на возврат ранее заказанного товара')
@pytest.mark.ui_cart
def test_checkout_from_compare_as_authorized_user(browser, base_url, create_user_with_address, pages):
    pages.browser.get(base_url)
    #<Предусловие
    pages.main \
                .click_my_account_button() \
                .click_link_login()
    pages.account_login \
                        .enter_email() \
                        .enter_password() \
                        .click_login_button()
    pages.account_account.click_main_page_logo()
    # Предусловие>
    pages.main \
                .components_mouseover() \
                .click_monitors_link()

    pages.catalog \
                    .click_add_to_wish_list_apple() \
                    .click_add_to_wish_list_samsung() \
                    .click_wish_list()
    pages.account_wishlist.click_add_to_cart_apple_button()
    pages.product_cart \
                        .click_radio_medium_checkbox() \
                        .click_checkbox3() \
                        .click_checkbox4() \
                        .enter_text_text() \
                        .click_select_available_options_dropdown() \
                        .click_yellow_available_options() \
                        .enter_textarea_available_options() \
                        .upload_file() \
                        .enter_date_time() \
                        .qty_entry() \
                        .click_add_to_cart_button() \
                        .click_cart_div() \
                        .click_cart_checkout()
    pages.checkout_cart \
                        .click_checkbox_use_existing_address() \
                        .click_continue_button_payment_address() \
                        .click_checkbox_use_existing_shipping_address() \
                        .click_continue_button_shipping_address() \
                        .enter_comment_textarea() \
                        .click_continue_button_shipping_method() \
                        .click_checkbox() \
                        .click_continue_button_payment_method() \
                        .click_confirm_order_button()
    pages.checkout_success \
                        .click_my_account_button() \
                        .click_order_history_button()
    pages.account_order \
                        .click_view_button() \
                        .click_return_link() \
                        .enter_telephone() \
                        .click_reason_for_return_checkbox() \
                        .click_submit_button()
    assert "account/return/success" in browser.current_url, "URL не содержит 'account/return/success'"
