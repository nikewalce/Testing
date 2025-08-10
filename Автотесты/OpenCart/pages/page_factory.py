from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_cart_page import ProductCartPage
from pages.checkout_cart_page import CheckoutCartPage
from pages.account_information_page import AccountInformationPage
from pages.account_login_page import AccountLoginPage
from pages.account_account_page import AccountAccountPage
from pages.search_page import SearchPage
from pages.compare_product_page import CompareProductPage
from pages.checkout_success_page import CheckoutSuccessPage
from pages.account_order_page import AccountOrderPage
from pages.account_wishlist_page import AccountWishlistPage

class PageFactory:
    def __init__(self, browser):
        self.browser = browser

    @property
    def main(self):
        return MainPage(self.browser)

    @property
    def catalog(self):
        return CatalogPage(self.browser)

    @property
    def product_cart(self):
        return ProductCartPage(self.browser)

    @property
    def checkout_cart(self):
        return CheckoutCartPage(self.browser)

    @property
    def account_info(self):
        return AccountInformationPage(self.browser)

    @property
    def account_login(self):
        return AccountLoginPage(self.browser)

    @property
    def account_account(self):
        return AccountAccountPage(self.browser)

    @property
    def search(self):
        return SearchPage(self.browser)

    @property
    def compare_product(self):
        return CompareProductPage(self.browser)

    @property
    def checkout_success(self):
        return CheckoutSuccessPage(self.browser)

    @property
    def account_order(self):
        return AccountOrderPage(self.browser)

    @property
    def account_wishlist(self):
        return AccountWishlistPage(self.browser)
