from aiogram import types
from database.songs_db import add_song

GROUP_ID = int(os.getenv("GROUP_ID"))

async def handle_new_song(message: types.Message):
    # فقط پیام‌های گروه مشترک
    if message.chat.id != GROUP_ID:
        return

    if not message.audio:
        return  # اگر پیام آهنگ نبود، خروج

    audio = message.audio
    title = audio.title or "Unknown Title"
    singer = audio.performer or "Unknown Singer"
    duration = audio.duration or 0
    file_id = audio.file_id  # معتبر برای اینلاین مود

    add_song(title, singer, file_id, duration)
    print(f"[INLINEBOT] New song added to database: {title} - {singer}")
