from aiogram import Bot, Dispatcher, executor, types

from inline_mode_urls.config import TOKEN_API

bot = Bot(TOKEN_API,
          parse_mode='HTML')  # create a bot here
dp = Dispatcher(bot)
