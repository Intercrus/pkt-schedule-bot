from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from datetime import datetime, timedelta

from src.misc.full_names import days
from src.misc.get_schedule import CACHE
from src.misc.anti_flood import rate_limit


@rate_limit(limit=12)
async def today(message: Message, state: FSMContext):
    data = await state.get_data()

    day = datetime.today().strftime("%A")
    date = datetime.today().strftime("%d.%m.%Y")

    schedule = []
    error_has_occurred = False

    if day == "Вокресенье":
        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"\nВыходной"
        )
    else:
        if data["who_is_user"] == "Студент":
            if CACHE.get(date) is not None:
                try:
                    schedule = CACHE[date]["groups"][data["group"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "Такой группы в кэше нет\nНапишите @Intercrus"
            else:
                error_has_occurred = True
                schedule = "\nРасписание на этот день ещё не добавлено"

        elif data["who_is_user"] == "Преподаватель":
            if CACHE.get(date) is not None:
                try:
                    schedule = CACHE[date]["teachers"][data["teacher"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "\nТакого преподавателя в кэше нет\nНапишите @Intercrus"
            else:
                error_has_occurred = True
                schedule = "\nРасписание на этот день ещё не добавлено"

        # If schedule is empty, so there are no lessons for this day
        if not schedule:
            schedule = "\nВыходной"

        # If the group or teacher in the cache
        if not error_has_occurred:
            schedule = "\n".join(schedule)

        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"{schedule}"
        )


@rate_limit(limit=12)
async def tomorrow(message: Message, state: FSMContext):
    data = await state.get_data()

    day = (datetime.today() + timedelta(days=1)).strftime("%A")
    date = (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y")

    schedule = []
    error_has_occurred = False

    if day == "Вокресенье":
        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"\nВыходной"
        )
    else:
        if data["who_is_user"] == "Студент":
            if CACHE.get(date) is not None:
                try:
                    schedule = CACHE[date]["groups"][data["group"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "\nТакой группы в кэше нет\nНапишите @Intercrus"
            else:
                error_has_occurred = True
                schedule = "\nРасписание на этот день ещё не добавлено"

        elif data["who_is_user"] == "Преподаватель":
            if CACHE.get(date) is not None:
                try:
                    schedule = CACHE[date]["teachers"][data["teacher"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "\nТакого преподавателя в кэше нет\nНапишите @Intercrus"
            else:
                error_has_occurred = True
                schedule = "\nРасписание на этот день ещё не добавлено"

        # If schedule is empty, so there are no lessons for this day
        if not schedule:
            schedule = "\nВыходной"

        # If the group or teacher in the cache
        if not error_has_occurred:
            schedule = "\n".join(schedule)

        await message.answer(
            f"<pre>{days[day]}, {date}</pre>\n"
            f"{schedule}"
        )


@rate_limit(limit=12)
async def week(message: Message, state: FSMContext):
    data = await state.get_data()

    exists_days = []
    for i in range(7):
        day = (datetime.today() + timedelta(days=i)).strftime("%A")
        date = (datetime.today() + timedelta(days=i)).strftime("%d.%m.%Y")
        if CACHE.get(date) is not None:
            exists_days.append((day, date))

    output_schedule = []
    for day, date in exists_days:
        schedule = []
        error_has_occurred = False

        if day == "Вокресенье":
            output_schedule.append(
                f"<pre>{days[day]}, {date}</pre>\n"
                f"\nВыходной"
            )
        else:
            if data["who_is_user"] == "Студент":
                try:
                    schedule = CACHE[date]["groups"][data["group"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "\nТакой группы в кэше нет\nНапишите @Intercrus"

            elif data["who_is_user"] == "Преподаватель":
                try:
                    schedule = CACHE[date]["teachers"][data["teacher"]]
                except KeyError:
                    error_has_occurred = True
                    schedule = "\nТакого преподавателя в кэше нет\nНапишите @Intercrus"

            # If schedule is empty, so there are no lessons for this day
            if not schedule:
                schedule = "\nВыходной"

            # If the group or teacher in the cache
            if not error_has_occurred:
                schedule = "\n".join(schedule)

            output_schedule.append(
                f"<pre>{days[day]}, {date}</pre>\n"
                f"{schedule}\n"
            )

    await message.answer("\n".join(output_schedule) + "\n<pre>Это все известное расписание на неделю</pre>")
