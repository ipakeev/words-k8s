import json
from collections.abc import Callable
from functools import wraps
from typing import Any

from aiogram import Dispatcher, types

from words.accessor import accessor
from words.logger import logger


def log_msg(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(event: types.Message, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"from: {event.from_user.full_name}, msg: {event.text}")
        return await func(event, *args, **kwargs)

    return wrapper


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(get_word)


@log_msg
async def start_handler(event: types.Message) -> None:
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


@log_msg
async def get_word(event: types.Message) -> None:
    data = json.dumps({"original": event.text})
    await accessor.rabbit.publish(data)
    await event.answer("Перевожу...")
