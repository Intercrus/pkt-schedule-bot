import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from environs import Env

from src.handlers.commands import register_commands_handlers
from src.handlers.user_registration import register_user_registration_handlers
from src.handlers.main_menu import register_main_menu_handlers

from src.misc.get_schedule import update_schedule_cache


env = Env()
env.read_env(".env")
env.str("BOT_TOKEN")


def register_all_handlers(dp):
    register_commands_handlers(dp)
    register_user_registration_handlers(dp)
    register_main_menu_handlers(dp)


async def main():
    bot = Bot(token=env.str("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    scheduler = AsyncIOScheduler()
    await update_schedule_cache()
    scheduler.add_job(update_schedule_cache, "cron", day="*", hour="5,13-20")
    scheduler.start()

    register_all_handlers(dp)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
