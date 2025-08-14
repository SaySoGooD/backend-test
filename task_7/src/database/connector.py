from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config_model import DatabaseConfig
from src.setup_logger import class_logger


@class_logger
class DatabaseConnection:
    """Класс для управления подключением к БД с SQLAlchemy Async"""

    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._engine = create_async_engine(self._config.dsn, echo=False)
        self._async_session_maker: Optional[sessionmaker] = None

    async def connect(self) -> None:
        """Инициализация engine и session maker"""
        self._async_session_maker = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )
        try:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            raise e

    async def close(self) -> None:
        """Закрываем engine"""
        await self._engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Контекстный менеджер для получения сессии"""
        if not self._async_session_maker:
            raise RuntimeError("Session maker не инициализирован. Вызовите connect() сначала.")

        async_session = self._async_session_maker()
        try:
            yield async_session
            await async_session.commit()
        except Exception as e:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()

    def __repr__(self):
        return f"<DatabaseConnection(id={id(self)})>"


Base = declarative_base()
