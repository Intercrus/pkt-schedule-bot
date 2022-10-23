import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from environs import Env

from src.handlers.user_registration import register_user_registration_handlers
from src.handlers.main_menu import register_main_menu_handlers


env = Env()
env.read_env(".env")
env.str("BOT_TOKEN")


def register_all_handlers(dp):
    register_user_registration_handlers(dp)
    register_main_menu_handlers(dp)


async def main():
    bot = Bot(token=env.str("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
