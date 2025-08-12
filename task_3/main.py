import asyncio
from datetime import date
import logging
from src.logger_setup import LoggerConfigurator
from src.database.connector import DatabaseConnection
from src.database.order_repository import OrdersRepository
from src.config_model import DatabaseConfig

logging.disable(logging.CRITICAL)
LoggerConfigurator.configure()


async def start_script(config, new_orders, year):
    """Точка входа в скрипт"""

    db_connection = DatabaseConnection(config)
    await db_connection.connect()

    try:
        orders_repo = OrdersRepository(db_connection)
        
        # Создаем таблицу, если не существует
        await orders_repo.initialize()

        # Вставка нескольких заказов (массив словарей с ключами: customer_id, order_date, amount)
        await orders_repo.bulk_insert_orders(new_orders)

        total_by_customer = await orders_repo.get_total_sum_by_customer()
        print("Общая сумма заказов по клиентам:")
        for item in total_by_customer:
            print(str(item))

        print('\n')
        max_customer = await orders_repo.get_customer_with_max_total()
        print(str(max_customer), '\n')

        orders_count_year = await orders_repo.get_orders_count_for_year(year)
        print(str(orders_count_year), '\n')

        avg_amount_by_customer = await orders_repo.get_avg_amount_by_customer()
        for item in avg_amount_by_customer:
            print(str(item))

    except Exception as e:
        logging.error(e)
    finally:
        await db_connection.close()


if __name__ == "__main__":
    # Добавление 10 заказов
    new_orders = [
        {"customer_id": 1, "order_date": date(2023, 1, 15), "amount": 150.00},
        {"customer_id": 2, "order_date": date(2023, 2, 10), "amount": 200.50},
        {"customer_id": 1, "order_date": date(2023, 3, 5), "amount": 99.99},
        {"customer_id": 3, "order_date": date(2021, 4, 12), "amount": 250.00},
        {"customer_id": 4, "order_date": date(2023, 5, 20), "amount": 175.75},
        {"customer_id": 2, "order_date": date(2023, 6, 25), "amount": 300.40},
        {"customer_id": 5, "order_date": date(2025, 7, 14), "amount": 50.00},
        {"customer_id": 3, "order_date": date(2023, 8, 9), "amount": 400.00},
        {"customer_id": 1, "order_date": date(2023, 9, 3), "amount": 120.00},
        {"customer_id": 4, "order_date": date(2022, 10, 29), "amount": 220.00},
    ]
    # Конфиг ДБ (можно вынести в .env или config.ini)
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        user="postgres",
        password="AV123",
        database="employees"
    )
    # Год сбора данных
    year = 2023
    asyncio.run(start_script(config, new_orders, year))