import logging


class LoggerConfigurator:
    @staticmethod
    def configure(level=logging.INFO):
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
