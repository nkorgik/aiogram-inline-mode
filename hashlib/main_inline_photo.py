"""Send photo as an answer to inline_query """
import uuid

from aiogram.types import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Bot, Dispatcher, executor
from aiogram.utils.callback_data import CallbackData

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
cb = CallbackData('test', 'action')

def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Нажми 😱', callback_data=cb.new('push'))],
        [InlineKeyboardButton(text='YouTube ✅', url='https://www.youtube.com/channel/UCOWaWydDLr2unk_F0LcvT1w/videos')],
    ])

    return ikb

def get_second_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Упс!', callback_data=cb.new('ops')), InlineKeyboardButton('Назад', callback_data=cb.new('back'))]
    ])

    return ikb


@dp.inline_handler()
async def inline_photo(inline_query: types.InlineQuery) -> None:
    text = inline_query.query
    result_id = uuid.uuid4()

    item = InlineQueryResultPhoto(
        id=str(result_id),
        photo_url='https://media.istockphoto.com/photos/funny-winking-kitten-picture-id1267021092?k=20&m=1267021092&s=612x612&w=0&h=yzwxZXklHn5NwDTgKmbq2Ojtg3pga6j8K3oT7lLneAY=',
        thumb_url='https://media.istockphoto.com/photos/funny-winking-kitten-picture-id1267021092?k=20&m=1267021092&s=612x612&w=0&h=yzwxZXklHn5NwDTgKmbq2Ojtg3pga6j8K3oT7lLneAY=',
        caption=text,
        reply_markup=get_inline_keyboard(),
    )

    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item],
                                  cache_time=2)


@dp.callback_query_handler(cb.filter(action='push'))
async def ikb_push_cb_handler(callback: types.CallbackQuery) -> None:
    # await callback.message.edit_reply_markup(reply_markup=get_second_keyboard())
    await callback.answer('Я в шоке!')


@dp.callback_query_handler(cb.filter(action='back'))
async def ikb_push_cb_handler(callback: types.CallbackQuery) -> None:
    # await callback.message.edit_reply_markup(reply_markup=get_inline_keyboard())
    await callback.answer('Я в шоке!')


@dp.callback_query_handler(cb.filter(action='ops'))
async def ikb_push_cb_handler(callback: types.CallbackQuery) -> None:
    await callback.answer('Я в шоке!',
                          show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
