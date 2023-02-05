import os
from dataclasses import dataclass


@dataclass
class RabbitConfig:
    schema: str = os.environ.get("RABBIT_SCHEMA", "amqp://")
    username: str = os.environ.get("RABBIT_USERNAME", "")
    password: str = os.environ.get("RABBIT_PASSWORD", "")
    host: str = os.environ.get("RABBIT_HOST", "localhost")
    port: int = os.environ.get("RABBIT_PORT", 5672)
    exchange: str = os.environ.get("RABBIT_EXCHANGE", "")
    routing_key: str = os.environ.get("RABBIT_ROUTING_KEY", "")

    @property
    def url(self) -> str:
        credentials = f"{self.username}:{self.password}@" if self.username else ""
        return f"{self.schema}{credentials}{self.host}:{self.port}"


@dataclass
class PostgresConfig:
    username: str = os.environ.get("POSTGRES_USERNAME", "")
    password: str = os.environ.get("POSTGRES_PASSWORD", "")
    host: str = os.environ.get("POSTGRES_HOST", "localhost")
    port: int = os.environ.get("POSTGRES_PORT", 5432)
    db: str = os.environ.get("POSTGRES_DB", "")


@dataclass(init=False)
class Config:
    rabbit: RabbitConfig
    postgres: PostgresConfig

    def __init__(self) -> None:
        self.rabbit = RabbitConfig()
        self.postgres = PostgresConfig()


def load_config() -> Config:
    return Config()
