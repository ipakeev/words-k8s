import typing

from aiogram import Bot, Dispatcher

from words.config import Config
from words.logger import logger

if typing.TYPE_CHECKING:
    from words.rabbit import Rabbit


class Accessor:
    config: Config
    bot: Bot
    dp: Dispatcher
    rabbit: "Rabbit"

    async def connect(self, config: Config) -> None:
        logger.info("connecting...")
        from words.handlers import register_handlers
        from words.rabbit import Rabbit

        self.config = config

        self.bot = Bot(token=config.bot.token)
        self.dp = Dispatcher(self.bot)
        register_handlers(self.dp)

        self.rabbit = Rabbit(self)
        await self.rabbit.connect()
        logger.info("connected")

    async def disconnect(self) -> None:
        logger.info("disconnecting...")
        self.dp.stop_polling()
        await self.dp.wait_closed()
        await self.rabbit.disconnect()
        logger.info("disconnected")


accessor = Accessor()
