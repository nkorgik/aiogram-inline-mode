from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# =====================KEYBOARDS =================
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='Ютуб канал',
                           url='https://www.youtube.com/channel/UCOWaWydDLr2unk_F0LcvT1w/videos')

ikb.add(ib1)
# ================================================


async def start_command(message: types.Message):
    await message.answer(text='Привет, а тут на русском уже 😝',
                         reply_markup=ikb)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])