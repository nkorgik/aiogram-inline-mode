from aiogram import types, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

from config import TOKEN_API

bot = Bot(TOKEN_API)

# =====================KEYBOARDS =================
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='Ютуб канал',
                           url='https://www.youtube.com/channel/UCOWaWydDLr2unk_F0LcvT1w/videos')

ivote_kb = InlineKeyboardMarkup(row_width=2)
vote_button1 = InlineKeyboardButton(text='❤',
                                    callback_data='like')
vote_button2 = InlineKeyboardButton(text='👎',
                                    callback_data='dislike')

ikb.add(ib1)
ivote_kb.add(vote_button1, vote_button2)
# ================================================


async def start_command(message: types.Message):
    await message.answer(text='Привет, а тут на русском уже 😝',
                         reply_markup=ikb)

async def vote_command(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://www.burgesspetcare.com/wp-content/uploads/2021/08/Hamster.jpg")
    await message.answer(text='Нравится фоточка?',
                         reply_markup=ivote_kb)


async def vote(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id,
                           text=str(callback))
    if callback.data == 'like':
        return await callback.answer('нравица')
    await callback.answer(text="не нравица(")
    await bot.send_message(chat_id=callback.from_user.id,
                           text="почему тебе это не понравилось? 🤕")


def register_queries(dp: Dispatcher):
    dp.register_callback_query_handler(vote, Text(equals=['like', 'dislike'], ignore_case=True))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(vote_command, commands=['vote'])
