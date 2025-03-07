import os
from telethon import TelegramClient

# گرفتن آیدی کانال از متغیر محیطی
X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))

async def forward_to_inlinebot(client):
    # استفاده از آیدی عددی کانال x_archive
    channel = await client.get_entity(X_ARCHIVE_CHANNEL_ID)
    
    # دریافت پیام‌های آخر از کانال
    messages = await client.get_messages(channel, limit=10)

    for message in messages:
        # فقط پیام‌هایی که شامل فایل صوتی هستند (آهنگ‌ها)
        if message.audio:
            try:
                # ارسال به پیوی Inlinebot
                await client.send_message(
                    'me',  # ارسال به پیوی خود Inlinebot
                    message
                )
                print(f"Forwarded song with message_id {message.id} to Inlinebot's private chat.")
            except Exception as e:
                print(f"Error forwarding song {message.id}: {e}")

# اجرای تابع
async def main(client):
    await forward_to_inlinebot(client)

# برای استفاده از این تابع در پروژه
await main(client)
