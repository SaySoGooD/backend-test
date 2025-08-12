import logging
from typing import List, Tuple, Optional

from src.database.connector import DatabaseConnection


class EmployeeRepository:
    """Репозиторий для работы с сотрудниками в БД"""

    def __init__(self, db_connection: DatabaseConnection):
        self._db = db_connection

    async def initialize(self) -> None:
        """Инициализация таблиц"""
        async with self._db.connection() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    salary INTEGER NOT NULL
                )
            """)
            logging.info("Таблица 'employees' инициализирована или уже существует")

    async def add_employee(self, employee_data: dict) -> None:
        """Добавление нового сотрудника"""
        async with self._db.connection() as conn:
            await conn.execute(
                "INSERT INTO employees (name, position, salary) VALUES ($1, $2, $3)",
                employee_data['name'], employee_data['position'], employee_data['salary']
            )
            logging.info(f"Добавлен сотрудник: {employee_data['name']}, "
                         f"должность: {employee_data['position']}, зарплата: {employee_data['salary']}")

    async def add_employees(self, employees_data: Tuple[Tuple[str, str, int], ...]) -> None:
        """Добавление новых сотрудников"""
        async with self._db.connection() as conn:
            placeholders = []
            values = []
            param_index = 1
            for employee in employees_data:
                placeholders.append(f"(${param_index}, ${param_index+1}, ${param_index+2})")
                values.extend(employee)
                param_index += 3
            query = f"""
                INSERT INTO employees (name, position, salary)
                VALUES {', '.join(placeholders)}
            """
            await conn.execute(query, *values)
            logging.info(f"Добавлено сотрудников: {len(employees_data)}")
