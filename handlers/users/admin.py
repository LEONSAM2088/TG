import logging
from random import random
import re
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, Message, InputFile
import uuid
from data.admins import Admins
from keyboards.inline.callback_data import buy_callback, items_callback, station_callback, admin_callback
from keyboards.inline.choice_buttons import items, accepting
from loader import dp, bot
from states.addItem import Item
from states.consts import Metro
from states.menu import Menu
import os
from utils.db_api.sqlLite import DB


@dp.message_handler(Command('admin'), user_id=[x.tg_id for x in Admins], state=Menu.MetroStation)
async def show_items(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Загружай фото")


@dp.message_handler(Command('admin'), user_id=[x.tg_id for x in Admins], state=Menu.ItemType)
async def show_items(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Загружай фото")


@dp.callback_query_handler(admin_callback.filter(accept="accept"), user_id=[x.tg_id for x in Admins])
async def accept_button(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = int(callback_data.get("user_id"))
    db = DB.select_order(user_id)
    if DB.check_exist(user_id):

        type_item = db[3]
        price_item = db[2]
        station = db[4]
        try:
          data_t = DB.select_one_item(type_item, price_item, station)

          await bot.send_message(user_id, text=f"""
          Наименование товара: {data_t[1]} {data_t[6]}гр({data_t[2]} руб.)

          Местонахождение:
          {data_t[3]}

          Метро: {data_t[5]}""")

          await bot.send_photo(user_id, photo=InputFile(path_or_bytesio=f"photos/{data_t[4]}"))
          DB.delete_item(price_item)
          await call.message.answer(f"Заказ №{user_id} закрыт!")
        except:
            await call.message.answer("Грустная ошибка")



        DB.delete_order(user_id)
    else:
        await call.message.answer("Такого заказа нет!")


@dp.message_handler(user_id=[x.tg_id for x in Admins], content_types=ContentType.PHOTO)
async def get_photo(message: Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    photoId = uuid.uuid4()
    await message.photo[-1].download(f'photos/{photoId}.' + file_info.file_path.split('photos/')[1].split('.')[-1])
    await Item.PhotoLink.set()

    await state.update_data(link=f'{photoId}.' + file_info.file_path.split('photos/')[1].split('.')[-1])
    await Item.next()
    await message.answer(text="Введите название товара")


@dp.message_handler(state=Item.ItemName)
async def choose_name(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text="Введите цену")
    await Item.next()


@dp.message_handler(state=Item.ItemPrice)
async def choose_name(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer(text="Введите описание")
    await Item.next()


@dp.message_handler(state=Item.ItemDescription)
async def choose_name(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    #await message.answer(text="Введите станцию метро")

    await Item.next()
    await choose_name22(message, state)


@dp.message_handler(state=Item.ItemStation)
async def choose_name22(message: Message, state: FSMContext):
    await state.update_data(station="м.Комендантский проспект(Чистое небо)")
    await message.answer(text="Введите вес")
    await Item.next()


@dp.message_handler(state=Item.ItemWeight)
async def choose_name(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await Item.next()
    await opa(message, state)


@dp.message_handler(state=Item.ItemType)
async def opa(message, state):
    await state.update_data(type="item")
    data = await state.get_data()
    price = data.get("price")
    weight = data.get("weight")
    try:
        price = int(price)

        DB.insert_item(data.get("title"), price, data.get("desc"), data.get("link"), data.get("station"),
                       weight, data.get("type"))
        await message.answer("Товар добавлен")
    except:
        await message.answer("Введены некорректные данные")

    await state.finish()
