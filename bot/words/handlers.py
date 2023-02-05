import json

from aiogram import Dispatcher, types

from words.accessor import accessor


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(get_word)


async def start_handler(event: types.Message) -> None:
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


async def get_word(event: types.Message) -> None:
    data = json.dumps({"original": event.text})
    await accessor.rabbit.publish(data)
    await event.answer("Перевожу...")
