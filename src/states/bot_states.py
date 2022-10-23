from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    who_is_user_state = State()
    enter_name_state = State()
    main_menu_state = State()

    # Search_by button
    search_by_state = State()

    search_by_group_state = State()
    search_by_teacher_state = State()
