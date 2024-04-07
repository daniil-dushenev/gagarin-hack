import telebot
import asyncio
from telethon.sync import TelegramClient
from config import API_ID, API_HASH, TOKEN

# Создаем экземпляр TelegramClient
client = TelegramClient('session_name', API_ID, API_HASH)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения сообщений из канала
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


# Обработчик команды /get_posts
@bot.message_handler(commands=['get_posts'])
def get_channel_posts(message):
    channel_username = 'cbrstocks'  # Замените на ваше имя канала
    ans = asyncio.run(parse_channel_messages(channel_username, limit=3))  # Вызываем асинхронную функцию

    bot.reply_to(message, "\n\n".join(ans))


bot.polling()

