from aiogram import executor

from words.bot import init_bot


def main() -> None:
    dp = init_bot()
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
