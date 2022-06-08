from aiogram.dispatcher.filters.state import StatesGroup, State


class Menu(StatesGroup):
    ItemType = State()
    MetroStation = State()
