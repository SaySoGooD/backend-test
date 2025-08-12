from pathlib import Path
import shutil
from typing import List, Tuple

from src.services.table_formatter import TableFormatter
from src.database.employee_table import Employee
from src.services.csv_loader import EmployeeCSVLoader
from src.database.employee_repository import EmployeeRepository
from src.setup_logger import decorate_all_methods


@decorate_all_methods
class EmployeeService:
    def __init__(self, repository: EmployeeRepository, csv_loader: EmployeeCSVLoader):
        """
        Инициализация сервиса сотрудников.

        Args:
            repository: репозиторий для работы с БД сотрудников.
            csv_loader: загрузчик сотрудников из CSV-файлов.
        """
        self.repository = repository
        self.csv_loader = csv_loader

    async def load_all_csv_from_folder(self, source_folder: Path, readed_folder: Path) -> None:
        """
        Загружает всех сотрудников из CSV-файлов в папке и перемещает файлы в папку прочитанных.

        Args:
            source_folder: папка с CSV-файлами для загрузки.
            readed_folder: папка для перемещения обработанных CSV-файлов.
        """
        source_folder.mkdir(exist_ok=True)
        readed_folder.mkdir(exist_ok=True)

        for csv_file in source_folder.glob("*.csv"):
            async for batch in self.csv_loader.load_employees_from_csv(csv_file):
                await self.repository.insert_employees(batch)
            shutil.move(str(csv_file), readed_folder / csv_file.name)

    async def list_employees_page(self, page: int = 1, per_page: int = 10) -> tuple[int, int]:
        """
        Выводит таблицу сотрудников по странице с пагинацией.

        Args:
            page: номер страницы (начиная с 1).
            per_page: количество сотрудников на странице.

        Returns:
            Кортеж (текущая_страница, общее_число_страниц).
        """
        employees = await self.repository.get_employees_page(page, per_page)
        total_employees = await self.repository.count_employees()
        total_pages = (total_employees + per_page - 1) // per_page if per_page else 1
        if page > total_pages:
            print(f"Страница {page} отсутствует. Всего страниц: {total_pages}")
            return total_pages, total_pages
        headers = ["id", "Name", "Position", "Salary"]
        rows = [
            [str(emp.id), emp.name, emp.position, f"{emp.salary:.2f}"]
            for emp in employees
        ]

        formatter = TableFormatter(headers, rows)
        await formatter.print_table()
        print(f"\nВсего страниц: {page}/{total_pages}")

        return page, total_pages

    async def get_employee_by_id(self, emp_id: int) -> Employee | None:
        """
        Получить сотрудника по ID.

        Args:
            emp_id: ID сотрудника.

        Returns:
            Объект Employee или None, если не найден.
        """
        return await self.repository.get_employee_by_id(emp_id)

    async def search_employees_by_name(self, name: str) -> List[Employee]:
        """
        Поиск сотрудников по имени (частичное совпадение, без учёта регистра).

        Args:
            name: имя для поиска.

        Returns:
            Список сотрудников, подходящих под критерий.
        """
        return await self.repository.find_employees_by_name(name.lower())

    async def search_employees_by_position(self, position: str) -> Tuple:
        """
        Поиск сотрудников по позиции (частичное совпадение, без учёта регистра) и получение всех позиций.

        Args:
            position: позиция для поиска.

        Returns:
            Кортеж (список сотрудников по позиции, список всех уникальных позиций).
        """
        employees = await self.repository.find_employees_by_position(position.lower())
        positions_list = await self.repository.get_all_positions()
        return employees, positions_list

    async def update_employee_salary(self, emp_id: int, new_salary: float) -> bool:
        """
        Обновление зарплаты сотрудника.

        Args:
            emp_id: ID сотрудника.
            new_salary: новая зарплата.

        Returns:
            True, если сотрудник найден и обновлён, иначе False.
        """
        employee = await self.repository.get_employee_by_id(emp_id)
        if employee:
            employee.salary = new_salary
            await self.repository.update_employee(employee)
            return True
        return False

    async def delete_employee(self, emp_id: int) -> None:
        """
        Удаление сотрудника по ID.

        Args:
            emp_id: ID сотрудника.
        """
        await self.repository.delete_employee(emp_id)

    def __repr__(self):
        return (f"<EmployeeService(repository={repr(self.repository)}, "
                f"csv_loader={repr(self.csv_loader)})>")
