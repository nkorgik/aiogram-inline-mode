import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN_API

from handlers import register_handlers, register_queries


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s:%(asctime)s - %(message)s')

    bot = Bot(TOKEN_API)
    dp = Dispatcher(bot)

    register_handlers(dp)
    register_queries(dp)

    try:
        await dp.start_polling()
    except:
        logging.error("Executor object hasn't been started")


if __name__ == "__main__":
    asyncio.run(main())
