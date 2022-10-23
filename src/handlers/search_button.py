from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from datetime import datetime, timedelta

from src.states.bot_states import BotStates

from src.misc.full_names import groups, teachers, days

from src.misc.get_schedule.py import CACHE

from src.keyboards.search_keyboard import search
from src.keyboards.main_menu_keyboard import main_menu


async def search_by(message: Message, state: FSMContext):
    await message.answer("Поиск", reply_markup=search)
    await state.set_state(BotStates.search_by_state)


async def enter_desired_group(message: Message, state: FSMContext):
    await message.answer("Введите название группы,\nрасписание которой нужно найти\n"
                         "Например, 111бд или 209ЗМ-3")
    await state.set_state(BotStates.search_by_group_state)


async def enter_desired_teacher(message: Message, state: FSMContext):
    await message.answer(
        "Введите имя преподавателя,\nрасписание которого нужно найти\n"
        "Например, Опуховская или соколов")
    await state.set_state(BotStates.search_by_teacher_state)


async def search_by_group(message: Message, state: FSMContext):
    today_day = datetime.today().strftime("%A")
    today_date = datetime.today().strftime("%d.%m.%Y")

    group = message.text.upper()

    schedule_is_not_empty = True

    if message.text == "Назад":
        await back_from_search(message, state)
    else:
        if group in groups:
            try:
                schedule = CACHE[today_date]["groups"][group]
            except KeyError:
                schedule = f"На дату {today_date} расписание не добавлено"
                schedule_is_not_empty = False

            if schedule_is_not_empty:
                schedule = "\n".join(schedule)

            if schedule:
                await message.answer(
                    f"<pre>{days[today_day]}, {today_date}</pre>\n"
                    f"{schedule}")
            else:
                await message.answer(f"У группы {group} сегодня нет пар")

            await state.set_state(BotStates.search_by_state)
        else:
            await message.answer("Группа не найдена ❌\n"
                                 "Возможно, вы ошиблись в написании группы")


async def search_by_teacher(message: Message, state: FSMContext):
    today_day = datetime.today().strftime("%A")
    today_date = datetime.today().strftime("%d.%m.%Y")

    teacher = message.text.capitalize()

    schedule_is_not_empty = True

    if message.text == "Назад":
        await back_from_search(message, state)
    else:
        if teachers.get(teacher) is not None:
            try:
                schedule = CACHE[today_date]["teachers"][teacher]
            except KeyError:
                schedule = f"На дату {today_date} расписание не добавлено"
                schedule_is_not_empty = False

            if schedule_is_not_empty:
                schedule = "\n".join(schedule)

            if schedule:
                await message.answer(
                    f"<pre>{days[today_day]}, {today_date}</pre>\n"
                    f"{schedule}")
            else:
                await message.answer(f"У преподавателя {teachers.get(teacher)} сегодня нет пар")

            await state.set_state(BotStates.search_by_state)
        else:
            await message.answer("Преподаватель не найден ❌\n"
                                 "Возможно, вы ошиблись в написании фамилии")


async def back_from_search(message: Message, state: FSMContext):
    await message.answer("Меню", reply_markup=main_menu)
    await state.set_state(BotStates.main_menu_state)


def register_search_button_handlers(dp: Dispatcher):
    dp.register_message_handler(search_by, state=BotStates.main_menu_state, text="Поиск")

    dp.register_message_handler(enter_desired_group, state=BotStates.search_by_state, text="Группа")
    dp.register_message_handler(enter_desired_teacher, state=BotStates.search_by_state, text="Преподаватель")

    dp.register_message_handler(search_by_group, state=BotStates.search_by_group_state)
    dp.register_message_handler(search_by_teacher, state=BotStates.search_by_teacher_state)

    dp.register_message_handler(back_from_search, state=BotStates.search_by_state, text="Назад")
    