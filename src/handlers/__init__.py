from aiogram import Dispatcher

from .commands import start, help, about
from .registration import enter_name, find_name
from .menu import today, tomorrow, week

from src.misc.states import BotStates


__all__ = ["register_all_handlers"]


def register_all_handlers(dp: Dispatcher):

    # Commands
    dp.register_message_handler(start, state="*", commands=["start"])
    dp.register_message_handler(help, state="*", commands=["help"])
    dp.register_message_handler(about, state="*", commands=["about"])

    # Registration
    dp.register_message_handler(enter_name, state=BotStates.who_is_user_state)
    dp.register_message_handler(find_name, state=BotStates.enter_name_state)

    # Menu
    dp.register_message_handler(
        today,
        state=BotStates.menu_state,
        text="Сегодня"
    )

    dp.register_message_handler(
        tomorrow,
        state=BotStates.menu_state,
        text="Завтра"
    )

    dp.register_message_handler(
        week,
        state=BotStates.menu_state,
        text="Неделя"
    )
