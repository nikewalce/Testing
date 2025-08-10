from sqlalchemy import create_engine, MetaData, Table, select, delete

class CartDB:
    def __init__(self):
        """Инициализируем БД и необходимые таблицы"""
        self.engine = create_engine("mysql+pymysql://bn_opencart:@localhost:3306/bitnami_opencart")
        self.metadata = MetaData()
        self.cart_table = Table("oc_cart", self.metadata, autoload_with=self.engine)
        self.api_session = Table("oc_api_session", self.metadata, autoload_with=self.engine)
        self.oc_session = Table("oc_session", self.metadata, autoload_with=self.engine)

    def select_oc_session(self, api_token):
        """Вывод таблицы oc_session по session_id(токен)"""
        with self.engine.connect() as conn:
            stmt = select(self.oc_session).where(
                self.oc_session.c.session_id == api_token
            )
            result = conn.execute(stmt).fetchone()
            return result

    def select_cart_info(self):
        """Вывод таблицы cart_table"""
        with self.engine.connect() as conn:
            result = conn.execute(select(self.cart_table).limit(10))
            for row in result.mappings():
                print(dict(row))

    def select_cart_info_by_session_id(self, session_id):
        """Проверка, что товар, созданный в определенной сессии существует в таблице"""
        with self.engine.connect() as conn:
            stmt = select(self.cart_table).where(
                self.cart_table.c.session_id == session_id
            )
            result = conn.execute(stmt).fetchone()
            return result is not None

    def select_cart_id_by_session_id(self, session_id):
        """Вывод cart_id товара, созданного в определенной сессии"""
        with self.engine.begin() as conn:
            stmt = select(self.cart_table.c.cart_id).where(
                self.cart_table.c.session_id == session_id
            )
            result = conn.execute(stmt).fetchone()
            return result[0]

    def select_session_info(self):
        """Вывод таблицы api_session"""
        with self.engine.connect() as conn:
            result = conn.execute(select(self.api_session).limit(10))
            for row in result.mappings():
                print(dict(row))

    def delete_cart_by_api_id(self, api_id: int):
        """Удаление товара"""
        with self.engine.begin() as conn:
            stmt = delete(self.cart_table).where(self.cart_table.c.api_id == api_id)
            conn.execute(stmt)

    def delete_session_by_session_id(self, session_id: str):
        """Удаление сессии"""
        with self.engine.begin() as conn:
            stmt = delete(self.api_session).where(self.api_session.c.session_id == session_id)
            conn.execute(stmt)

    def delete_oc_session_by_session_id(self, session_id: str):
        """Удаление данных сессии из таблицы oc_session"""
        with self.engine.begin() as conn:
            stmt = delete(self.oc_session).where(self.oc_session.c.session_id == session_id)
            conn.execute(stmt)

    def check_product_in_cart(self, session_id, product_id, quantity):
        """Проверка, что продукт с определенными session_id, product_id, quantity существует в таблице"""
        with self.engine.begin() as conn:
            stmt = select(self.cart_table).where(
                self.cart_table.c.session_id == session_id,
                self.cart_table.c.product_id == product_id,
                self.cart_table.c.quantity == quantity
            )
            result = conn.execute(stmt).fetchone()
            return result is not None

    def check_update_quantity_in_cart(self, cart_id, session_id, quantity):
        """Проверка, что изменилось количество товара в таблице"""
        with self.engine.begin() as conn:
            stmt = select(self.cart_table).where(
                self.cart_table.c.session_id == session_id,
                self.cart_table.c.cart_id == cart_id,
                self.cart_table.c.quantity == quantity
            )
            result = conn.execute(stmt).fetchone()
            return result is not None
