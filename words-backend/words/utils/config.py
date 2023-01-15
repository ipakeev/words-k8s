import os
import pathlib
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class RabbitConfig:
    schema: str = "amqp://"
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 5672
    exchange: str = ""
    routing_key: str = ""

    def build_url(self) -> str:
        credentials = f"{self.username}:{self.password}@" if self.username else ""
        return os.environ.get(
            "RABBIT_URL",
            f"{self.schema}{credentials}{self.host}:{self.port}",
        )


@dataclass(frozen=True)
class PostgresConfig:
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 5432
    db: str = ""

    def build_url(self) -> str:
        pass


@dataclass(init=False)
class Config:
    rabbit: RabbitConfig
    postgres: PostgresConfig

    def __init__(self, config: dict) -> None:
        self.rabbit = RabbitConfig(**config.get("rabbit", {}))
        self.postgres = PostgresConfig(**config.get("postgres", {}))


def _load_yaml(filename: str | pathlib.Path) -> dict:
    with open(filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(filename: str | pathlib.Path | None = None) -> Config:
    if filename is None:
        try:
            config = _load_yaml("etc/local.yml")
        except FileNotFoundError:
            config = _load_yaml("config/config.yml")
    else:
        config = _load_yaml(filename)
    return Config(config)
