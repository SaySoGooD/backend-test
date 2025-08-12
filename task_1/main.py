import sys
import asyncio
from typing import Optional

from src.config_models import DatabaseConfig
from src.database.connector import DatabaseConnection
from src.database.employee_repository import EmployeeRepository
from src.logger_setup import LoggerConfigurator

LoggerConfigurator.configure()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_script(config: DatabaseConfig, new_employee: Optional[dict] = None,
                       new_employees: Optional[tuple] = None, min_salary: int = 0, max_salary: int = 900000):
    """Точка входа в скрипт"""

    db_connection = DatabaseConnection(config)
    await db_connection.connect()

    try:
        repo = EmployeeRepository(db_connection)
        await repo.initialize()

        if new_employees:
            await repo.add_employees(new_employees)

        if new_employee:
            await repo.add_employee(new_employee)

        employees = await repo.get_by_salary_range(min_salary, max_salary)
        for emp in employees:
            print(emp)

        employee = await repo.get_by_name('Иван')
        print('До обновления зарплаты:', employee)

        await repo.update_salary_by_name({"name": "Иван", "salary": 60000})

        employee = await repo.get_by_name('Иван')
        print('После обновления зарплаты:', employee)

        employee = await repo.get_by_name('Анна')
        print('Да удаления:', employee)

        employee = await repo.delete_by_name("Анна")
        print('После:', employee)
    finally:
        await db_connection.close()


if __name__ == "__main__":
    # Добавление одного сотрудника
    new_employee = {
        "name": "Иван Петров",
        "position": "Инженер",
        "salary": 85000
    }
    # Добавление 5 сотрудников
    new_employees = (
        ("Иван", "Разработчик", 155000),
        ("Анна", "Аналитик", 52000),
        ("Петр", "Тестировщик", 48000),
        ("Мария", "Менеджер", 20000),
        ("Сергей", "Дизайнер", 25000),
    )
    # Суммы для фильтра
    min_salary = 50000
    max_salary = 0
    # Конфиг ДБ (можно вынести в .env или config.ini)
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        user="postgres",
        password="AV123",
        database="employees"
    )
    asyncio.run(start_script(config, new_employee, new_employees))
