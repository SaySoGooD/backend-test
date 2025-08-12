from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"