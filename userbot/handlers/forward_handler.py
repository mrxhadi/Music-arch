import os
from telethon import TelegramClient

# گرفتن آیدی کانال از متغیر محیطی
X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))

async def forward_to_inlinebot(client):
    # دریافت آیدی کانال از متغیر محیطی
    channel = await client.get_entity(X_ARCHIVE_CHANNEL_ID)
    # دریافت آخرین ۱۰ پیام از کانال
    messages = await client.get_messages(channel, limit=10)

    for message in messages:
        if message.audio:  # فقط آهنگ‌ها رو فوروارد می‌کنیم
            try:
                # ارسال فایل‌ها به پیوی Inlinebot
                await client.send_message(
                    'me',  # ارسال به پیوی خود Inlinebot
                    message
                )
                print(f"Forwarded song with message_id {message.id} to Inlinebot's private chat.")
            except Exception as e:
                print(f"Error forwarding song {message.id}: {e}")
