import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    def __init__(self, env_file: str = ".env"):
        env_path = Path(__file__).resolve().parent / env_file
        load_dotenv(dotenv_path=env_path)
        self.username = os.getenv("ADMIN_USERNAME")
        self.password = os.getenv("ADMIN_PASSWORD")
        self.product_name = os.getenv("PRODUCT_NAME")
        self.meta_tag_title = os.getenv("META_TAG_TITLE")
        self.model = os.getenv("MODEL")
        self.keyword = os.getenv("KEYWORD")
        self.register_firstname = os.getenv("REGISTER_FIRSTNAME")
        self.register_lastname = os.getenv("REGISTER_LASTNAME")
        self.register_email = os.getenv("REGISTER_EMAIL")
        self.register_shipping_address1 = os.getenv("REGISTER_SHIPPING_ADDRESS1")
        self.register_city = os.getenv("REGISTER_CITY")
        self.register_postcode = os.getenv("REGISTER_POSTCODE")
        self.register_password = os.getenv("REGISTER_PASSWORD")
        self.token_username = os.getenv("TOKEN_USERNAME")
        self.token_key = os.getenv("TOKEN_KEY")
        self.register_telephone = os.getenv("REGISTER_TELEPHONE")
        self.register_country_id = os.getenv("REGISTER_COUNTRY_ID")
        self.register_zone_id = os.getenv("REGISTER_ZONE_ID")
