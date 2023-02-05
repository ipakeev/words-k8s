import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str = os.environ.get("BOT_TOKEN", "")


@dataclass
class RabbitConfig:
    schema: str = os.environ.get("RABBIT_SCHEMA", "amqp://")
    username: str = os.environ.get("RABBIT_USERNAME", "")
    password: str = os.environ.get("RABBIT_PASSWORD", "")
    host: str = os.environ.get("RABBIT_HOST", "localhost")
    port: str = os.environ.get("RABBIT_PORT", "5672")
    exchange: str = os.environ.get("RABBIT_EXCHANGE", "")
    routing_key: str = os.environ.get("RABBIT_ROUTING_KEY", "")

    @property
    def url(self) -> str:
        credentials = f"{self.username}:{self.password}@" if self.username else ""
        return f"{self.schema}{credentials}{self.host}:{self.port}"


@dataclass(init=False)
class Config:
    bot: BotConfig
    rabbit: RabbitConfig

    def __init__(self) -> None:
        self.bot = BotConfig()
        self.rabbit = RabbitConfig()


def load_config(config_file: str) -> Config:
    load_dotenv(config_file)
    return Config()
