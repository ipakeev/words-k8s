import asyncio
import json
import typing

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

from words.logger import logger
from words.schema import MessageToSend

if typing.TYPE_CHECKING:
    from words.accessor import Accessor


class Rabbit:
    connection: AbstractConnection
    channel: AbstractChannel
    exchange: AbstractExchange
    consumer: asyncio.Task

    def __init__(self, accessor: "Accessor"):
        self.accessor = accessor
        self.config = accessor.config.rabbit

    async def connect(self) -> None:
        self.connection = await aio_pika.connect(self.config.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.config.publish_exchange
        )
        self.consumer = asyncio.create_task(self.consume())
        logger.info("connected")

    async def disconnect(self) -> None:
        await self.channel.close()
        await self.connection.close()
        self.consumer.cancel()
        logger.info("disconnected")

    async def publish(self, data: str) -> None:
        msg = aio_pika.Message(body=data.encode(encoding="utf-8"))
        await self.exchange.publish(
            message=msg,
            routing_key=self.config.publish_routing_key,
        )
        logger.debug(f"published msg: {data}")

    async def consume(self) -> None:
        logger.info("started consuming")
        message: aio_pika.abc.AbstractIncomingMessage
        queue = await self.channel.declare_queue(self.config.consume_queue)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    dc = MessageToSend(**data)
                    await self.accessor.bot.send_message(
                        chat_id=dc.chat_id,
                        text=dc.text,
                    )
                    logger.debug(f"received msg: {data}")
        logger.info("stopped consuming")
