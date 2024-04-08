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

dp = Dispatcher()

client = TelegramClient('session_name', API_ID, API_HASH)


async def parse_channel_messages(channel_username, limit=5):
    await client.start()
    ans = []

    # Получаем информацию о канале
    channel_info = await client.get_entity(channel_username)

    # Получаем все сообщения из канала
    messages = await client.get_messages(channel_info, limit=limit)

    # Выводим текст каждого сообщения
    for message in messages:
        ans.append(message.text)

    # Останавливаем клиент Telegram
    await client.disconnect()

    return ans


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")



@dp.message(aiogram.filters.Command('get_posts'))
async def get_channel_posts(message: types.Message,
                            command):

    channel_username = command.args
    ans = await parse_channel_messages(channel_username, limit=3)  # Вызываем асинхронную функцию
    await message.answer(f"Новости канала {channel_username}\n\n" + "\n\n".join(ans))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())