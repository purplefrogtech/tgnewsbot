from telethon import TelegramClient, events
import logging
import re

# Telegram API ID ve Hash (my.telegram.org'dan alınabilir)
api_id = '29444056'
api_hash = '2f4d6c5ad97e4f9fbb15a9809d5f9056'
phone = '+905525515184'

# Kaynak ve hedef grup ID'leri
SOURCE_CHAT_IDS = [-1001300416070, -1001380799178, -1001814562728]  # Kaynak grup ID'leri
TARGET_CHAT_ID = -1001754667210  # Hedef grup ID'si

# Logging yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Telegram istemcisi
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):
    message_text = event.message.message
    
    # Link, telegram kullanıcı ismi veya grup ismi kontrolü
    if re.search(r'http[s]?://|www\.|@[\w_]+|t\.me', message_text):
        logging.info(f"Message contains prohibited content, not forwarding: {message_text}")
    else:
        logging.info(f"Received message from {event.chat_id}: {message_text}")
        await client.send_message(TARGET_CHAT_ID, message_text)

async def main():
    # Giriş yap
    await client.start(phone)
    logging.info("Client started")
    # Dinlemeye başla
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
