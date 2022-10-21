from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    who_is_user_state = State()
    enter_name_state = State()
    main_menu_state = State()
