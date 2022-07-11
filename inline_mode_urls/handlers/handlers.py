from aiogram import Dispatcher, types

from inline_mode_urls.utils.main import bot
from inline_mode_urls.keyboards import inline_keyboard

async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome to me bot!',
                           reply_markup=inline_keyboard.ikb)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
