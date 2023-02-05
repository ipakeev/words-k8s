import typing

from aiogram import Bot, Dispatcher

from words.config import Config

if typing.TYPE_CHECKING:
    from words.rabbit import Rabbit


class Accessor:
    config: Config
    bot: Bot
    dp: Dispatcher
    rabbit: "Rabbit"

    async def connect(self, config: Config) -> None:
        from words.handlers import register_handlers
        from words.rabbit import Rabbit

        self.config = config

        self.bot = Bot(token=config.bot.token)
        self.dp = Dispatcher(self.bot)
        register_handlers(self.dp)

        self.rabbit = Rabbit(config)
        await self.rabbit.connect()

    async def disconnect(self) -> None:
        self.dp.stop_polling()
        await self.dp.wait_closed()
        await self.rabbit.disconnect()


accessor = Accessor()
