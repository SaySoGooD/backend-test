import logging
from typing import List, Optional
from src.database.connector import DatabaseConnection
from src.database.dto import CustomerAvgDTO, CustomerTotalDTO, MaxCustomerTotalDTO, OrdersCountDTO


class OrdersRepository:
    """Репозиторий для работы с таблицей orders"""

    def __init__(self, db_connection: DatabaseConnection):
        self._db = db_connection

    async def initialize(self) -> None:
        """Создание таблицы orders, если не существует"""
        async with self._db.connection() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INT NOT NULL,
                    order_date DATE NOT NULL,
                    amount NUMERIC(15, 2) NOT NULL
                )
            """)
            logging.info("Таблица 'orders' готова к работе")

    async def get_total_sum_by_customer(self) -> List[CustomerTotalDTO]:
        """Общая сумма заказов по каждому клиенту"""
        async with self._db.connection() as conn:
            logging.info("Выполняется запрос: общая сумма заказов по клиентам")
            rows = await conn.fetch("""
                SELECT customer_id, SUM(amount) AS total_amount
                FROM orders
                GROUP BY customer_id
            """)
            logging.info(f"Получено записей: {len(rows)}")
            return [CustomerTotalDTO(**dict(row)) for row in rows]

    async def get_customer_with_max_total(self) -> Optional[MaxCustomerTotalDTO]:
        """Клиент с максимальной суммой заказов"""
        async with self._db.connection() as conn:
            logging.info("Выполняется запрос: клиент с максимальной суммой заказов")
            row = await conn.fetchrow("""
                SELECT customer_id, SUM(amount) AS total_amount
                FROM orders
                GROUP BY customer_id
                ORDER BY total_amount DESC
                LIMIT 1
            """)
            if row:
                logging.info(
                    f"Найден клиент с max суммой заказов: его id:{row['customer_id']}, сумма: {row['total_amount']}")
                return MaxCustomerTotalDTO(**dict(row))
            logging.info("Клиенты не найдены")
            return None

    async def get_orders_count_for_year(self, year: int) -> OrdersCountDTO:
        """Количество заказов за указанный год"""
        async with self._db.connection() as conn:
            logging.info(f"Выполняется запрос: количество заказов за {year} год")
            row = await conn.fetchrow("""
                SELECT EXTRACT(YEAR FROM order_date) AS year, COUNT(*) AS orders_count
                FROM orders
                WHERE EXTRACT(YEAR FROM order_date) = $1
                GROUP BY year
            """, year)
            if row:
                logging.info(f"Найдено заказов за {year}: {row['orders_count']}")
                return OrdersCountDTO(**dict(row))
            logging.info(f"Заказов за {year} не найдено")
            return OrdersCountDTO(year=year, orders_count=0)

    async def get_avg_amount_by_customer(self) -> List[CustomerAvgDTO]:
        """Средняя сумма заказов по каждому клиенту"""
        async with self._db.connection() as conn:
            logging.info("Выполняется запрос: средняя сумма заказов по клиентам")
            rows = await conn.fetch("""
                SELECT customer_id, AVG(amount) AS avg_amount
                FROM orders
                GROUP BY customer_id
            """)
            logging.info(f"Получено записей: {len(rows)}")
            return [CustomerAvgDTO(**dict(row)) for row in rows]

    async def bulk_insert_orders(self, orders: List[dict]) -> None:
        """
        Вставка нескольких заказов одним запросом.
        orders - список словарей с ключами: customer_id, order_date, amount
        """
        async with self._db.connection() as conn:
            logging.info(f"Выполняется множественная вставка {len(orders)} заказов")
            values = [(o["customer_id"], o["order_date"], o["amount"]) for o in orders]
            await conn.executemany("""
                INSERT INTO orders (customer_id, order_date, amount)
                VALUES ($1, $2, $3)
            """, values)
            logging.info("Множественная вставка завершена")
