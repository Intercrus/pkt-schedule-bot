import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config

from handlers import register_all_handlers

from misc.anti_flood import ThrottlingMiddleware
from misc.get_schedule import update_schedule_cache


async def main() -> None:
    bot = Bot(token=config.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=RedisStorage2(db=1))

    # Anti-flood
    dp.middleware.setup(ThrottlingMiddleware())

    # Register handlers
    register_all_handlers(dp)

    # Cache update
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(update_schedule_cache, "cron", day="*", hour="6,13-21")
    scheduler.start()

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
