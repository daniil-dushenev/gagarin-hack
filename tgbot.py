from telethon.sync import TelegramClient
from config import API_ID, API_HASH

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

channel_username = 'cbrstocks'
ans = client.loop.run_until_complete(parse_channel_messages(channel_username))
print(ans)