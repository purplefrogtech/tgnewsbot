from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument  # Gerekli sınıfları import ettik
import logging
import re

# Telegram API ID and Hash (can be obtained from my.telegram.org)
api_id = '29444056'
api_hash = '2f4d6c5ad97e4f9fbb15a9809d5f9056'
phone = '+905525515184'

# Source and target group IDs
SOURCE_CHAT_IDS = [-1002225995329, -1001508782705, -1001380799178, -1001106100161, -1001814562728, -1001742406071, -1001602871646, -1002201531922]  # Source group IDs
TARGET_CHAT_ID = -1001754667210  # Target group ID

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel=LOG_INFO'
)

# Telegram client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):
    message = event.message
    message_text = message.message

    # Yasaklı argümanları belirle
    forbidden_pattern = re.compile(r'http[s]?://|www\.|@[\w_]+|t\.me')

    # Mesajda yalnızca grup adı veya bağlantısı varsa ve yasaklı diğer argümanlar yoksa
    if re.search(r't\.me/[\w_]+', message_text) and not forbidden_pattern.search(message_text.replace(re.search(r't\.me/[\w_]+', message_text).group(), '')):
        # Mesajdaki yasaklı bağlantıyı kaldır
        cleaned_message_text = re.sub(r't\.me/[\w_]+', '', message_text).strip()
        # Mesajı yasaklı bağlantı olmadan ve iki satır boşluklu @themumadam ekleyerek gönder
        cleaned_message_text += '\n\n@themumadam'
        logging.info(f"Message cleaned and forwarded: {cleaned_message_text}")
        await client.send_message(TARGET_CHAT_ID, cleaned_message_text)
    # Yasaklı argümanları içeren mesajları engelle
    elif forbidden_pattern.search(message_text):
        logging.info(f"Message contains prohibited content, not forwarding: {message_text}")
    else:
        # Mesajın buton içerip içermediğini kontrol et
        if message.buttons:
            logging.info(f"Message contains buttons, not forwarding: {message_text}")
        else:
            logging.info(f"Received message from {event.chat_id}: {message_text}")
            # Mesajı iki satır boşluklu @themumadam ekleyerek gönder
            message_text += '\n\n\n ✊@mumadam0\n\n           👉@themumadam'
            # Medya içeriğini kontrol ederek mesajı ilet
            if message.media:
                if isinstance(message.media, MessageMediaPhoto) or isinstance(message.media, MessageMediaDocument):
                    await client.send_message(TARGET_CHAT_ID, message_text, file=message.media)
                else:
                    logging.info(f"Unsupported media type, not forwarding: {message_text}")
            else:
                await client.send_message(TARGET_CHAT_ID, message_text)

async def main():
    # Giriş yap
    await client.start(phone)
    logging.info("Client started")
    # Dinlemeye başla
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
