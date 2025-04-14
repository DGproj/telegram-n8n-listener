#Telegram to n8n Webhook Forwarder
Скрипт на Python, который слушает указанные Telegram-каналы через Telethon и отправляет новые сообщения в Webhook n8n.

#Установка
pip install -r requirements.txt

#Запуск
python listener.py

#Настройки
Измени в:

listener.py
- список каналов (17)

.env
- api_id
- api_hash
- webhook_url