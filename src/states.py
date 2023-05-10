from aiogram.dispatcher.filters.state import State, StatesGroup


class ClaendarStates(StatesGroup):
    wait_answer = State()


class YaDriveStates(StatesGroup):
    arhcieve_dir = State()
    req_for_files = State()
    wait_for_files = State()
