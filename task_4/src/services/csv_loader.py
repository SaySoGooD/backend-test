import csv
from pathlib import Path
from typing import AsyncGenerator, List
from decimal import Decimal

from src.database.employee_table import Employee
from src.setup_logger import decorate_all_methods


@decorate_all_methods
class EmployeeCSVLoader:
    def __init__(self, batch_size: int = 1000):
        """
        Инициализация загрузчика CSV.

        Args:
            batch_size: количество сотрудников в одном батче при загрузке.
        """
        self.batch_size = batch_size

    async def load_employees_from_csv(self, csv_file: Path) -> AsyncGenerator[List[Employee], None]:
        """
        Асинхронно загружает сотрудников из CSV-файла по батчам.

        Args:
            csv_file: путь к CSV-файлу с данными сотрудников.

        Returns:
            AsyncGenerator, выдающий списки Employee размером batch_size или меньше.
        """
        batch: List[Employee] = []
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                employee = Employee(
                    name=row["name"],
                    position=row["position"],
                    salary=Decimal(row["salary"])
                )
                batch.append(employee)
                if len(batch) >= self.batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    def __repr__(self):
        return f"<EmployeeCSVLoader(batch_size={self.batch_size})>"
