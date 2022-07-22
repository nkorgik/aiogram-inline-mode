"""Finite state machine
States, MemoryStorage
explanation
"""
import sqlite3 as sq

from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text

from config import TOKEN_API


storage = MemoryStorage()  # create new instance of our storage
bot = Bot(TOKEN_API)
dp = Dispatcher(bot=bot,
                storage=storage)
cb = CallbackData('menu', 'action')


def start_db() -> None:
    global db, cur
    db = sq.connect('new.db')
    cur = db.cursor()

    if db:
        print('connected to db successfully')

    db.execute("CREATE TABLE IF NOT EXISTS profiles(id TEXT PRIMARY KEY, photo TEXT, description TEXT, age TEXT, name TEXT)")
    db.commit()


async def create_profile(user_id: str) -> None:
    user = cur.execute("SELECT 1 FROM profiles WHERE id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profiles VALUES(?, ?, ?, ?, ?)", (user_id, '', '', '', ''))
        db.commit()

    return


async def edit_profile(state: FSMContext, user_id: str) -> None:
    async with state.proxy() as data:
        cur.execute("UPDATE profiles SET photo = '{}', description = '{}', age = '{}', name = '{}' WHERE id == '{}'"
                    .format(data['photo'], data['desc'], data['age'], data['name'], user_id))

        db.commit()


async def get_profile(user_id: str):
    return cur.execute("SELECT * FROM profiles WHERE id == '{}'".format(user_id)).fetchall()


async def on_startup(_) -> None:
    print('Bot has been started successfully')
    start_db()


class ProfileStateGroup(StatesGroup):  # this contains all the states of our finite-state automaton

    photo = State()
    name = State()
    age = State()
    desc = State()


def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Заполнить анкету 🐝', callback_data=cb.new('start'))],
        [InlineKeyboardButton(text='Мой YouTube', url='https://www.youtube.com/watch?v=HU_A2pRYw74')]
    ])

    return ikb


def get_cancel_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Отмена', callback_data=cb.new('cancel'))]
    ])

    return ikb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('_Добро пожаловать в наш бот!_',
                         parse_mode='markdown',
                         reply_markup=get_ikb())

    await create_profile(message.from_user.id)


@dp.callback_query_handler(cb.filter(action='start'))  # it's essential according to srp
async def cb_menu_start_handler(callback: types.CallbackQuery) -> None:

    await callback.message.edit_text(text='_Сначала отправь нам свою фотографию_',
                                     parse_mode='markdown',
                                     reply_markup=get_cancel_ikb())

    await ProfileStateGroup.photo.set()
    await callback.answer()


@dp.message_handler(lambda message: not message.photo, state=ProfileStateGroup.photo)
async def check_is_photo(message: types.Message) -> types.Message:
    return await message.reply('Это вообще не фотография!')


@dp.message_handler(content_types=['photo'], state=ProfileStateGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await ProfileStateGroup.next()
    await message.reply('А теперь имя введите своё имя',
                        reply_markup=get_cancel_ikb())


@dp.message_handler(lambda message: not message.text, state=ProfileStateGroup.name)
async def check_is_name(message: types.Message) -> types.Message:
    return await message.reply('Это не имя! Врёшь!')


@dp.message_handler(state=ProfileStateGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await ProfileStateGroup.next()
    await message.reply('А теперь укажи свой возраст',
                        reply_markup=get_cancel_ikb())


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) > 90, state=ProfileStateGroup.age)
async def check_is_age(message: types.Message) -> types.Message:
    return await message.reply('Укажи, пожалуйста, возраст')


@dp.message_handler(lambda message: message.text.isdigit(), state=ProfileStateGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await ProfileStateGroup.next()
    await message.reply('А теперь расскажи вкратце о себе',
                        reply_markup=get_cancel_ikb())


@dp.message_handler(state=ProfileStateGroup.desc)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['desc'] = message.text

    await edit_profile(state, message.from_user.id)

    await state.finish()

    user = await get_profile(message.from_user.id)
    print(user)
    await bot.send_photo(message.from_user.id,
                         photo=user[0][1],
                         caption=f"{user[0][2]} {user[0][3]}\n{user[0][4]}")
    await message.answer('Твой профиль успешно создан!')


@dp.callback_query_handler(cb.filter(action='cancel'), state='*')
async def cb_menu_cancel_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await callback.message.edit_text('_Добро пожаловать в наш бот!_',
                                     parse_mode='markdown',
                                     reply_markup=get_ikb())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
