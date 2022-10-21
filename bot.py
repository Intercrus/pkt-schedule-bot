import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from environs import Env

from src.handlers.user_registration import register_user_registration_handlers


env = Env()
env.read_env(".env")


def register_all_handlers(dp):
    register_user_registration_handlers(dp)


async def main():
    bot = Bot(token=env.str("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
