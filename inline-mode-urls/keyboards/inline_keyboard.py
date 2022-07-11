from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='YouTube Channel',
                           url='https://www.youtube.com/channel/UCOWaWydDLr2unk_F0LcvT1w/videos')

ikb.add(ib1)