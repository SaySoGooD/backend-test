import logging
import asyncio
import functools
import inspect


def configure(level=logging.DEBUG):
    """
    Настраивает базовую конфигурацию логирования с указанным уровнем.

    Args:
        level (int, optional): Уровень логирования (например, logging.DEBUG). По умолчанию logging.DEBUG.
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def decorate_all_methods(cls):
    """
    Декорирует все методы класса логирующим декоратором `log_method_call`, кроме метода `__repr__`.

    Args:
        cls (type): Класс для декорирования.

    Returns:
        type: Класс с задекорированными методами.
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and attr_name != '__repr__':
            decorated = log_method_call(attr_value)
            setattr(cls, attr_name, decorated)
    return cls


class Logger:
    """
    Обёртка над стандартным модулем logging для удобства вызова методов логирования.
    """

    def __init__(self, name: str = __name__):
        """
        Инициализация логгера с заданным именем.

        Args:
            name (str): Имя логгера. По умолчанию используется имя текущего модуля.
        """
        self.logger = logging.getLogger(name)

    def debug(self, msg: str):
        """Логирует сообщение с уровнем DEBUG."""
        self.logger.debug(msg)

    def info(self, msg: str):
        """Логирует сообщение с уровнем INFO."""
        self.logger.info(msg)

    def warning(self, msg: str):
        """Логирует сообщение с уровнем WARNING."""
        self.logger.warning(msg)

    def error(self, msg: str):
        """Логирует сообщение с уровнем ERROR."""
        self.logger.error(msg)

    def critical(self, msg: str):
        """Логирует сообщение с уровнем CRITICAL."""
        self.logger.critical(msg)


log = Logger(__name__)


def log_method_call(func):
    """
    Декоратор, логирующий вызовы функции или асинхронной корутины.

    Логирует имя класса, имя метода и аргументы вызова, а также факт завершения метода.

    Args:
        func (callable): Функция или корутина для декорирования.

    Returns:
        callable: Обёртка вокруг исходной функции с логированием.
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            cls_name = args[0].__class__.__name__
            func_name = func.__name__
            params = inspect.signature(func).bind(*args, **kwargs)
            params.apply_defaults()
            params.arguments.pop('self', None)
            log.debug(f"{cls_name}.{func_name} вызвано с args={params.arguments}")
            result = await func(*args, **kwargs)
            log.debug(f"{cls_name}.{func_name} завершено")
            return result

        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            cls_name = args[0].__class__.__name__
            func_name = func.__name__
            params = inspect.signature(func).bind(*args, **kwargs)
            params.apply_defaults()
            params.arguments.pop('self', None)
            log.debug(f"{cls_name}.{func_name} вызвано с args={params.arguments}")
            result = func(*args, **kwargs)
            log.debug(f"{cls_name}.{func_name} завершено")
            return result

        return sync_wrapper
