from aiogram.dispatcher.filters.state import StatesGroup, State


class Item(StatesGroup):
    PhotoLink = State()
    ItemName = State()
    ItemPrice = State()
    ItemDescription = State()
    ItemStation = State()
    ItemWeight = State()
    ItemType = State()
