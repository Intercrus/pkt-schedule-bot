from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


who_is_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Студент"),
            KeyboardButton(text="Преподаватель")
        ]
    ],
    resize_keyboard=True
)
