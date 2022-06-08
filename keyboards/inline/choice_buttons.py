from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.items import ItemEntity
from keyboards.inline.callback_data import buy_callback, items_callback, station_callback

items = InlineKeyboardMarkup(row_width=0, inline_keyboard=[
    [InlineKeyboardButton(text=f"{x.title} {x.weight}гр({x.price} руб.)",
                          callback_data=items_callback.new(
                              type=x.type,
                              FullName=f"{x.title} {x.weight}гр({x.price} руб.)",
                              price=x.price
                          ))] for x in ItemEntity.getItems()
])

# metro_stations = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
#     [InlineKeyboardButton(text=x[1], callback_data=station_callback.new(type=x[0], title=x[1]))] for x in metro
# ])


accepting = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Оплатить",
            callback_data=buy_callback.new(category_item_name="Buy"))],
    [
        InlineKeyboardButton(
            text="Отменить",
            callback_data=buy_callback.new(category_item_name="Cancel"))],
])
