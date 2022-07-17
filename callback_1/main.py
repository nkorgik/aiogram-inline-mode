import logging
from aiogram import Bot, executor, Dispatcher, types

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN_API
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()

f = logging.Formatter('%(levelname)s:%(asctime)s - %(message)s')
ch.setLevel(logging.INFO)
ch.setFormatter(f)

logger.addHandler(ch)

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❤️', callback_data='like'), InlineKeyboardButton(text='👎', callback_data='difslidke:count')],
    []
])

@dp.message_handler(commands=['items'])
async def items_commands(message: types.Message) -> None:
    await message.answer(text='Do you like it?',
                         reply_markup=ikb)

@dp.callback_query_handler(text_contains='like')
async def callback_like(callback: types.CallbackQuery):
    await callback.answer('MEOW')


if __name__ == "__main__":
    logger.info('bot has been started')
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
