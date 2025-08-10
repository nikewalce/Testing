from sqlalchemy import create_engine, MetaData, Table, insert, update, select, func, delete
from datetime import datetime
import random
import hashlib
import string

class OpenCartDB:
    def __init__(self):
        """Инициализируем БД и необходимые таблицы"""
        self.engine = create_engine("mysql+pymysql://bn_opencart:@localhost:3306/bitnami_opencart")
        self.metadata = MetaData()
        self.customer_table = Table("oc_customer", self.metadata, autoload_with=self.engine)
        self.cart_table = Table("oc_cart", self.metadata, autoload_with=self.engine)
        self.address_table = Table("oc_address", self.metadata, autoload_with=self.engine)
        self.order_table = Table("oc_order", self.metadata, autoload_with=self.engine)
        self.return_table = Table("oc_return", self.metadata, autoload_with=self.engine)
        self.order_product_table = Table("oc_order_product", self.metadata, autoload_with=self.engine)
        self.order_history_table = Table("oc_order_history", self.metadata, autoload_with=self.engine)
        self.order_total_table = Table("oc_order_total", self.metadata, autoload_with=self.engine)

    def generate_oc_password(self, password):
        """Генерирует хешированный пароль с солью"""
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        hashed = hashlib.sha1((salt + hashlib.sha1((salt + hashlib.sha1(password.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
        return hashed, salt

    def create_customer_with_address(self, firstname, lastname, email, phone, password,
                                     address_1, city, postcode, country_id, zone_id):
        # Вставка пользователя
        result_customer = self._insert_customer(firstname, lastname, email, phone, password)
        customer_id = result_customer.inserted_primary_key[0]
        # Вставка адреса
        result_address = self._insert_address(customer_id, firstname, lastname, address_1, city, postcode, country_id,
                                              zone_id)
        address_id = result_address.inserted_primary_key[0]
        with self.engine.begin() as conn:
            conn.execute(update(self.customer_table)
                         .where(self.customer_table.c.customer_id == customer_id)
                         .values(address_id=address_id))

    def _insert_customer(self, firstname, lastname, email, phone, password):
        hashed_password, salt = self.generate_oc_password(password)
        with self.engine.begin() as conn:
            return conn.execute(insert(self.customer_table).values(
                customer_group_id=1,
                store_id=0,
                language_id=1,
                firstname=firstname,
                lastname=lastname,
                email=email,
                telephone=phone,
                fax='',
                password=hashed_password,
                salt=salt,
                cart=None,
                wishlist=None,
                newsletter=0,
                address_id=0,  # временно
                custom_field='',
                ip='127.0.0.1',
                status=1,
                safe=0,
                token='',
                code='',
                date_added=datetime.now()
            ))

    def _insert_address(self, customer_id, firstname, lastname, address_1, city, postcode, country_id, zone_id):
        with self.engine.begin() as conn:
            return conn.execute(insert(self.address_table).values(
                customer_id=customer_id,
                firstname=firstname,
                lastname=lastname,
                company='',
                address_1=address_1,
                address_2='',
                city=city,
                postcode=postcode,
                country_id=country_id,
                zone_id=zone_id,
                custom_field=''
            ))

    def select_users_info(self, limit=10):
        """Извлекает информацию о пользователях customer_table"""
        with self.engine.connect() as conn:
            result = conn.execute(select(self.customer_table).limit(limit))
            return [dict(row) for row in result.mappings()]# <-- возвращает dict-подобные строки

    def delete_user_by_email(self, email):
        """Удаляет запись о пользователе по email из таблицы oc_customer"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.customer_table).where(self.customer_table.c.email == email))

    def delete_order_by_email(self, email):
        """Удаляет заказы пользователя по email из таблицы oc_order"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.order_table).where(self.order_table.c.email == email))

    def delete_cart_by_product_id(self, product_id):
        """Удаляет запись о товаре из корзины пользователя по ID продукта"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.cart_table).where(self.cart_table.c.product_id == product_id))

    def delete_address_by_firstname(self, firstname):
        """Удаляет адреса пользователя по firstname"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.address_table).where(self.address_table.c.firstname == firstname))

    def delete_return_by_email(self, email):
        """Удаляет записи о возвратах товара пользователя по его email"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.return_table).where(self.return_table.c.email == email))

    def delete_order_product_by_product_id(self,  product_ids):
        """Удаляет записи о продуктах в заказах. Принимает список ID и одиночный"""
        if isinstance(product_ids, int):
            product_ids = [product_ids]
        if not product_ids:
            return
        with self.engine.begin() as conn:
            conn.execute(
                delete(self.order_product_table).where(
                    self.order_product_table.c.product_id.in_(product_ids)
                )
            )

    def clear_order_history(self):
        """Удаляет всю историю заказов из таблицы oc_order_history"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.order_history_table))

    def clear_order_total(self):
        """Удаляет все записи о суммах заказов из таблицы oc_order_total"""
        with self.engine.begin() as conn:
            conn.execute(delete(self.order_total_table))
