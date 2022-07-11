from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_client = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True)
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/desc')
b3 = KeyboardButton('Start work')

kb_client.add(b1).insert(b2).add(b3)
