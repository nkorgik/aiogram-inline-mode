from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN_API
from keyboards import inline_keyboard

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('The bot has been powered up successfully =)')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Welcome to our excellent bot!',
                         reply_markup=)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           on_startup="")