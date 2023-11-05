from aiogram.dispatcher.filters.state import State, StatesGroup


class ClaendarStates(StatesGroup):
    wait_answer = State()


class YaDriveStates(StatesGroup):
    wait_for_files = State()
