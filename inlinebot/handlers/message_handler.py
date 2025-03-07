import os
import json
from aiogram.types import Document
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
    if isinstance(audio, Document):
        # در اینجا باید اطلاعات را از Document به درستی استخراج کنیم
        title = audio.file_name or title
        singer = "Unknown"  # چون در aiogram این اطلاعات ممکن است در دسترس نباشند
        duration = 0  # فرضی: ممکن است اطلاعات duration در فایل صوتی نباشند

    file_id = audio.file_id if hasattr(audio, 'file_id') else audio.id
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
