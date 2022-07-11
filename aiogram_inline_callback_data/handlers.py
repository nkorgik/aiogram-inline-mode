from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

# =====================KEYBOARDS =================
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='Ютуб канал',
                           url='https://www.youtube.com/channel/UCOWaWydDLr2unk_F0LcvT1w/videos')
vote_button1 = InlineKeyboardButton(text='❤',
                                    callback_data='like')
vote_button2 = InlineKeyboardButton(text='👎',
                                    callback_data='dislike')

ikb.add(ib1).add(vote_button1, vote_button2)
# ================================================


async def start_command(message: types.Message):
    await message.answer(text='Привет, а тут на русском уже 😝',
                         reply_markup=ikb)


async def vote(callback: types.CallbackQuery):
    await callback.answer(callback.data)

def register_queries(dp: Dispatcher):
    dp.register_callback_query_handler(vote, Text(equals=['like', 'dislike'], ignore_case=True))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
