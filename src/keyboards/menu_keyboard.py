from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сегодня"),
            KeyboardButton(text="Завтра")
        ],
        [
            KeyboardButton(text="Неделя"),
            KeyboardButton(text="Поиск")
        ],
    ],
    resize_keyboard=True
)