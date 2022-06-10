import asyncio
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ContentType
from data.admins import Admins
from data.items import ItemEntity
from keyboards.inline.callback_data import buy_callback, items_callback, station_callback, admin_callback
from keyboards.inline.choice_buttons import accepting
from loader import dp, bot
from states.consts import Metro
from states.menu import Menu
from utils.db_api.sqlLite import DB


def get_inline_keyboard_items():
    list_st = ItemEntity.getMenuItems()

    return InlineKeyboardMarkup(row_width=0, inline_keyboard=[
        [InlineKeyboardButton(text=f"{x.title} {x.weight}гр({x.price} руб.)",
                              callback_data=items_callback.new(
                                  type=x.type,
                                  FullName=f"{x.title} {x.weight}гр({x.price} руб.)",
                                  price=x.price
                              ))] for x in list_st
    ])


@dp.message_handler(Command('start'))
async def show_items(message: types.Message):
    await message.answer(f"Привет")
    items2 = get_inline_keyboard_items()
    await message.answer(text="Вот что у нас есть", reply_markup=items2)


@dp.message_handler(Command('start'), state=Menu.ItemType)
async def show_items(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Привет")
    items2 = get_inline_keyboard_items()
    await message.answer(text="Вот что у нас есть", reply_markup=items2)


@dp.message_handler(Command('start'), state=Menu.MetroStation)
async def show_items(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Привет")
    items2 = get_inline_keyboard_items()
    await message.answer(text="Вот что у нас есть", reply_markup=items2)


@dp.callback_query_handler(items_callback.filter())
async def choose_metro(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await Menu.ItemType.set()
    fullName = callback_data.get("FullName")
    type1 = callback_data.get("type")
    price = callback_data.get("price")

    list_st = Metro.stations_by_item(int(price))

    ms = InlineKeyboardMarkup(row_width=1, inline_keyboard=[

        [InlineKeyboardButton(text=x, callback_data=station_callback.new(type='station', title=x[0]))] for x in list_st

    ])

    await call.message.answer("выберите метро", reply_markup=ms)

    await state.update_data(item=[fullName, type1, price])
    await Menu.next()


@dp.callback_query_handler(station_callback.filter(type="station"), state=Menu.MetroStation)
async def pre_order(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    ans1 = data.get("item")
    ans2 = call.message.reply_markup.inline_keyboard[0][0].text

    for i in call.message.reply_markup.inline_keyboard:
        if i[0].text[0] == callback_data.get('title'):
            ans2 = i[0].text
    await state.update_data(station=ans2)

    await call.message.answer(f"""
Товар и объем {ans1[0]}
Ближайшее метро {ans2}
Для проведения оплаты нажмите на кнопку ОПЛАТИТЬ
После того, как Вы нажмете кнопку оплаты, у вас есть 30 минут на оплату
    """, reply_markup=accepting)
    await Menu.next()


@dp.callback_query_handler(buy_callback.filter(category_item_name="Cancel"))
async def cancel(call: CallbackQuery, state: FSMContext):
    if DB.check_exist(call.from_user.id):
        DB.unreserve_any_item()
    await state.finish()
    await state.reset_state()
    await state.reset_data()
    DB.delete_order(call.from_user.id)
    await call.message.answer("Предыдущий заказ отменён")
    items2 = get_inline_keyboard_items()
    await call.message.answer(text="Вот что у нас есть", reply_markup=items2)


# async def otmena(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await state.reset_state()
#     await state.reset_data()
#     DB.delete_order(call.from_user.id)
#     await call.message.answer(text="Вот что у нас есть", reply_markup=items)
#     await Menu.ItemType.set()


@dp.callback_query_handler(buy_callback.filter(category_item_name="Buy"))
async def buy(call: CallbackQuery, state: FSMContext):
    card = Admins[0].card
    tg_id = Admins[0].tg_id
    data = await state.get_data()
    if DB.check_exist(call.from_user.id):
        await call.message.answer("Предыдущий заказ отменён")
        DB.delete_order(call.from_user.id)

    if data and DB.check_item(data.get("item")[2], data.get("station")):
        loop = asyncio.get_event_loop()
        loop.create_task(scheduled(10, state, call))

        ans1 = data.get("item")

        try:
            mu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[

                [InlineKeyboardButton(text="Оплачено",
                                      callback_data=admin_callback.new(accept="accept", user_id=call.from_user.id))]

            ])
            await dp.bot.send_message(tg_id, "Ожидай " + ans1[2] + " руб.    ID: " + str(call.from_user.id),
                                      reply_markup=mu)
        except Exception as err:
            logging.exception(err)

        st = data.get("station")

        DB.insert_order(call.from_user.id, ans1[2], ans1[1], st)
        order_t = DB.select_order(call.from_user.id)

        DB.reserve_item(data.get("item")[2], data.get("station"))

        await call.message.answer(
            text=f"""Заявка на оплату № {10173 + order_t[0]}. Переведите на банковскую карту {ans1[2]} рублей удобным для вас способом. Важно пополнить ровную сумму. {card} ‼️ у вас есть 30 мин на оплату, после чего платёж не будет зачислен ‼️ перевёл неточную сумму - оплатил чужой заказ
                """)
        await state.finish()
    else:
        await state.finish()
        await call.message.answer("Товар закончился!")
        await show_items(call.message, state)


async def scheduled(wait_for, state, call):
    await asyncio.sleep(wait_for)

    if DB.check_exist(call.from_user.id):
        await call.message.answer("Время вышло!")
        data = await state.get_data()
        await cancel(call, state)
