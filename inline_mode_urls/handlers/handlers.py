from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from inline_mode_urls.utils.main import bot
from inline_mode_urls.keyboards import inline_keyboard
from inline_mode_urls.keyboards import keyboard

TEST_MESSAGE = """
<em>Hi, welcome to my bot. Here you're gonna be able to
plan something, create your own events and set 
notifications in the Telegram.
You can also take a look at my <b>YouTube</b> channel where I expound 
how to create Telegram bots and much more</em>"""
HELP_COMMAND = """
<b>/help</b> - <em>a list of commands</em>
<b>/desc</b> - <em>description of this bot</em>
<b>/menu</b> - <em>the main menu of our bot</em>"""

async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome to my bot!\nIn order for you to give this a start - push /menu')

async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode='HTML')

async def description_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=TEST_MESSAGE,
                           reply_markup=inline_keyboard.ikb,
                           parse_mode='HTML')

async def menu_command(message: types.Message):
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker="CAACAgQAAxkBAAEFO9hiyZapnjUwZ0cgIelk-Qe49P2R5gACWAADzjkIDRhMYBsy9QjTKQQ")
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome to main menu!',
                           reply_markup=keyboard.kb_client)

async def start_working(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           tetx='')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(description_command, commands=['desc'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(menu_command, commands=['menu'])
    dp.register_message_handler(start_working, Text(equals='Start work', ignore_case=True))
