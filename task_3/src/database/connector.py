from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
import asyncpg

from src.config_model import DatabaseConfig


class DatabaseConnection:
    """Класс для управления подключением к БД с asyncpg"""

    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Устанавливает соединение с БД"""
        self._pool = await asyncpg.create_pool(self._config.dsn)

    async def close(self) -> None:
        """Закрывает соединение с БД"""
        if self._pool:
            await self._pool.close()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[asyncpg.Connection]:
        """
        Контекстный менеджер для работы с соединением из пула.
        """
        if not self._pool:
            raise RuntimeError("Connection pool is not initialized")

        async with self._pool.acquire() as conn:
            yield conn
