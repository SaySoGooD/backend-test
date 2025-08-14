import asyncio
from decimal import Decimal
import logging

from src.config_model import DatabaseConfig
from src.database.connector import DatabaseConnection
from src.database.product_repository import ProductRepository
from src.setup_logger import configure


async def main(config, products_data):
    db = DatabaseConnection(config)
    await db.connect()

    repo = ProductRepository(db)

    try:
        # Добавляем 10 тестовых продуктов
        await repo.insert_products(products_data)
        print("✅ Добавлено 10 тестовых продуктов")

        # Получаем товары с остатком < 10
        low_stock = await repo.get_low_stock_products(threshold=10)
        print("\n📦 Продукты с остатком < 10:")
        for p in low_stock:
            print(f"{p.id}: {p.name} — {p.price} ₽, {p.quantity} шт.")

        # Обновляем цену одного из продуктов
        await repo.update_price_by_name("Apple", Decimal("19.99"))
        updated_product = await repo.get_product_by_name("Apple")
        print("\n💰 После обновления цены:")
        print(
            f"{updated_product.id}: {updated_product.name} — {updated_product.price} ₽, {updated_product.quantity} шт.")
    finally:
        await db.close()


if __name__ == "__main__":
    configure(logging.INFO)

    config = DatabaseConfig(
        host="localhost",
        port=5432,
        user="postgres",
        password="AV123",
        database="employees"
    )

    products_data = [
        {"name": "Apple", "price": Decimal("15.50"), "quantity": 5},
        {"name": "Banana", "price": Decimal("7.20"), "quantity": 20},
        {"name": "Orange", "price": Decimal("10.00"), "quantity": 8},
        {"name": "Mango", "price": Decimal("25.00"), "quantity": 2},
        {"name": "Grapes", "price": Decimal("18.30"), "quantity": 15},
        {"name": "Peach", "price": Decimal("12.00"), "quantity": 7},
        {"name": "Cherry", "price": Decimal("30.00"), "quantity": 50},
        {"name": "Strawberry", "price": Decimal("40.00"), "quantity": 3},
        {"name": "Pineapple", "price": Decimal("22.00"), "quantity": 1},
        {"name": "Watermelon", "price": Decimal("50.00"), "quantity": 12},
    ]

    asyncio.run(main(config, products_data))
