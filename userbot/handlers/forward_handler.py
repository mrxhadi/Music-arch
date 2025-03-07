import os
from telethon import TelegramClient

# گرفتن آیدی کانال x_archive و آیدی Inlinebot از متغیر محیطی
X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))
INLINEBOT_ID = int(os.getenv("INLINEBOT_ID"))

async def forward_to_inlinebot(client):
    # دریافت آخرین 10 پیام از کانال x_archive
    channel = await client.get_entity(X_ARCHIVE_CHANNEL_ID)
    messages = await client.get_messages(channel, limit=10)

    for message in messages:
        if message.audio:  # فقط آهنگ‌ها
            try:
                await client.send_message(
                    INLINEBOT_ID,  # ارسال به پیوی Inlinebot
                    message
                )
                print(f"[FORWARD] Song {message.id} forwarded to Inlinebot.")
            except Exception as e:
                print(f"[ERROR] Failed to forward song {message.id}: {e}")

async def forward_files(client):
    await forward_to_inlinebot(client)
