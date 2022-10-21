from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.states.bot_states import BotStates


async def today(message: Message, state: FSMContext):
    pass


async def tomorrow(message: Message, state: FSMContext):
    pass


async def week(message: Message, state: FSMContext):
    pass


def register_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(
        today,
        state=BotStates.main_menu_state,
        text="Сегодня"
    )

    dp.register_message_handler(
        tomorrow,
        state=BotStates.main_menu_state,
        text="Завтра"
    )

    dp.register_message_handler(
        week,
        state=BotStates.main_menu_state,
        text="Неделя"
    )
