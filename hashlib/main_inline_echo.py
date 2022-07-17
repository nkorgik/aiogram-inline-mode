"""The simplest sample of inline_echo bot that's written using Aiogram
You can also find this example in the standard documentation of Aiogram library"""

import hashlib

from aiogram import types, Bot, Dispatcher, executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle


from config import TOKEN_API

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or 'echo'  # we have chosen "echo or .query" because .query can be equal an empty value

    input_content = InputTextMessageContent(text)  # content of the reply message
    result_id: str = hashlib.md5(text.encode()).hexdigest()      # but for example i'll generate it based on text because I know, that
                                                                  # only text will be passed in this example (c) - from DOC

    item = InlineQueryResultArticle(
        id=result_id,
        title='ECHO BOT',
        input_message_content=input_content
    )

    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item],
                                  cache_time=1)


if __name__ == '__main__':
    executor.start_polling(skip_updates=True,
                           dispatcher=dp)


