import os
import pathlib
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class BotConfig:
    token: str = ""


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
        if self.username:
            credentials = f"{self.username}:{self.password}@"
        else:
            credentials = ""
        return os.environ.get(
            "RABBIT_URL",
            f"{self.schema}{credentials}{self.host}:{self.port}",
        )


@dataclass(init=False)
class Config:
    bot: BotConfig
    rabbit: RabbitConfig

    def __init__(self, config: dict) -> None:
        self.bot = BotConfig(**config.get("words-bot", {}))
        self.rabbit = RabbitConfig(**config.get("rabbit", {}))


def _load_yaml(filename: str | pathlib.Path) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
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
