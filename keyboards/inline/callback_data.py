from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "category_item_name")

items_callback = CallbackData("item", "type", "FullName", "price")
station_callback = CallbackData("station", "type", "title")


admin_callback = CallbackData("admin", "accept", "user_id")
