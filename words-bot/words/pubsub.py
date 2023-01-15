import aio_pika

from words.utils.config import Config, RabbitConfig


class PubSub:
    def __init__(self, config: RabbitConfig):
        self.config = config

    async def connect(self) -> None:
        self.connection = await aio_pika.connect(self.config.build_url())
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


pubsub: PubSub


def init_pubsub(config: Config) -> None:
    global pubsub
    pubsub = PubSub(config.rabbit)
