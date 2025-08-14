from typing import List, Optional
from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy import delete, update
from src.database.connector import DatabaseConnection
from src.setup_logger import class_logger
from src.database.product_table import Product


@class_logger
class ProductRepository:
    """Репозиторий для работы с сущностью Product."""

    def __init__(self, db: DatabaseConnection):
        """
        Инициализация репозитория.

        Args:
            db (DatabaseConnection): Объект подключения к базе данных, 
                предоставляющий метод session().
        """
        self.db = db

    async def insert_products(self, products_data: List[dict]) -> None:
        """
        Добавляет несколько продуктов в таблицу за одну транзакцию.

        Args:
            products_data (list[dict]): Список словарей с данными о продуктах.
                Каждый словарь должен содержать ключи:
                    - name (str): Название продукта (уникальное).
                    - price (Decimal): Цена продукта.
                    - quantity (int): Количество продукта на складе.
        """
        async with self.db.session() as session:
            products = [Product(**data) for data in products_data]
            session.add_all(products)
            await session.commit()

    async def insert_product(self, product: Product) -> None:
        """
        Вставить один продукт.

        Args:
            product (Product): Объект Product для добавления.
        """
        async with self.db.session() as session:
            session.add(product)
            await session.commit()

    async def get_product_by_id(self, prod_id: int) -> Optional[Product]:
        """
        Получить продукт по ID.

        Args:
            prod_id (int): Идентификатор продукта.

        Returns:
            Optional[Product]: Объект Product или None.
        """
        stmt = select(Product).where(Product.id == prod_id)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_all_products(self) -> List[Product]:
        """
        Получить все продукты.

        Returns:
            List[Product]: Список всех продуктов.
        """
        stmt = select(Product).order_by(Product.id)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Получить список продуктов, у которых остаток меньше указанного порога.

        Args:
            threshold (int, optional): минимальный порог для фильтрации
        Returns:
            List[Product]: Список объектов Product.
        """
        stmt = select(Product).where(Product.quantity < threshold)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update_price_by_name(self, name: str, new_price: Decimal) -> None:
        """
        Обновить цену продукта по имени.

        Args:
            name (str): Имя продукта.
            new_price (Decimal): Новая цена.
        """
        stmt = (
            update(Product)
            .where(Product.name == name)
            .values(price=new_price)
        )
        async with self.db.session() as session:
            await session.execute(stmt)
            await session.commit()

    async def delete_product(self, prod_id: int) -> None:
        """
        Удалить продукт по ID.

        Args:
            prod_id (int): Идентификатор продукта.
        """
        async with self.db.session() as session:
            await session.execute(delete(Product).where(Product.id == prod_id))
            await session.commit()

    def __repr__(self):
        return f"<ProductRepository(db={self.db!r})>"
