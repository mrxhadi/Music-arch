import os
import json
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import add_song

X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))

async def handle_new_song(event, client):
    message = event.message

    if not message.audio and not message.document:
        return  # اگر پیام آهنگ یا فایل صوتی نبود، خروج

    # اگر فایل صوتی باشد
    if message.audio:
        audio = message.audio
    elif message.document:
        audio = message.document

    title = "Unknown Title"
    singer = "Unknown Singer"
    duration = 0

    # استخراج اطلاعات از attributes اگر موجود باشند
    if isinstance(audio, DocumentAttributeAudio):
        title = audio.title or title
        singer = audio.performer or singer
        duration = audio.duration or duration

    file_id = audio.file_reference.hex() if hasattr(audio, 'file_reference') else audio.id
    channel = await event.get_chat()
    channel_username = channel.username or "Private Channel"
    message_id = message.id

    # فوروارد آهنگ به کانال x_archive برای ثبت رسمی فایل
    await client.send_file(
        entity=X_ARCHIVE_CHANNEL_ID,
        file=message.media,
        caption=f"{title} - {singer}"
    )

    # ثبت در دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)
    print(f"[INLINEBOT] New song added: {title} by {singer}")
