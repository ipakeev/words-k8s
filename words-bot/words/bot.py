import asyncio

from aiogram import Bot, Dispatcher

from words.pubsub import init_pubsub
from words.utils.config import Config, load_config


async def _connect():
    from words.pubsub import pubsub
    await pubsub.connect()


def init_bot(config: Config | None = None) -> Dispatcher:
    config = config or load_config()
    init_pubsub(config)

    from words.handlers import register_handlers
    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot)
    register_handlers(dp)
    asyncio.get_event_loop().create_task(_connect())
    return dp
