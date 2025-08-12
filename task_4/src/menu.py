import decimal
from pathlib import Path

from src.setup_logger import decorate_all_methods
from src.services.employee_service import EmployeeService


@decorate_all_methods
class Menu:
    def __init__(self, service: EmployeeService, csv_folder: Path, csv_readed_folder: Path):
        """
        Инициализация меню.

        Args:
            service: сервис для работы с сотрудниками.
            csv_folder: папка с CSV-файлами для загрузки.
            csv_readed_folder: папка для перемещения прочитанных CSV-файлов.
        """
        self.service = service
        self.csv_folder = csv_folder
        self.csv_readed_folder = csv_readed_folder

    async def run(self):
        """
        Основной цикл меню, обрабатывающий ввод пользователя и вызывающий соответствующие действия.
        """
        while True:
            self.print_main_menu()
            choice = input("Введите номер действия: ").strip().upper()
            print()

            if choice == "A":
                await self.load_csv()

            elif choice == "B":
                await self.list_employees()

            elif choice == "C":
                await self.select_employee_by_id()

            elif choice == "D":
                await self.search_employee_by_name()

            elif choice == "F":
                await self.search_employee_by_position()

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор, попробуйте снова.")

    def print_main_menu(self):
        """
        Выводит главное меню с доступными действиями.
        """
        print("\nВыберите действие:")
        print("A. Загрузить все CSV из папки")
        print("B. Показать список сотрудников")
        print("C. Выбрать сотрудника по ID")
        print("D. Поиск сотрудника по имени")
        print("F. Поиск сотрудника по специальности")
        print("0. Выход")

    async def load_csv(self):
        """
        Загружает все CSV-файлы из папки в базу и перемещает их в папку прочитанных.
        """
        await self.service.load_all_csv_from_folder(
            source_folder=self.csv_folder,
            readed_folder=self.csv_readed_folder
        )
        print("CSV-файлы загружены в базу и перемещены.")

    async def list_employees(self):
        """
        Показывает постраничный список сотрудников и предоставляет дополнительные действия.
        """
        page = 1
        per_page = 10
        while True:
            await self.service.list_employees_page(page=page, per_page=per_page)
            print("\nA. Выбрать сотрудника по ID")
            print("B. Поиск сотрудника по имени")
            print("C. Поиск сотрудника по специальности")
            print("0. В меню")
            sub_choice = input("Введите страницу или действие: ").strip().upper()

            if sub_choice == "A":
                await self.select_employee_by_id()
            elif sub_choice == "B":
                await self.search_employee_by_name()
            elif sub_choice == "C":
                await self.search_employee_by_position()
            elif sub_choice == "0":
                break
            elif sub_choice.isdigit():
                page = int(sub_choice)
            else:
                print("Неверный выбор, попробуйте снова.")

    async def select_employee_by_id(self):
        """
        Позволяет выбрать сотрудника по ID и выполнить с ним действия: изменить зарплату или удалить.
        """
        try:
            emp_id = int(input("Введите ID сотрудника: "))
        except ValueError:
            print("Неверный ввод ID.")
            return

        emp = await self.service.get_employee_by_id(emp_id)
        if not emp:
            print("Сотрудник не найден.")
            return

        print(emp)

        while True:
            print("\nA. Изменить зарплату")
            print("B. Удалить сотрудника")
            print("0. В меню")
            action = input("Выберите действие: ").strip().upper()
            print()

            if action == "A":
                await self.change_salary(emp_id)
            elif action == "B":
                if await self.delete_employee(emp_id):
                    break
            elif action == "0":
                break
            else:
                print("Неверный выбор, попробуйте снова.")

    async def change_salary(self, emp_id: int):
        """
        Изменяет зарплату сотрудника с указанным ID.

        Args:
            emp_id: ID сотрудника.
        """
        new_salary_str = input("Введите новую зарплату (например, 12345.67): ").strip()
        print()
        try:
            new_salary = decimal.Decimal(new_salary_str).quantize(decimal.Decimal('0.01'))
        except decimal.InvalidOperation:
            print("Неверный формат зарплаты. Попробуйте снова.")
            return

        success = await self.service.update_employee_salary(emp_id, new_salary)
        if success:
            print(f"Зарплата сотрудника с ID {emp_id} обновлена на {new_salary:.2f}.")
            emp = await self.service.get_employee_by_id(emp_id)
            print(emp)
        else:
            print("Не удалось обновить зарплату.")

    async def delete_employee(self, emp_id: int) -> bool:
        """
        Удаляет сотрудника после подтверждения.

        Args:
            emp_id: ID сотрудника.

        Returns:
            True, если сотрудник удалён, иначе False.
        """
        confirm = input(f"Вы действительно хотите удалить сотрудника с ID {emp_id}? (да/нет): ").strip().lower()
        print()
        if confirm == "да":
            await self.service.delete_employee(emp_id)
            print(f"Сотрудник с ID {emp_id} удалён.")
            return True
        else:
            print("Удаление отменено.")
            return False

    async def search_employee_by_name(self):
        """
        Выполняет поиск сотрудников по имени (или части имени) и выводит результаты.
        """
        name = input("Введите имя (или часть имени): ")
        print()
        results = await self.service.search_employees_by_name(name)
        if results:
            for emp in results:
                print(emp)
        else:
            print("Сотрудники не найдены.")

    async def search_employee_by_position(self):
        """
        Выполняет поиск сотрудников по должности (или части должности) и выводит результаты.

        Также выводит список всех доступных профессий.
        """
        positions = await self.service.repository.get_all_positions()
        print(f"\nВот список всех профессий: {positions}\n")
        position = input("Введите должность (или часть должности): ")
        print()
        results = await self.service.repository.find_employees_by_position(position.lower())
        if results:
            print("\nНайденные сотрудники:")
            for emp in results:
                print(emp)
        else:
            print("Сотрудники не найдены.")

    def __repr__(self):
        return (f"<Menu(service={self.service!r}, "
                f"csv_folder={self.csv_folder!r}, "
                f"csv_readed_folder={self.csv_readed_folder!r})>")
