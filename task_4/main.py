import asyncio
from src.config_model import DatabaseConfig
from src.database.connector import DatabaseConnection
from src.database.employee_repository import EmployeeRepository
from src.services.csv_loader import EmployeeCSVLoader
from src.services.employee_service import EmployeeService
from src.menu import Menu
from pathlib import Path
import logging
from src.setup_logger import configure

BASE_DIR = Path(__file__).resolve().parent
CSV_FOLDER = BASE_DIR / "csv_folder"
CSV_READED_FOLDER = BASE_DIR / "csv_readed_folder"


async def main(config):
    """
    Основная асинхронная функция запуска приложения.

    Производит подключение к базе данных, создание репозитория, загрузчика и сервиса,
    затем запускает интерактивное меню. В конце закрывает соединение с базой данных.

    Args:
        config (DatabaseConfig): Конфигурация подключения к базе данных.
    """
    db = DatabaseConnection(config)
    try:
        await db.connect()
    except Exception as e:
        raise e
    try:
        repo = EmployeeRepository(db)
        loader = EmployeeCSVLoader()
        service = EmployeeService(repo, loader)

        menu = Menu(service, CSV_FOLDER, CSV_READED_FOLDER)
        await menu.run()
    finally:
        await db.close()


if __name__ == "__main__":
    """
    Точка входа в приложение.

    Настраивает логирование, создаёт конфигурацию базы данных и запускает
    асинхронную функцию main.
    """
    configure(logging.INFO)
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        user="postgres",
        password="AV123",
        database="employees"
    )
    asyncio.run(main(config))
