from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.states.bot_states import BotStates
from src.misc.full_names import days
from src.misc.get_schedule import CACHE

from datetime import datetime, timedelta


async def today(message: Message, state: FSMContext):
    data = await state.get_data()

    day = datetime.today().strftime("%A")
    date = datetime.today().strftime("%d.%m.%Y")

    schedule = []
    schedule_is_not_empty = True

    if day == "Sunday":
        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"Выходной"
        )
    else:
        try:
            if data["who_is_user"] == "Студент":
                schedule = CACHE[date]["groups"][data["group"]]

            elif data["who_is_user"] == "Преподаватель":
                schedule = CACHE[date]["teachers"][data["teacher"]]
        except KeyError:
            schedule = "Выходной"
            schedule_is_not_empty = False

        if schedule_is_not_empty:
            schedule = "\n".join(schedule)

        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"{schedule}"
        )


async def tomorrow(message: Message, state: FSMContext):
    data = await state.get_data()

    day = (datetime.today() + timedelta(days=1)).strftime("%A")
    date = (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")

    schedule = []
    schedule_is_not_empty = True

    if day == "Sunday":
        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"Выходной"
        )
    else:
        try:
            if data["who_is_user"] == "Студент":
                schedule = CACHE[date]["groups"][data["group"]]

            elif data["who_is_user"] == "Преподаватель":
                schedule = CACHE[date]["teachers"][data["teacher"]]
        except KeyError:
            schedule = "Выходной"
            schedule_is_not_empty = False

        if schedule_is_not_empty:
            schedule = "\n".join(schedule)

        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"{schedule}"
        )


async def week(message: Message, state: FSMContext):
    data = await state.get_data()

    output_schedule = []
    for i in range(7):
        day = (datetime.today() + timedelta(days=i)).strftime("%A")
        date = (datetime.today() + timedelta(days=i)).strftime("%d.%m.%Y")

        if day == "Sunday":
            output_schedule.append(f"<pre>Воскресенье, {(datetime.today() + timedelta(days=i)).strftime('%d.%m.%y')}</pre>\n<b>Выходной. Пар нет</b>\n")
        else:
            try:
                if data["who_is_user"] == "Студент":
                    schedule = CACHE[date]["groups"][
                        data["group"]]
                else:
                    schedule = CACHE[date]["teachers"][
                        data["teacher"]]
            except KeyError:
                output_schedule.append("\n\n<pre>Это всё известное расписание на неделю</pre>")
                break


            schedule = "\n".join(schedule)

            if schedule:
                output_schedule.append(
                    f"<pre>{days[day]}, {date}</pre>\n"
                    f"{schedule}\n\n")
            else:
                output_schedule.append(
                    f"<pre>{days[day]}, {date}</pre>\n"
                    f"<b>Выходной. Пар нет</b>\n\n")

    await message.answer("".join(output_schedule))


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
