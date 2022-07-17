import random
import pprint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from config import TOKEN_API

random_number = 0

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Increase', callback_data='increase'), InlineKeyboardButton(text='decrease', callback_data='decrease')],
    [InlineKeyboardButton(text='Random', callback_data='random_value')]
])


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


# implementation with using simple callback_data: str #

@dp.message_handler(commands=['counter'])
async def cmd_counter(message: types.Message) -> None:
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


# implementation with using Callback Data Factory pattern | callback_data: dict #

cb = CallbackData('number', 'action')  # here we've created new "callback" data factory pattern instance
user_data = dict()  # in this dictionary we're gonna store our random_number here that's got to do with our user model

def get_keyboard() -> InlineKeyboardMarkup:  # unfinished
    ikb_2 = InlineKeyboardMarkup(inline_keyboard=[  # here we have created our inlinekeyboardmarkup obviously
        [InlineKeyboardButton('Increase', callback_data=cb.new('increase')),
         InlineKeyboardButton('Decrease', callback_data='decrease')],
        [InlineKeyboardButton('Random', callback_data=cb.new('random'))]
    ])
    return ikb_2


@dp.message_handler(commands=['callback'])  # this handler is going to be processing "/callback" command and "reply" ikb_2 we have created above
async def cmd_callback(message: types.Message) -> None:
    user_data[message.from_user.id] = 0
    await bot.send_message(chat_id=message.chat.id,
                           reply_markup=get_keyboard(),
                           text='The current number is - 0')


@dp.callback_query_handler(cb.filter())  # there's no need to use sophisticated lambda filters anymore, we just implement new built-in filter in this place that significantly simplify our work
async def ikb2_increase_cb_handler(callback: types.CallbackQuery, callback_data: dict) -> None:
    global user_data
    if callback_data['action'] == 'increase':
        user_data[callback.from_user.id] += 1
        await callback.message.edit_text(f'The current number is - {user_data[callback.from_user.id]}',
                                         reply_markup=get_keyboard())
    elif callback_data['action'] == 'decrease':
        user_data[callback.from_user.id] -= 1
        await callback.message.edit_text(f'The current number is - {user_data[callback.from_user.id]}',
                                         reply_markup=get_keyboard())

    user_data[callback.from_user.id] = random.randint(1, 50)
    await callback.message.edit_text(f'The current number is - {user_data[callback.from_user.id]}',
                                     reply_markup=get_keyboard())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
