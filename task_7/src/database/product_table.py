from decimal import Decimal
from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from src.database.connector import Base


class Product(Base):
    """Модель продукта."""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"
