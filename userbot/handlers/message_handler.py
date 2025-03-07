import asyncio
import os
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import add_song

X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))

async def handle_new_song(event, client):
    message = event.message

    if not message.audio:
        return  # اگر پیام آهنگ نبود، خروج

    audio = message.document
    title = "Unknown Title"
    singer = "Unknown Singer"
    duration = 0

    for attr in audio.attributes:
        if isinstance(attr, DocumentAttributeAudio):
            title = attr.title or title
            singer = attr.performer or singer
            duration = attr.duration or duration

    file_id = audio.file_reference.hex()
    channel = await event.get_chat()
    channel_username = channel.username or "Private Channel"
    message_id = message.id

    # فوروارد آهنگ بدون کپشن
    await client.send_file(
        entity=event.chat_id,
        file=message.media,
        caption="",
    )

    # حذف پیام اصلی
    await asyncio.sleep(0.5)
    await message.delete()

    # فوروارد آهنگ به کانال x_archive برای ثبت رسمی فایل
    await client.send_file(
        entity=X_ARCHIVE_CHANNEL_ID,
        file=message.media,
        caption=f"{title} - {singer}"
    )

    # ثبت در دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)
