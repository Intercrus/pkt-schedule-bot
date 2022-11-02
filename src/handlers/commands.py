from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from src.misc.states import BotStates

from src.keyboards.choice_keyboard import who_is_user


async def start(message: Message, state: FSMContext):
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name} 👋\n"
        "Кто вы?",
        reply_markup=who_is_user
    )
    await state.set_state(BotStates.who_is_user_state)


async def help(message: Message):
    await message.answer(
        "Ответы на часто задаваемые вопросы\n"
        "==================================\n\n"
        "<b>Почему бот не может найти мою группу?\n</b>"
        "   Возможно, вы неправильно пишите\n   название группы."
        " Название группы\n   должно быть написано в соответствии\n"
        "   с названием группы в расписании\n   на сайте. Но для удобства"
        " можно не\n   писать заглавные буквы.\n   Например 2ЗМ-1 тоже что и 2зм-1.\n\n"
        "   Второй вариант: группы нет в списке.\n"
        "   Напишите @Intercrus и вашу группу\n   добавят"
        
        "\n\n"
        
        "<b>Почему бот не может найти мою фамилию?\n</b>"
        "   Такого преподавателя нет в списке.\n"
        "   Напишите @Intercrus и вас добавят"

        "\n\n"

        "<b>Почему бот не отвечает?\n</b>"
        "   * Бот обновляет кэш.\n     Подождите пару минут\n\n"
        "   * Разработчик обновляет бота.\n     Подождать чуть дольше\n\n"
        
        "   Чаще всего именно первая причина,\n"
        "   поскольку бота обновляют по вечерам\n\n"
        
        "   Если вы подождали и бот не отвечает,\n"
        "   то напишите, пожалуйста, @Intercrus"
        "\n\n"

        "<b>Как сменить группу?\n</b>"
        "   Для этого нужно сбросить настройки.\n"
        "   Введите команду /start"
    )


async def about(message: Message):
    await message.answer(
        "PKT Bot v2.1.0\n"
        "==============\n\n"
        "Section in development\n\n"
        "Author: Semyon @Intercrus"
    )
