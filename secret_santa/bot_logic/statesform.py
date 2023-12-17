from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    NAME_OF_THE_GAME = State()
    PLAYER_NAME = State()
    E_MAIL = State()
    INTERESTS = State()
    LETTER = State()