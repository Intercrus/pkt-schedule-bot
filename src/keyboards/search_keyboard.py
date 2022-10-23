from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

search = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Группа"),
            KeyboardButton(text="Преподаватель")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)