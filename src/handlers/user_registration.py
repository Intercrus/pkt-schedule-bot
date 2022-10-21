from aiogram import Dispatcher
from aiogram.types import Message


async def start(message: Message):
    await message.answer(f"-")


def register_user_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(start, state="*", commands=["start"])
