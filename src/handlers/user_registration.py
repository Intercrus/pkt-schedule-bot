from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from src.states.bot_states import BotStates

from src.keyboards.main_menu_keyboard import main_menu

from src.misc.full_names import groups, teachers


async def enter_name(message: Message, state: FSMContext):
    await state.update_data(who_is_user=message.text)

    if message.text == "Студент":
        await message.answer(
            "Введите название вашей группы\n"
            "Например, 209ЗМ-2 или 209БД",
            reply_markup=ReplyKeyboardRemove()
        )

        await state.set_state(BotStates.enter_name_state)

    elif message.text == "Преподаватель":
        await message.answer(
            "Введите вашу фамилию\n"
            "Например, Опуховская или Цветкова",
            reply_markup=ReplyKeyboardRemove()
        )

        await state.set_state(BotStates.enter_name_state)


async def find_name(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["who_is_user"] == "Студент":
        group = message.text.upper()
        if group in groups:
            await state.update_data(group=group)
            await message.answer("Группа найдена ✅", reply_markup=main_menu)
            await state.set_state(BotStates.main_menu_state)
        else:
            await message.answer("Группа не найдена ❌")

    elif data["who_is_user"] == "Преподаватель":
        teacher = message.text.capitalize()
        if teacher in teachers:
            await state.update_data(teacher=teacher)
            await message.answer("Преподаватель найден ✅", reply_markup=main_menu)
            await state.set_state(BotStates.main_menu_state)
        else:
            await message.answer("Преподаватель не найден ❌")


def register_user_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_name, state=BotStates.who_is_user_state)
    dp.register_message_handler(find_name, state=BotStates.enter_name_state)
