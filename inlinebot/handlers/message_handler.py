import os
from aiogram.types import Message
from aiogram import types
from database.songs_db import add_song

# گروه مشترک، بررسی اینکه پیام مربوط به گروه است
GROUP_ID = int(os.getenv("GROUP_ID"))  # از GROUP_ID در متغیر محیطی استفاده می‌کنیم

async def handle_new_song(message: Message):
    # اگر پیام شامل audio باشد
    if message.audio:
        # استخراج مشخصات آهنگ
        title = message.audio.title or "Unknown Title"
        singer = message.audio.performer or "Unknown Singer"
        duration = message.audio.duration or 0
        file_id = message.audio.file_id
    # اگر پیام شامل document (که می‌تواند یک فایل صوتی باشد)
    elif message.document:
        if 'audio' in message.document.mime_type:
            title = message.document.attributes[0].title or "Unknown Title"
            singer = message.document.attributes[0].performer or "Unknown Singer"
            duration = message.document.attributes[0].duration or 0
            file_id = message.document.file_id
        else:
            return  # اگر پیام شامل فایل صوتی نباشد، آن را نادیده می‌گیریم
    else:
        return  # اگر پیام نه audio و نه document دارد، هیچ کاری نمی‌کنیم

    channel_username = message.chat.username or "Private Channel"
    message_id = message.message_id

    # افزودن آهنگ به دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)

    print(f"[GROUP] New song added: {title} by {singer}")
