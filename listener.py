from dotenv import load_dotenv
import os
from telethon import TelegramClient, events
import requests
import asyncio

#Загружаем переменные из .env
load_dotenv()

#ДАННЫЕ ДЛЯ АВТОРИЗАЦИИ
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

#URL Webhook в n8n
webhook_url = os.getenv("WEBHOOK_URL")

# Список каналов, которые нужно слушать (можно расширить)
channels_usernames = (
    'название канала1 без @',
    'название канала2 без @'
)

#ИНИЦИАЛИЗАЦИЯ КЛИЕНТА (Эмулируем обычное устройство)
client = TelegramClient(
    'anon', api_id, api_hash,
    system_version='4.16.30-vxCUSTOM',
    device_model='Windows PC',
    app_version='4.2'
)

#ОБРАБОТКА НОВЫХ СООБЩЕНИЙ
@client.on(events.NewMessage(chats=channels_usernames))
async def handler(event):
    msg = event.message.message  # Текст сообщения
    channel = event.chat.username if event.chat else "unknown"  # Имя канала
    date = event.message.date.isoformat()  # Форматируем дату в ISO 8601
    message_id = event.message.id  # ID сообщения

    print(f"📩 Новое сообщение из {channel}: {msg}")

    # 📤 Формируем JSON для Webhook
    data = {
        "update_id": message_id,
        "message": {
            "text": msg,
            "chat": {
                "username": channel
            },
            "date": date
        }
    }

    # 📬 Отправляем данные в n8n
    try:
        response = requests.post(webhook_url, json=data)
        print(f"✅ Webhook отправлен (статус: {response.status_code})")
    except Exception as e:
        print(f"❌ Ошибка при отправке в n8n: {e}")

#Запуск клиента
async def main():
    print("⏳ Запуск клиента...")
    await client.start()
    print("✅ Клиент запущен, слушаю каналы...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())