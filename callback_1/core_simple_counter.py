import random
import pprint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN_API

random_number = 0

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Increase', callback_data='increase'), InlineKeyboardButton(text='decrease', callback_data='decrease')],
    [InlineKeyboardButton(text='Random', callback_data='random_value')]
])

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_message(chat_id=message.chat.id,
                           text='Number is 0',
                           reply_markup=ikb)
    await message.delete()


@dp.callback_query_handler(text='random_value')  # handler will process the callback queries whose callback_data consists of "random_value"
async def ikb_cb_handler(callback: types.CallbackQuery) -> None:
    global random_number
    random_number = random.randint(1, 50)

    await callback.message.edit_text(f'The number is {random_number} at the moment',
                                     reply_markup=ikb)

    # await callback.answer(f'The number is - {random_number}')


@dp.callback_query_handler(text='decrease')  # handler is going to be processing the callback queries whose callback_data consists of "decrease"
async def ikb_decrease_cb_handler(callback: types.CallbackQuery) -> None:
    global random_number
    random_number -= 1
    # pprint.pprint(callback)
    await callback.message.edit_text(f'The number is {random_number} at the moment',
                                     reply_markup=ikb)


@dp.callback_query_handler(lambda callback: callback.data.startswith('i'))  # handler processes the callback queries that begin with "i"
async def ikb_increase_cb_handler(callback: types.CallbackQuery) -> None:
    global random_number
    random_number += 1

    await callback.message.edit_text(f'The number is {random_number} at the moment',
                                     reply_markup=ikb)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
