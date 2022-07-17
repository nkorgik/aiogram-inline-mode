"""Here's the simplest sample of errorHandler using Aiogram library"""
import asyncio

from aiogram.utils.exceptions import BotBlocked

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from config import TOKEN_API

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)
cb = CallbackData('number', 'action')

number = 0

def get_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Increase', callback_data=cb.new('increase')), InlineKeyboardButton('Decrease', callback_data=cb.new('decrease'))],
        [InlineKeyboardButton('Close', callback_data='close')],
        [InlineKeyboardButton('Reply', callback_data=cb.new('reply'))]
    ])

    return ikb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='The number is - 0',
                           reply_markup=get_keyboard())


# @dp.callback_query_handler(cb.filter())  # bad code
# async def ikb_cb_handler(callback: types.CallbackQuery, callback_data: dict) -> None:
#     global number
#     if callback_data['action'] == 'increase':
#         number += 1
#         await callback.message.edit_text(f'The number is - {number}',
#                                          reply_markup=get_keyboard())
#     elif callback_data['action'] == 'decrease':
#         number -= 1
#         await callback.message.edit_text(f'The number is - {number}',
#                                          reply_markup=get_keyboard())
#     elif callback_data['action'] == 'reply':
#         await asyncio.sleep(10)
#         await callback.message.answer('Прости, забыл!')
#     await callback.answer()

@dp.callback_query_handler(cb.filter(action='increase'))    # it's of vital importance to write code with using one responsibility principle
async def ikb_increase_cb_handler(callback: types.CallbackQuery) -> None:
    global number
    number += 1
    await callback.message.edit_text(f'The number is - {number}',
                                     reply_markup=get_keyboard())
    await callback.answer()


@dp.callback_query_handler(cb.filter(action='decrease'))
async def ikb_increase_cb_handler(callback: types.CallbackQuery) -> None:
    global number
    number -= 1
    await callback.message.edit_text(f'The number is - {number}',
                                     reply_markup=get_keyboard())
    await callback.answer()


@dp.callback_query_handler(cb.filter(action='reply'))
async def ikb_increase_cb_handler(callback: types.CallbackQuery) -> None:
    await asyncio.sleep(10)
    await callback.message.answer('Прости, забыф(')
    await callback.answer()


@dp.callback_query_handler(text='close')
async def ikb_close_cb_handler(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.answer()


@dp.errors_handler(exception=BotBlocked)
async def global_error_handler(update: types.Update, exception: BotBlocked) -> bool:
    print('ошибочка вышла - пользователь нас заблокировал')

    return True


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)


