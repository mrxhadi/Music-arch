import os
import json
from aiogram.types import Document
from database.songs_db import add_song

# اینجا GROUP_ID باید از متغیر محیطی گرفته بشه
GROUP_ID = int(os.getenv("GROUP_ID"))

async def handle_new_song(event, client):
    message = event.message

    # لاگ برای بررسی اینکه پیام از گروه مشترک دریافت میشه یا نه
    print(f"[INLINEBOT] Received message from chat ID: {message.chat.id}, Message: {message.text}")

    # بررسی اینکه آیا پیام شامل آهنگ است (یا فایل صوتی یا داکیومنت)
    if not message.audio and not message.document:
        return  # اگر پیام آهنگ یا فایل صوتی نبود، خروج

    # اگر فایل صوتی باشد
    if message.audio:
        audio = message.audio
    elif message.document:
        audio = message.document

    # مقادیر پیش‌فرض برای اطلاعات آهنگ
    title = "Unknown Title"
    singer = "Unknown Singer"
    duration = 0

    # استخراج اطلاعات از attributes اگر موجود باشند
    if isinstance(audio, Document):
        title = audio.file_name or title
        singer = "Unknown"  # چون در aiogram این اطلاعات ممکن است در دسترس نباشند
        duration = 0  # فرضی: ممکن است اطلاعات duration در فایل صوتی نباشند

    file_id = audio.file_id if hasattr(audio, 'file_id') else audio.id
    channel = await event.get_chat()
    channel_username = channel.username or "Private Channel"
    message_id = message.id

    # ارسال به گروه مشترک
    await client.send_file(
        entity=GROUP_ID,
        file=message.media,
        caption=f"{title} - {singer}"
    )

    # ثبت در دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)
    print(f"[INLINEBOT] New song added: {title} by {singer}")
