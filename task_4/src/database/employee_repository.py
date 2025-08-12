from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy import delete, func
from src.database.employee_table import Employee
from src.database.connector import DatabaseConnection
from src.setup_logger import decorate_all_methods


@decorate_all_methods
class EmployeeRepository:
    """Репозиторий для работы с сущностью Employee."""

    def __init__(self, db: DatabaseConnection):
        """
        Инициализация репозитория.

        Args:
            db: объект DatabaseConnection, предоставляет метод session().
        """
        self.db = db

    async def insert_employees(self, employees: List[Employee]) -> None:
        """
        Вставить список сотрудников в базу.

        Выполняет вставку всех переданных объектов Employee в одной транзакции.

        Args:
            employees: список объектов Employee для вставки.

        Raises:
            Любые исключения, проброшенные SQLAlchemy при выполнении операции.
        """
        async with self.db.session() as session:
            session.add_all(employees)
            await session.commit()

    async def get_employees_page(self, page: int, per_page: int = 10) -> List[Employee]:
        """
        Получить страницу сотрудников (пагинация).

        Args:
            page: номер страницы (1-based).
            per_page: количество записей на страницу.

        Returns:
            Список объектов Employee для указанной страницы (возможно пустой).
        """
        offset = (page - 1) * per_page
        stmt = (
            select(Employee)
            .order_by(Employee.id)
            .limit(per_page)
            .offset(offset)
        )
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        """
        Получить сотрудника по ID.

        Args:
            emp_id: идентификатор сотрудника.

        Returns:
            Объект Employee при найденном сотруднике, иначе None.
        """
        stmt = select(Employee).where(Employee.id == emp_id)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    async def find_employees_by_name(self, name: str) -> List[Employee]:
        """
        Поиск сотрудников по имени (частичное совпадение, регистр игнорируется).

        Args:
            name: строка для поиска в имени (может быть частью имени).

        Returns:
            Список подходящих объектов Employee.
        """
        stmt = (
            select(Employee)
            .where(func.lower(Employee.name).like(f"%{name.lower()}%"))
            .order_by(Employee.id)
        )
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def find_employees_by_position(self, position: str) -> List[Employee]:
        """
        Поиск сотрудников по должности (частичное совпадение, регистр игнорируется).

        Args:
            position: строка для поиска в поле position (может быть частью названия должности).

        Returns:
            Список подходящих объектов Employee.
        """
        stmt = (
            select(Employee)
            .where(func.lower(Employee.position).like(f"%{position.lower()}%"))
            .order_by(Employee.id)
        )
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_all_positions(self) -> List[str]:
        """
        Получить список всех уникальных должностей.

        Returns:
            Отсортированный список уникальных значений поля position (строки).
        """
        stmt = select(Employee.position).distinct().order_by(Employee.position)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return [row[0] for row in result.all()]

    async def count_employees(self) -> int:
        """
        Подсчитать общее количество сотрудников в таблице.

        Returns:
            Общее количество записей (int).
        """
        stmt = select(func.count()).select_from(Employee)
        async with self.db.session() as session:
            result = await session.execute(stmt)
            return result.scalar_one()

    async def insert_employee(self, employee: Employee) -> None:
        """
        Вставить одного сотрудника.

        Args:
            employee: объект Employee для вставки.
        """
        async with self.db.session() as session:
            session.add(employee)
            await session.commit()

    async def update_employee(self, employee: Employee):
        """
        Обновить (merge) существующего сотрудника.

        Args:
            employee: объект Employee с заполненным id и новыми значениями.

        Notes:
            Используется session.merge(), затем commit().
        """
        async with self.db.session() as session:
            await session.merge(employee)
            await session.commit()

    async def delete_employee(self, emp_id: int):
        """
        Удалить сотрудника по ID.

        Args:
            emp_id: идентификатор сотрудника для удаления.
        """
        async with self.db.session() as session:
            await session.execute(delete(Employee).where(Employee.id == emp_id))
            await session.commit()

    def __repr__(self):
        return f"<EmployeeRepository(db={self.db!r})>"
