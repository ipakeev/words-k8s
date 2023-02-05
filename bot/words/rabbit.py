import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

from words.config import Config


class Rabbit:
    connection: AbstractConnection
    channel: AbstractChannel
    exchange: AbstractExchange

    def __init__(self, config: Config):
        self.config = config.rabbit

    async def connect(self) -> None:
        self.connection = await aio_pika.connect(self.config.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(self.config.exchange)
        print("connected")

    async def disconnect(self) -> None:
        await self.channel.close()
        await self.connection.close()

    async def publish(self, data: str) -> None:
        msg = aio_pika.Message(body=data.encode(encoding="utf-8"))
        await self.exchange.publish(
            message=msg,
            routing_key=self.config.routing_key,
        )
        print(f"published msg: {data}")
