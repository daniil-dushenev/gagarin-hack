import asyncio
import logging
import sys
from os import getenv

import aiogram.filters
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from telethon.sync import TelegramClient

from config import API_ID, API_HASH, TOKEN
from client import parse_channel_messages

dp = Dispatcher()

client = TelegramClient('session_name', API_ID, API_HASH)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", parse_mode=ParseMode.HTML)



@dp.message(aiogram.filters.Command('get_posts'))
async def get_channel_posts(message: types.Message,
                            command):
    try:
        channel_username = command.args
        ans = await parse_channel_messages(client, channel_username, limit=3)
        await message.answer(f"Новости канала {channel_username}\n\n" + "\n\n".join(ans))
    except Exception as e:
        error_message = f"Произошла ошибка при получении постов из канала {channel_username}: {str(e)}"
        await message.answer(error_message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())