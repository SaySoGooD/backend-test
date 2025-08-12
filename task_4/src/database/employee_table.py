from decimal import Decimal

from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import mapped_column, Mapped

from src.database.connector import Base


class Employee(Base):
    """Таблица с сотрудниками"""

    __tablename__ = "csv_employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Position: {self.position}\n"
                f"Salary: {float(self.salary):.2f}")
