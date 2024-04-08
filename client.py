from telethon.sync import TelegramClient


async def parse_channel_messages(client: TelegramClient, channel_username, limit=5):
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