import asyncio
import os

from aiogram import executor

from words.accessor import accessor
from words.config import load_config


async def main() -> None:
    config_file = os.environ.get("CONFIG_FILE", "local/.env")
    config = load_config(config_file)

    await accessor.connect(config)
    executor.start_polling(accessor.dp)


if __name__ == "__main__":
    asyncio.run(main())
